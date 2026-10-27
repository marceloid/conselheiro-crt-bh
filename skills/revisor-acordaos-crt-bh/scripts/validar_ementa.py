#!/usr/bin/env python3
"""
Validador Automático de Ementas do CRT-BH (Conselho de Recursos Tributários).
Verifica verbetação (6 níveis), normas municipais e direito intertemporal, precedentes vinculantes,
anti-casuísmo e fechos oficiais.

Uso:
    python validar_ementa.py caminho/para/arquivo.docx
    python validar_ementa.py caminho/para/ementa.txt
    python validar_ementa.py "ISSQN – REVISÃO DO LANÇAMENTO..."
"""

import sys
import os
import re
import zipfile
import xml.etree.ElementTree as ET

CANONICAL_NIVEL_1 = {
    "ISSQN", "ITBI", "IPTU", "TFLF", "TFEP", "TFS", "TAXAS", "SIMPLES NACIONAL", "AGRAVO"
}

GENERIC_NIVEL_1_WARNINGS = {
    "AITI": "Substitua 'AITI' pelo tributo específico correspondente (ex.: ISSQN, TAXAS, ITBI).",
    "RECURSO": "Inicie com a espécie tributária envolvida, deixando a espécie recursal para o fecho.",
    "PEDIDO": "Inicie com a espécie tributária envolvida (ex.: ITBI – PEDIDO DE RECONHECIMENTO DE IMUNIDADE...).",
    "IMPUGNAÇÃO": "Inicie com a espécie tributária ou 'SIMPLES NACIONAL'.",
    "PROCESSO": "Inicie com a matéria de fundo ou espécie tributária.",
    "TVF": "Substitua pela espécie tributária examinada na ação fiscal.",
}

PREDECENTS_MAP = [
    {
        "pattern": r"Tema\s+(?:n[º°\.]?\s*)?487\b",
        "expected_re": r"RE\s+640\.?452",
        "wrong_re": r"RE\s+582\.?461",
        "description": "Tema 487 do STF (multa isolada por dever instrumental)",
        "correct_citation": "Tema 487 do STF (RE 640.452/RO)",
        "why_wrong": "O RE 582.461/SP refere-se ao Tema 214 (multa moratória)."
    },
    {
        "pattern": r"Tema\s+(?:n[º°\.]?\s*)?214\b",
        "expected_re": r"RE\s+582\.?461",
        "description": "Tema 214 do STF (limite de 20% para multa moratória)",
        "correct_citation": "Tema 214 do STF (RE 582.461/SP)",
    },
    {
        "pattern": r"Tema\s+(?:n[º°\.]?\s*)?796\b",
        "expected_re": r"RE\s+796\.?376",
        "description": "Tema 796 do STF (imunidade de ITBI na integralização de capital)",
        "correct_citation": "Tema 796 do STF (RE 796.376/SC)",
    },
    {
        "pattern": r"Tema\s+(?:n[º°\.]?\s*)?1\.?113\b",
        "expected_re": r"REsp\s+1\.?937\.?821",
        "description": "Tema 1.113 do STJ (presunção relativa do valor declarado no ITBI)",
        "correct_citation": "Tema 1.113 do STJ (REsp 1.937.821/SP)",
    },
    {
        "pattern": r"Tema\s+(?:n[º°\.]?\s*)?863\b",
        "expected_re": r"RE\s+736\.?090",
        "description": "Tema 863 do STF (limite de multa punitiva qualificada)",
        "correct_citation": "Tema 863 do STF (RE 736.090/SC)",
    }
]

FORBIDDEN_FECHOS = [
    (r"por\s+tudo\s+que\s+restou\s+provado", "Fórmula arcaica e prolixa; substitua pela fórmula enxuta da Secretaria."),
    (r"por\s+tudo\s+que\s+dos\s+autos\s+consta", "Fórmula arcaica e prolixa; substitua pela fórmula enxuta da Secretaria."),
    (r"mister\s+o\s+desprovimento", "Fórmula prolixa; substitua por 'Recurso voluntário conhecido e desprovido.'"),
    (r"mister\s+o\s+provimento", "Fórmula prolixa; substitua por 'Recurso voluntário conhecido e provido.'"),
    (r"reexame\s+necess[aá]rio\s+(?:provido|desprovido)", "Erro processual grave: Reexame Necessário não é recurso. Use 'mantida a decisão de primeira instância' ou 'reformada a decisão de primeira instância'."),
]

