# 🏛️ Toolkit do CRT-BH: Skills para o Conselho de Recursos Tributários de Belo Horizonte

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Type](https://img.shields.io/badge/type-Agentic--AI--Skills-emerald.svg)

Repositório monorepo contendo as agent skills especializadas em direito processual tributário municipal para atuação perante o **Conselho de Recursos Tributários de Belo Horizonte (CRT / CART-BH)**.

---

## 📦 Skills Disponíveis

| Skill | Escopo / Papel | Descrição Resumida |
|---|---|---|
| **[`conselheiro-do-crt-bh`](skills/conselheiro-do-crt-bh)** | Assessor Judicante | Elaboração de relatórios, votos e ementas para Agravos contra despachos denegatórios, Admissibilidade de Recurso Especial (REsp) e Recursos de Plenário/Câmaras. Redação em primeira pessoa com zero meta-linguagem. |
| **[`revisor-acordaos-crt-bh`](skills/revisor-acordaos-crt-bh)** | Presidência e Secretaria | Auditoria formal, controle de qualidade, padronização estrita de siglas/legislação/processos, validação de ementas e aplicação de sugestões rastreadas (*redlining*) em acórdãos e minutas já lavrados. |

---

## 📁 Estrutura do Repositório

```
conselheiro-crt-bh/
├── README.md
├── LICENSE
└── skills/
    ├── conselheiro-do-crt-bh/                   # Skill 1: Atividade Judicante de Relatoria
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── elaboracao-minuta-agravo.md
    │   │   ├── analise-admissibilidade-recurso-especial.md
    │   │   ├── pesquisa-jurisprudencial-jusratio.md
    │   │   ├── agravo-negativa-seguimento.md
    │   │   ├── recurso-especial.md
    │   │   ├── recurso-voluntario.md
    │   │   └── legislacao.md
    │   └── templates/
    │       └── modelo-agravo.docx
    │
    └── revisor-acordaos-crt-bh/                 # Skill 2: Atividade Administrativa / Presidência
        ├── SKILL.md
        └── references/
            ├── checklist-padronizacao.md        # Siglas, CTM/CTN, Processos, Transcrição JJT
            ├── criterios-validacao-ementa.md   # Validação de ementas vs. voto condutor
            └── pipeline-redlining-gdocs.md      # Redlining Word/XML e Google Docs
```

---

## ⚙️ Instalação nos Agentes de IA

### Via Catálogo Central (`my-agent-skills`)

No arquivo `skills.json` do seu repositório de skills, aponte cada skill para sua respectiva subpasta:

```json
{
  "name": "conselheiro-do-crt-bh",
  "group": "pbh",
  "summary": "Orientação jurídica, elaboração de minutas de relatórios, votos e ementas para o CRT-BH.",
  "repo": "https://github.com/marceloid/conselheiro-crt-bh.git",
  "path": "skills/conselheiro-do-crt-bh",
  "owner": "self",
  "update": "ff"
},
{
  "name": "revisor-acordaos-crt-bh",
  "group": "pbh",
  "summary": "Revisão, auditoria formal, padronização e validação de minutas e acórdãos do CRT-BH em modo sugestão.",
  "repo": "https://github.com/marceloid/conselheiro-crt-bh.git",
  "path": "skills/revisor-acordaos-crt-bh",
  "owner": "self",
  "update": "ff"
}
```

---

## ⚖️ Licença

Distribuído sob a licença [MIT](LICENSE).
