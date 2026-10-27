#!/usr/bin/env python3
"""
Extrator e Catalogaçador de Teses-Paradigma do CRT-BH a partir de decisao.csv.
Gera arquivos temáticos estruturados em references/teses/ com as teses canônicas e acórdãos precedentes.
"""

import sys
import os
import re
from collections import defaultdict
import pandas as pd

CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../decisao.csv"))
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../references/teses"))

def clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip()

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Erro: Arquivo {CSV_PATH} não encontrado.")
        sys.exit(1)
        
    os.makedirs(OUT_DIR, exist_ok=True)
    
    print(f"Lendo base histórica com pandas: {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH, sep=";")
    print(f"Total de decisões carregadas: {len(df)}")
    
    cat_theses = {
        "itbi": defaultdict(list),
        "issqn": defaultdict(list),
        "iptu_taxas": defaultdict(list),
        "processual": defaultdict(list)
    }
    
    for idx, row in df.iterrows():
        ementa = str(row.get("ementa", "")).strip()
        if not ementa or ementa == "nan":
            continue
            
        lines = [l.strip() for l in ementa.split("\n") if l.strip()]
        if len(lines) <= 1:
            continue
            
        first_line = lines[0]
        topics = lines[1:-1]
        
        acordao = str(row.get("numero_da_decisao", "")).strip()
        camara = str(row.get("camara", "")).strip()
        data = str(row.get("data_do_julgamento", ""))[:10]
        relator = str(row.get("relator", "")).strip()
        redator = str(row.get("redator", "")).strip()
        autor_tese = f"Red. {redator}" if redator and redator != "nan" else f"Rel. {relator}"
        
        meta = {
            "acordao": acordao,
            "camara": camara,
            "data": data,
            "autor": autor_tese,
            "first_line": first_line
        }
        
        full_em_upper = ementa.upper()
        
        # ── ITBI ─────────────────────────────────────────────────────
        if "ITBI" in first_line.upper():
            if "796" in full_em_upper or "INTEGRALIZAÇÃO" in full_em_upper or "CAPITAL SOCIAL" in full_em_upper:
                cat_theses["itbi"]["integralizacao_capital"].append((topics, meta))
            elif "1.113" in full_em_upper or "1113" in full_em_upper or "ARBITRAMENTO" in full_em_upper or "148" in full_em_upper:
                cat_theses["itbi"]["arbitramento_base_calculo"].append((topics, meta))
            elif "17.026" in full_em_upper or "120 DIAS" in full_em_upper or "VINCULAÇÃO" in full_em_upper:
                cat_theses["itbi"]["vinculacao_temporal_base_calculo"].append((topics, meta))
            elif "PREPONDERÂNCIA" in full_em_upper or "ATIVIDADE IMOBILIÁRIA" in full_em_upper:
                cat_theses["itbi"]["preponderancia_atividade"].append((topics, meta))
            else:
                cat_theses["itbi"]["outros_itbi"].append((topics, meta))
                
        # ── ISSQN ────────────────────────────────────────────────────
        elif "ISSQN" in first_line.upper() or "ISS" in first_line.upper():
            if "ESTABELECIMENTO PRESTADOR" in full_em_upper or "SUJEIÇÃO ATIVA" in full_em_upper or "LOCAL DA PRESTAÇÃO" in full_em_upper or "UNIDADE ECONÔMICA" in full_em_upper:
                cat_theses["issqn"]["local_incidencia_estabelecimento"].append((topics, meta))
            elif "REENQUADRAMENTO" in full_em_upper or "VÍCIO DE MOTIVAÇÃO" in full_em_upper or "142 DO CTN" in full_em_upper:
                cat_theses["issqn"]["incompetencia_jjt_reenquadramento"].append((topics, meta))
            elif "RETENÇÃO NA FONTE" in full_em_upper or "RETENTOR OBRIGATÓRIO" in full_em_upper or "DES" in full_em_upper:
                cat_theses["issqn"]["retencao_fonte_obrigacoes_acessorias"].append((topics, meta))
            elif "SOCIEDADE DE PROFISSIONAIS" in full_em_upper or "SUP" in full_em_upper:
                cat_theses["issqn"]["sociedade_uniprofissional_sup"].append((topics, meta))
            elif "CONSTRUÇÃO CIVIL" in full_em_upper or "7.02" in full_em_upper or "SUBEMPREITADA" in full_em_upper:
                cat_theses["issqn"]["construcao_civil_deducoes"].append((topics, meta))
            else:
                cat_theses["issqn"]["outros_issqn"].append((topics, meta))
                
        # ── IPTU E TAXAS ─────────────────────────────────────────────
        elif any(t in first_line.upper() for t in ["IPTU", "TFLF", "TFEP", "TFS", "TAXA"]):
            if "PEDOLOGIA" in full_em_upper or "INUNDAÇÃO" in full_em_upper or "FATOR DE CORREÇÃO" in full_em_upper:
                cat_theses["iptu_taxas"]["pedologia_inundabilidade"].append((topics, meta))
            elif "146 DO CTN" in full_em_upper or "CRITÉRIO JURÍDICO" in full_em_upper:
                cat_theses["iptu_taxas"]["mudanca_criterio_juridico_146"].append((topics, meta))
            elif "COWORKING" in full_em_upper or "RESIDÊNCIA" in full_em_upper or "DOMICÍLIO" in full_em_upper:
                cat_theses["iptu_taxas"]["tflf_domicilio_coworking"].append((topics, meta))
            elif "ENGENHO" in full_em_upper or "PUBLICIDADE" in full_em_upper or "TFEP" in full_em_upper:
                cat_theses["iptu_taxas"]["tfep_publicidade"].append((topics, meta))
            else:
                cat_theses["iptu_taxas"]["outros_iptu_taxas"].append((topics, meta))
                
        # ── PROCESSUAL E AGRAVOS ──────────────────────────────────────
        elif any(t in first_line.upper() for t in ["AGRAVO", "IMPUGNAÇÃO", "SIMPLES NACIONAL", "DESPACHO", "AITI"]):
            cat_theses["processual"]["agravos_notificacoes_defesas"].append((topics, meta))

    print("\nEstatísticas de Teses Catalogadas:")
    for cat, subdict in cat_theses.items():
        total_cat = sum(len(v) for v in subdict.values())
        print(f"  [{cat.upper()}]: {total_cat} decisões classificadas em {len(subdict)} temas")

    # ── GERAÇÃO DOS ARQUIVOS MARKDOWN ─────────────────────────────────
    
    # 1. ITBI
    with open(os.path.join(OUT_DIR, "itbi.md"), "w", encoding="utf-8") as f:
        f.write("# Catálogo de Teses-Paradigma: ITBI\n\n")
        f.write("Este repositório consolida as teses jurídicas padronizadas de ITBI formuladas pelo CRT-BH.\n\n---\n\n")
        
        # Tema 1: Integralização de Capital e Tema 796
        f.write("## 1. Integralização de Capital Social e Alcance da Imunidade (Tema 796 do STF)\n\n")
        f.write("**Verbetação Recomendada:**\n")
        f.write("> **`ITBI – IMUNIDADE TRIBUTÁRIA – INTEGRALIZAÇÃO DE CAPITAL SOCIAL COM IMÓVEL – VALOR DE AVALIAÇÃO FISCAL SUPERIOR AO VALOR INTEGRALIZADO – TRIBUTAÇÃO DA PARCELA EXCEDENTE – POSSIBILIDADE – TEMA 796 DO STF – ACÓRDÃO Nº 11.317-E/CER – RECURSO VOLUNTÁRIO CONHECIDO E DESPROVIDO.`**\n\n")
        f.write("**Teses Normativas Paradigmáticas:**\n")
        f.write("- A imunidade do ITBI prevista no art. 156, § 2º, I, da CF/88 alcança a transmissão de bens imóveis incorporados ao patrimônio de pessoa jurídica em realização de capital apenas até o limite do valor do capital social subscrito e integralizado.\n")
        f.write("- O valor do bem imóvel que exceder o montante do capital social integralizado está sujeito à incidência do ITBI, independentemente da existência ou não de formação formal de reserva de capital ou ágio na subscrição de quotas, consoante pacificado pela Câmara Especial de Recursos (Acórdão nº 11.317-E/CER) com esteio no Tema 796 do Supremo Tribunal Federal (RE 796.376/SC).\n\n")
        f.write("**Acórdãos Precedentes Relevantes:**\n")
        for topics, meta in cat_theses["itbi"]["integralizacao_capital"][:8]:
            f.write(f"- **Acórdão nº {meta['acordao']}** ({meta['camara']} – {meta['data']} – {meta['autor']})\n")
        f.write("\n---\n\n")

        # Tema 2: Presunção Relativa e Arbitramento
        f.write("## 2. Presunção Relativa do Valor Declarado e Arbitramento de Base de Cálculo (Tema 1.113 do STJ)\n\n")
        f.write("**Verbetação Recomendada:**\n")
        f.write("> **`ITBI – BASE DE CÁLCULO – VALOR VENAL – VALOR DECLARADO PELO CONTRIBUINTE – PRESUNÇÃO RELATIVA DE VERACIDADE – TEMA 1.113 DO STJ – DESCONSTITUIÇÃO POR PROCEDIMENTO ADMINISTRATIVO REGULAR – ART. 148 DO CTN – AVALIAÇÃO ESPECÍFICA – RECURSO VOLUNTÁRIO DESPROVIDO.`**\n\n")
        f.write("**Teses Normativas Paradigmáticas:**\n")
        f.write("- O valor da transação declarado pelo contribuinte goza de presunção de veracidade em relação ao valor de mercado do imóvel, em observância ao princípio da boa-fé e à diretriz firmada pelo STJ no Tema 1.113 (REsp 1.937.821/SP).\n")
        f.write("- Essa presunção possui natureza relativa (juris tantum) e pode ser legitimamente ilidida pelo Fisco municipal mediante regular procedimento administrativo de arbitramento da base de cálculo, com esteio no art. 148 do CTN, assegurando-se ciência prévia dos critérios técnicos ao sujeito passivo.\n\n")
        f.write("**Acórdãos Precedentes Relevantes:**\n")
        for topics, meta in cat_theses["itbi"]["arbitramento_base_calculo"][:8]:
            f.write(f"- **Acórdão nº {meta['acordao']}** ({meta['camara']} – {meta['data']} – {meta['autor']})\n")
        f.write("\n---\n\n")

        # Tema 3: Vinculação Temporal da Avaliação
        f.write("## 3. Vinculação Temporal de 120 Dias da Base de Cálculo (Art. 7º do Dec. 17.026/2018)\n\n")
        f.write("**Verbetação Recomendada:**\n")
        f.write("> **`ITBI – BASE DE CÁLCULO – APURAÇÃO FISCAL PRELIMINAR – VINCULAÇÃO TEMPORAL DA ADMINISTRAÇÃO PELO PRAZO DE 120 DIAS – ART. 7º DO DECRETO MUNICIPAL Nº 17.026/2018 (REDAÇÃO DO DECRETO Nº 18.735/2024) – SEGUNDA AVALIAÇÃO COM NOVA METODOLOGIA EM SEDE DE RESPOSTA A RECLAMAÇÃO – IMPOSSIBILIDADE – NULIDADE RECONHECIDA – RECURSO VOLUNTÁRIO PROVIDO.`**\n\n")
        f.write("**Teses Normativas Paradigmáticas:**\n")
        f.write("- O valor da base de cálculo apurada vincula a administração tributária municipal durante o prazo improrrogável de 120 (cento e vinte) dias, contados da notificação do contribuinte, a teor do art. 7º do Decreto Municipal nº 17.026/2018 (redação dada pelo Decreto nº 18.735/2024), ressalvadas apenas as estritas hipóteses de revisão de ofício do art. 149 do CTN.\n")
        f.write("- O Fisco não pode, dentro do prazo de vinculação regulamentar e sob o pretexto de responder a uma reclamação tempestiva, reescrever a apuração primitiva substituindo-a por uma segunda avaliação específica com metodologia distinta.\n\n")
        f.write("**Acórdãos Precedentes Relevantes:**\n")
        f.write("- **Acórdão nº 11.676/3ª** (3ª Câmara – 30/07/2026 – Rel. Matheus Santos Castro)\n")
        f.write("- **Acórdão nº 11.932/3ª** (3ª Câmara – Rel. João Marcelo Araújo Vieira)\n")

    # 2. ISSQN
    with open(os.path.join(OUT_DIR, "issqn.md"), "w", encoding="utf-8") as f:
        f.write("# Catálogo de Teses-Paradigma: ISSQN\n\n")
        f.write("Este repositório consolida as teses jurídicas padronizadas de ISSQN formuladas pelo CRT-BH.\n\n---\n\n")
        
        # Tema 1: Local da Incidência
        f.write("## 1. Sujeição Ativa e Local da Incidência (Art. 3º da LC nº 116/2003 e Unidade Autônoma)\n\n")
        f.write("**Verbetação Recomendada:**\n")
        f.write("> **`ISSQN – REVISÃO DE LANÇAMENTO – LOCAL DA INCIDÊNCIA – REGRA GERAL DO ESTABELECIMENTO PRESTADOR – ART. 3º, CAPUT, DA LEI COMPLEMENTAR Nº 116/2003 – PRESTAÇÃO DE SERVIÇOS EM PLANTAS DOS TOMADORES – DESLOCAMENTO TRANSITÓRIO DE PROFISSIONAIS – NÃO CARACTERIZAÇÃO DE UNIDADE ECONÔMICA AUTÔNOMA – SUJEIÇÃO ATIVA DO MUNICÍPIO DE BELO HORIZONTE – RECURSO VOLUNTÁRIO DESPROVIDO.`**\n\n")
        f.write("**Teses Normativas Paradigmáticas:**\n")
        f.write("- A teor do art. 3º, caput, da Lei Complementar nº 116/2003, o ISSQN é devido, como regra geral, no local do estabelecimento prestador do serviço, caracterizado pela unidade econômica ou profissional que centraliza a organização dos fatores de produção.\n")
        f.write("- O simples deslocamento temporário de técnicos ou equipamentos para a execução de serviços nas dependências da tomadora (plantas industriais ou áreas de mineração), desprovido de estrutura gerencial própria e autônoma, não desloca o critério espacial da hipótese de incidência para o município do tomador.\n\n")
        f.write("**Acórdãos Precedentes Relevantes:**\n")
        for topics, meta in cat_theses["issqn"]["local_incidencia_estabelecimento"][:8]:
            f.write(f"- **Acórdão nº {meta['acordao']}** ({meta['camara']} – {meta['data']} – {meta['autor']})\n")
        f.write("\n---\n\n")

        # Tema 2: Vício de Motivação / Reenquadramento JJT
        f.write("## 2. Incompetência Funcional dos Órgãos Julgadores para Reenquadramento Substitutivo (Art. 142 do CTN)\n\n")
        f.write("**Verbetação Recomendada:**\n")
        f.write("> **`ISSQN – AUTO DE INFRAÇÃO – RECLASSIFICAÇÃO DE SERVIÇOS REALIZADA DE OFÍCIO PELA JUNTA DE JULGAMENTO TRIBUTÁRIO (JJT) – IMPOSSIBILIDADE DO ÓRGÃO JULGADOR REALIZAR LANÇAMENTO SUBSTITUTIVO – COMPETÊNCIA PRIVATIVA DA AUTORIDADE LANÇADORA – ART. 142 DO CTN – VÍCIO INSANÁVEL DE MOTIVAÇÃO – NULIDADE DOS ITENS REENQUADRADOS – RECURSO VOLUNTÁRIO PARCIALMENTE PROVIDO.`**\n\n")
        f.write("**Teses Normativas Paradigmáticas:**\n")
        f.write("- A constituição do crédito tributário pelo lançamento é atividade administrativa plenamente vinculada e privativa da autoridade fiscal lançadora (art. 142 do CTN), cabendo aos órgãos julgadores da 1ª e 2ª instâncias (JJT e CRT) exclusivamente o controle da legalidade do ato administrativo primitivo.\n")
        f.write("- É nulo por vício de motivação e violação ao contraditório o reenquadramento de serviços procedido de ofício pela instância julgadora administrativa para subitem diverso do capitulado no auto de infração originário, impondo-se a exclusão do crédito das notas fiscais afetadas pela alteração indevida de tipificação.\n\n")
        f.write("**Acórdãos Precedentes Relevantes:**\n")
        for topics, meta in cat_theses["issqn"]["incompetencia_jjt_reenquadramento"][:8]:
            f.write(f"- **Acórdão nº {meta['acordao']}** ({meta['camara']} – {meta['data']} – {meta['autor']})\n")
        f.write("\n---\n\n")

        # Tema 3: Retenção na Fonte Compulsória e DES
        f.write("## 3. Retenção na Fonte Obrigatória e Obrigações Acessórias da DES\n\n")
        f.write("**Verbetação Recomendada:**\n")
        f.write("> **`ISSQN – DESCUMPRIMENTO DE OBRIGAÇÃO ACESSÓRIA – RETENÇÃO NA FONTE – TOMADOR ENQUADRADO COMO RETENTOR OBRIGATÓRIO – ART. 20, VIII, DA LEI MUNICIPAL Nº 8.725/2003 – LIMITE LEGAL APURADO NAS DECLARAÇÕES DO SUJEITO PASSIVO – EXCLUSÃO DE CORREÇÃO MONETÁRIA PELO DECRETO MUNICIPAL Nº 15.445/2013 – INFRAÇÃO MENSAL PERIÓDICA – INEXISTÊNCIA DE BIS IN IDEM – RECURSO VOLUNTÁRIO DESPROVIDO.`**\n\n")
        f.write("**Teses Normativas Paradigmáticas:**\n")
        f.write("- O enquadramento do tomador de serviços como retentor obrigatório do ISSQN decorre de critério objetivo e opera de pleno direito quando os valores anuais despendidos com a contratação de terceiros superam o limite legalmente fixado, prescindindo de prévio enquadramento formal da autoridade fazendária.\n")
        f.write("- A sanção pela omissão de retenção possui natureza de dever instrumental autônomo, incidindo mensalmente por competência de apuração, sendo legítima a autuação englobada em documento único sem que isso configure dupla penalização sobre o mesmo fato gerador.\n\n")
        f.write("**Acórdãos Precedentes Relevantes:**\n")
        for topics, meta in cat_theses["issqn"]["retencao_fonte_obrigacoes_acessorias"][:8]:
            f.write(f"- **Acórdão nº {meta['acordao']}** ({meta['camara']} – {meta['data']} – {meta['autor']})\n")

    # 3. IPTU E TAXAS
    with open(os.path.join(OUT_DIR, "iptu_taxas.md"), "w", encoding="utf-8") as f:
        f.write("# Catálogo de Teses-Paradigma: IPTU e Taxas Municipais\n\n")
        f.write("Este repositório consolida as teses jurídicas padronizadas de IPTU e Taxas Municipais (TFLF, TFEP e TFS) formuladas pelo CRT-BH.\n\n---\n\n")
        
        # Tema 1: Fator Pedologia e Área de Risco de Inundação
        f.write("## 1. IPTU: Fator de Correção Pedologia e Área de Risco de Inundação\n\n")
        f.write("**Verbetação Recomendada:**\n")
        f.write("> **`IPTU – REVISÃO DE LANÇAMENTO – BASE DE CÁLCULO – FATOR DE CORREÇÃO DO TERRENO – PEDOLOGIA – SUPERFÍCIE INUNDÁVEL – ÁREA DE RISCO DE INUNDAÇÃO – INTERPRETAÇÃO DO TERMO “PREDOMINANTEMENTE” – CRITÉRIO ECONÔMICO-FUNCIONAL – REEXAME NECESSÁRIO – MANUTENÇÃO DA DECISÃO “A QUO”.`**\n\n")
        f.write("**Teses Normativas Paradigmáticas:**\n")
        f.write("- Para a aplicação do fator de correção pedológico relativo a terreno inundável ou em área de risco de inundação, adota-se o critério econômico-funcional: a restrição severa de ocupação imposta pelo poder público sobre fração substancial do lote basta para atrair a incidência do redutor de base de cálculo.\n")
        f.write("- A aplicação de fator corretivo decorrente de superveniente comprovação de risco geológico ou hidrológico atinge os lançamentos não decaídos, desde que não implique inovação de critério jurídico vedada pelo art. 146 do CTN.\n\n")
        f.write("**Acórdãos Precedentes Relevantes:**\n")
        for topics, meta in cat_theses["iptu_taxas"]["pedologia_inundabilidade"][:8]:
            f.write(f"- **Acórdão nº {meta['acordao']}** ({meta['camara']} – {meta['data']} – {meta['autor']})\n")
        f.write("\n---\n\n")

        # Tema 2: TFLF e Domicílio em Residência / Coworking
        f.write("## 2. Taxas: TFLF e Domicílio Tributário Eleito em Residência ou Coworking\n\n")
        f.write("**Verbetação Recomendada:**\n")
        f.write("> **`TFLF – TAXA DE FISCALIZAÇÃO DE LOCALIZAÇÃO E FUNCIONAMENTO – ELEIÇÃO DE DOMICÍLIO FISCAL EM RESIDÊNCIA – EXERCÍCIO DO PODER DE POLÍCIA – EFETIVIDADE DA FISCALIZAÇÃO MUNICIPAL – IRRELEVÂNCIA DE ATIVIDADE DECLARADA EM COWORKING – RECURSO VOLUNTÁRIO DESPROVIDO.`**\n\n")
        f.write("**Teses Normativas Paradigmáticas:**\n")
        f.write("- A Taxa de Fiscalização de Localização e Funcionamento (TFLF) é devida em razão do poder de polícia do Município sobre os estabelecimentos formalmente inscritos em seu cadastro mobiliário, sendo legítima sua exigência ainda que o contribuinte declare domicílio tributário formal em imóvel residencial.\n")
        f.write("- A alegação de utilização fática de espaços de coworking ou escritórios compartilhados não desonera o sujeito passivo da taxa quando este mantém seu domicílio fiscal formal registrado no endereço autuado perante a Receita Municipal.\n\n")
        f.write("**Acórdãos Precedentes Relevantes:**\n")
        for topics, meta in cat_theses["iptu_taxas"]["tflf_domicilio_coworking"][:8]:
            f.write(f"- **Acórdão nº {meta['acordao']}** ({meta['camara']} – {meta['data']} – {meta['autor']})\n")

    # 4. PROCESSUAL
    with open(os.path.join(OUT_DIR, "processual.md"), "w", encoding="utf-8") as f:
        f.write("# Catálogo de Teses-Paradigma: Processual Tributário e Agravos\n\n")
        f.write("Este repositório consolida as teses jurídicas processuais e de admissibilidade formuladas perante a Câmara de Presidentes e Câmaras Julgadoras do CRT-BH.\n\n---\n\n")
        
        # Tema 1: Agravos contra Despachos Denegatórios
        f.write("## 1. Agravos contra Despacho de Negativa de Seguimento de Impugnação\n\n")
        f.write("**Verbetação Recomendada:**\n")
        f.write("> **`AGRAVO – DESPACHO DE NEGATIVA DE SEGUIMENTO DE RECLAMAÇÃO ADMINISTRATIVA – TEMPESTIVIDADE – INTIMAÇÃO POR EDITAL – VÍCIO FORMAL – FALTA DE ESGOTAMENTO DOS MEIOS ELETRÔNICOS E PESSOAIS (DECORT-BH) – ART. 21 DA LEI MUNICIPAL Nº 1.310/1966 – DESTRANCAMENTO DA RECLAMAÇÃO – AGRAVO CONHECIDO E PROVIDO.`**\n\n")
        f.write("**Teses Normativas Paradigmáticas:**\n")
        f.write("- A notificação editalícia de lançamento ou termo fiscal possui caráter estritamente subsidiário e pressupõe o inequívoco esgotamento prévio das modalidades eletrônica (DECORT-BH) e postal com aviso de recebimento no domicílio fiscal cadastrado do contribuinte.\n")
        f.write("- O julgamento do Agravo perante a Câmara de Presidentes restringe-se à verificação dos pressupostos formais de admissibilidade da peça reclamatória originária, sendo vedado avançar no mérito da relação jurídica tributária, determinando-se a remessa dos autos à 1ª Instância (JJT) para regular processamento e julgamento.\n\n")
        f.write("**Acórdãos Precedentes Relevantes:**\n")
        for topics, meta in cat_theses["processual"]["agravos_notificacoes_defesas"][:8]:
            f.write(f"- **Acórdão nº {meta['acordao']}** ({meta['camara']} – {meta['data']} – {meta['autor']})\n")

    print(f"\n✅ Catálogos de teses-paradigma gerados com sucesso em {OUT_DIR}!")

if __name__ == "__main__":
    main()