def extract_text_from_docx(path: str) -> str:
    with zipfile.ZipFile(path, "r") as z:
        xml_content = z.read("word/document.xml")
        tree = ET.fromstring(xml_content)
        W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        paras = []
        in_ementa = False
        ementa_lines = []
        for p in tree.iter(f"{W}p"):
            texts = [node.text for node in p.iter(f"{W}t") if node.text]
            p_text = "".join(texts).strip()
            if not p_text:
                continue
            if p_text.upper() == "EMENTA":
                in_ementa = True
                continue
            if in_ementa:
                if p_text.upper().startswith("ACÓRDÃO") or p_text.upper().startswith("ACORDA") or p_text.upper().startswith("VISTOS"):
                    break
                ementa_lines.append(p_text)
        if ementa_lines:
            return "\n".join(ementa_lines)
        return "\n".join(paras)

def validate_ementa(text: str):
    issues = [] # list of (severity, code, message, suggestion)
    
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    if not lines:
        return [("ERRO", "EMPTY", "Texto da ementa vazio ou não localizado.", None)]
        
    first_line = lines[0]
    body_topics = lines[1:] if len(lines) > 1 else []
    
    # ── 1. AUDITORIA DA VERBETAÇÃO ───────────────────────────────────
    has_dash = any(sep in first_line for sep in [" – ", " - ", " − "])
    if not has_dash:
        issues.append(("ERRO", "VERBETACAO_FORMATO", 
            "A primeira linha não aparenta ser uma verbetação válida com separadores de travessão (' – ').",
            "Estruture em 6 níveis em caixa alta separados por travessão: 1º TRIBUTO – 2º PROCEDIMENTO – 3º INSTITUTO – 4º TESE – 5º FUNDAMENTO – 6º RESULTADO."))
    else:
        # Check separator uniformity
        if " - " in first_line:
            issues.append(("AVISO", "SEPARADOR_HIFEN", 
                "Verbetação utilizando hífen simples (' - ') em vez do travessão oficial (' – ').",
                "Substituir ' - ' por ' – ' (en-dash com espaços laterais)."))
        if " − " in first_line:
            issues.append(("AVISO", "SEPARADOR_MENOS", 
                "Verbetação utilizando caractere de sinal de subtração (' − ') em vez do travessão (' – ').",
                "Substituir ' − ' por ' – '."))
                
        levels = [lvl.strip() for lvl in re.split(r"\s+[–−-]\s+", first_line) if lvl.strip()]
        num_levels = len(levels)
        
        if num_levels < 5:
            issues.append(("AVISO", "NIVEIS_INSUFICIENTES", 
                f"Verbetação com apenas {num_levels} níveis. O padrão oficial do CRT recomenda 6 níveis bem definidos.",
                "Complete os níveis faltantes (Tributo, Procedimento, Instituto Central, Tese Específica, Fundamento/Precedente e Resultado)."))
        elif num_levels > 8:
            issues.append(("AVISO", "NIVEIS_EXCESSIVOS", 
                f"Verbetação excessivamente longa com {num_levels} níveis (a média recomendada são 6 níveis objetivos).",
                "Sintetize os desdobramentos fáticos e concentre-se nas 6 categorias canônicas."))
                
        # Nível 1 check
        if levels:
            n1 = levels[0].upper()
            matched_canonical = any(n1 == c or n1.startswith(c + " ") or n1.startswith(c + "–") for c in CANONICAL_NIVEL_1)
            if not matched_canonical:
                for gen_word, advice in GENERIC_NIVEL_1_WARNINGS.items():
                    if gen_word in n1:
                        issues.append(("ERRO", "NIVEL_1_GENERICO", 
                            f"O 1º nível da verbetação inicia com termo genérico ('{levels[0]}').",
                            advice))
                        break
                else:
                    issues.append(("AVISO", "NIVEL_1_NAO_CANONICO", 
                        f"O 1º nível ('{levels[0]}') não consta na lista canônica dos tributos do CRT ({', '.join(sorted(CANONICAL_NIVEL_1))}).",
                        "Inicie pelo nome do tributo ou matéria principal (ex.: ISSQN, ITBI, IPTU)."))
                        
        # Final level check (outcome)
        if levels and len(levels) >= 2:
            last_lvl = levels[-1].upper()
            has_outcome = any(k in last_lvl for k in ["PROVIDO", "DESPROVIDO", "MANTIDA", "REFORMADA", "CONHECIDO", "EXTINTO"])
            if not has_outcome:
                issues.append(("AVISO", "NIVEL_FINAL_SEM_RESULTADO", 
                    f"O último nível da verbetação ('{levels[-1]}') não expressa o resultado do julgamento.",
                    "Encerre o 6º nível com o resultado (ex.: RECURSO VOLUNTÁRIO CONHECIDO E DESPROVIDO / REEXAME NECESSÁRIO – MANUTENÇÃO DA DECISÃO “A QUO”)."))
            if last_lvl.endswith(" ."):
                issues.append(("AVISO", "PONTO_ESPACO", 
                    "Espaço gráfico antes do ponto final no fecho da verbetação (' .').",
                    "Eliminar o espaço antes do ponto."))

    # ── 2. AUDITORIA DE DIREITO INTERTEMPORAL ─────────────────────────
    full_text = text
    
    # Decreto 11.467/2003 (DES)
    if re.search(r"Decreto\s+(?:Municipal\s+)?n[º°\.]?\s*11\.?467", full_text, re.IGNORECASE):
        issues.append(("AVISO", "DECRETO_DES_REVOGADO", 
            "Citação do Decreto Municipal nº 11.467/2003 (Regulamento da DES).",
            "Atenção ao Direito Intertemporal: O Decreto nº 11.467/2003 foi expressamente revogado pelo Decreto Municipal nº 17.174, de 27/09/2019 (art. 2º, V). Se a autuação/competência fiscalizada for posterior a setembro de 2019, a citação correta é do Decreto Municipal nº 17.174/2019."))
            
    # Decreto 16.197/2016 (Regulamento do CART)
    if re.search(r"Decreto\s+(?:Municipal\s+)?n[º°\.]?\s*16\.?197", full_text, re.IGNORECASE):
        issues.append(("AVISO", "DECRETO_CART_REVOGADO", 
            "Citação do Decreto Municipal nº 16.197/2016 (Regulamento do CART-BH).",
            "Atenção ao Direito Intertemporal: O Decreto nº 16.197/2016 foi expressamente revogado pelo Decreto nº 18.716/2024 (que vigeu até o Dec. 18.783/2024, sucedido pelo atual Dec. 19.460/2026). Para sessões e ritos atuais, cite o regulamento vigente."))
            
    # Lei 9.249/1955 (Typo crasso)
    if re.search(r"Lei\s+(?:Federal\s+)?n[º°\.]?\s*9\.?249(?:[,\s]+de)?\s*1955", full_text, re.IGNORECASE):
        issues.append(("ERRO", "ERRO_ANO_LEI_9249", 
            "Citação com ano incorreto: 'Lei nº 9.249, de 1955'.",
            "Corrigir para 'Lei Federal nº 9.249, de 1995'."))
            
    # Art. 101 do CTN (Typo crasso para CTM)
    if re.search(r"art(?:igo|\.)\s*101\s+do\s+(?:C[oó]digo\s+Tribut[aá]rio\s+Nacional|CTN)", full_text, re.IGNORECASE):
        issues.append(("ERRO", "ERRO_ART_101_CTN", 
            "Citação do art. 101 do CTN para requisitos de clareza/precisão do Auto de Infração.",
            "Substituir por 'art. 101 do Código Tributário Municipal (CTM - Lei Municipal nº 1.310/1966)'. O CTN não disciplina requisitos formais de auto de infração em seu art. 101."))

    # Sigla de Conselho "CRT-BH" ou "Corte"
    if "CRT-BH" in full_text:
        issues.append(("AVISO", "SIGLA_CRT_BH", 
            "Emprego da sigla despadronizada 'CRT-BH'.",
            "No âmbito do Conselho, use exclusivamente 'Conselho de Recursos Tributários (CRT)' ou 'CRT' (sem o sufixo '-BH')."))
    if re.search(r"\b(?:esta\s+Corte|aquela\s+Corte|Corte\s+Maior)\b", full_text, re.IGNORECASE):
        issues.append(("ERRO", "TERMO_CORTE_VEDADO", 
            "Emprego do termo 'Corte' para referir-se ao CRT ou tribunais judiciais.",
            "Regra de Ouro nº 5 da Presidência do CRT: veda-se estritamente o uso da palavra 'Corte'. Substitua por 'Conselho', 'Tribunal' ou 'Supremo Tribunal Federal'."))

    # ── 3. AUDITORIA DE PRECEDENTES STF / STJ ─────────────────────────
    for line in lines:
        for prec in PREDECENTS_MAP:
            if re.search(prec["pattern"], line, re.IGNORECASE):
                if "wrong_re" in prec and re.search(prec["wrong_re"], line, re.IGNORECASE):
                    issues.append(("ERRO", "PRECEDENTE_INVERTIDO", 
                        f"Inversão ou erro no precedente vinculado ao {prec['description']} na mesma proposição: {prec.get('why_wrong', '')}",
                        f"Citação correta: {prec['correct_citation']}"))
                elif "expected_re" in prec and not re.search(prec["expected_re"], line, re.IGNORECASE):
                    found_res = re.findall(r"RE(?:sp)?\s+[\d\./-]+", line, re.IGNORECASE)
                    if found_res:
                        issues.append(("AVISO", "PRECEDENTE_LEADING_CASE", 
                            f"Verifique se o leading case citado na proposição para o {prec['description']} está correto.",
                            f"Precedente padrão: {prec['correct_citation']}"))

    # ── 4. AUDITORIA DOS TÓPICOS E ANTI-CASUÍSMO ─────────────────────
    if body_topics:
        # Check if first character is a dash
        for i, topic in enumerate(body_topics):
            if not (topic.startswith("- ") or topic.startswith("– ") or topic.startswith("— ")):
                issues.append(("AVISO", "TOPICO_SEM_TRACO", 
                    f"Tópico {i+1} da ementa não se inicia com traço padronizado ('- ').",
                    f"Iniciar com '- ': {topic[:50]}..."))
                    
            # Anti-casuísmo: check company suffixes
            if re.search(r"\b(?:LTDA|S/?A|S\.A\.|EIRELI|ME|EPP)\b", topic):
                issues.append(("AVISO", "ANTI_CASUISMO_PARTE", 
                    f"Tópico {i+1} cita razão social ou tipo societário específico de parte.",
                    "Ementas devem fixar teses abstratas despersonalizadas. Substitua nomes empresariais por 'o sujeito passivo', 'a tomadora' ou 'a pessoa jurídica'."))
                    
            # Anti-casuísmo: check specific notas fiscais or volume
            if re.search(r"\bnotas?\s+fiscais?\s+n[º°\.]?\s*\d+", topic, re.IGNORECASE):
                issues.append(("AVISO", "ANTI_CASUISMO_DOC", 
                    f"Tópico {i+1} menciona números específicos de notas fiscais.",
                    "Generalize a menção fática para 'documentos fiscais emitidos no período'."))

    # ── 5. AUDITORIA DO FECHO ─────────────────────────────────────────
    if body_topics:
        fecho = body_topics[-1]
        for pat, advice in FORBIDDEN_FECHOS:
            if re.search(pat, fecho, re.IGNORECASE):
                issues.append(("ERRO", "FECHO_INVALIDO", 
                    f"O fecho da ementa contém fórmula não recomendada ou errônea: '{fecho[:60]}...'",
                    advice))
                    
        # Plural with apostrophe in fecho or body
        if re.search(r"AITI[’']s", full_text):
            issues.append(("AVISO", "SIGLA_PLURAL_APOSTROFO", 
                "Grafia de sigla no plural com apóstrofo ('AITI's' ou 'AITI’s').",
                "Substituir por 'AITIs' sem apóstrofo."))

    return issues

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
        
    arg = sys.argv[1]
    if os.path.isfile(arg):
        if arg.lower().endswith(".docx"):
            print(f"📄 Extraindo ementa de arquivo Word: {arg}")
            text = extract_text_from_docx(arg)
        else:
            with open(arg, "r", encoding="utf-8") as f:
                text = f.read()
    else:
        text = arg
        
    print("\n" + "="*70)
    print("⚖️  AUDITORIA DE EMENTA DO CRT-BH (RELATÓRIO TÉCNICO)")
    print("="*70)
    print("\n[TEXTO ANALISADO]:")
    print("-" * 50)
    lines = text.strip().split("\n")
    for l in lines[:8]:
        print(f"  {l}")
    if len(lines) > 8:
        print(f"  ... (+ {len(lines)-8} linhas)")
    print("-" * 50 + "\n")
    
    issues = validate_ementa(text)
    
    erros = [i for i in issues if i[0] == "ERRO"]
    avisos = [i for i in issues if i[0] == "AVISOS" or i[0] == "AVISO"]
    
    print(f"Resultado: {len(erros)} ERROS CRÍTICOS | {len(avisos)} AVISOS\n")
    
    if not issues:
        print("✅ EMENTA EM PLENA CONFORMIDADE COM OS PADRÕES DO CRT-BH!")
        sys.exit(0)
        
    for sev, code, msg, sugg in issues:
        icon = "❌ [ERRO CRÍTICO]" if sev == "ERRO" else "⚠️  [AVISO]"
        print(f"{icon} ({code}): {msg}")
        if sugg:
            print(f"   💡 Recomendação: {sugg}")
        print()

if __name__ == "__main__":
    main()
