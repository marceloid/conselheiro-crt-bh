# 🏛️ Skill: Conselheiro do CRT-BH

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Type](https://img.shields.io/badge/type-Agentic--AI--Skill-emerald.svg)

Skill especializada em direito tributário municipal para atuar como **Assessor Jurídico de Conselheiro Relator** no **Conselho de Recursos Tributários de Belo Horizonte (CRT-BH)**.

---

## 📌 Visão Geral e Arquitetura Modular

Esta skill possui uma arquitetura modular baseada em um arquivo orquestrador geral (`SKILL.md`) e arquivos de procedimentos específicos localizados no diretório `references/`:

```
.
├── SKILL.md                                           # Orquestrador geral, persona, regras de estilo e roteamento
├── README.md                                          # Documentação do repositório
├── LICENSE                                            # Licença MIT
├── .gitignore
└── references/
    ├── elaboracao-minuta-agravo.md                    # Procedimento para minuta de Agravo
    └── analise-admissibilidade-recurso-especial.md    # Procedimento para análise de admissibilidade de REsp
```

---

## 📜 Procedimentos Suportados

1. **[Agravo contra Despacho de Negativa de Seguimento](references/elaboracao-minuta-agravo.md)**:
   - **Relatório**: Histórico processual, fatos da controvérsia, fundamentação do despacho denegatório e razões do recurso.
   - **Voto**: Delimitação de escopo (cognição estrita), tempestividade/legitimidade, instrumentalidade das formas (CPC/CTN) e julgamento de mérito (ITBI / IPTU).
   - **Ementa**: Síntese padronizada em caixa alta e dispositivos aplicados.

2. **[Análise de Admissibilidade de Recurso Especial - REsp](references/analise-admissibilidade-recurso-especial.md)**:
   - **Formato Colegiado (Decreto nº 19.460/2026)**: Julgamento pela Câmara de Presidentes resultando em Acórdão de Admissibilidade composto por **Relatório, Voto e Ementa**.
   - **Requisitos**: Confronto analítico de divergência jurisprudencial, acórdão paradigma irrecorrível, tempestividade (15 dias), vedações a reexame de provas (art. 78, § 3º) e confronto com súmulas.

---

## 🛠️ Como Instalar nos Agentes de IA

### 1. Instalação Centralizada no Hub de Skills (`~/.agents/skills`)

Recomendamos clonar o repositório no seu repositório central de skills:

```bash
git clone https://github.com/marceloid/conselheiro-crt-bh.git ~/.agents/skills/conselheiro-do-crt-bh
```

A partir daí, você pode criar links simbólicos (symlinks) para os agentes desejados:

---

### 2. Google Antigravity (`~/.gemini/antigravity/skills`)

Para disponibilizar a skill globalmente no Antigravity:

```bash
mkdir -p ~/.gemini/antigravity/skills
ln -s ~/.agents/skills/conselheiro-do-crt-bh ~/.gemini/antigravity/skills/conselheiro-do-crt-bh
```

*Ou diretamente no repositório de trabalho:*
```bash
ln -s ~/.agents/skills/conselheiro-do-crt-bh ./skills/conselheiro-do-crt-bh
```

---

### 3. Claude Code / Claude CLI (`~/.claude/skills`)

Para vincular a skill ao Claude Code:

```bash
mkdir -p ~/.claude/skills
ln -s ~/.agents/skills/conselheiro-do-crt-bh ~/.claude/skills/conselheiro-do-crt-bh
```

---

### 4. Pi Agent (`~/.pi/agent/skills`)

Para disponibilizar a skill no Pi Agent:

```bash
mkdir -p ~/.pi/agent/skills
ln -s ~/.agents/skills/conselheiro-do-crt-bh ~/.pi/agent/skills/conselheiro-do-crt-bh
```

---

### 5. OpenCode (`~/.config/opencode/skills` ou `~/.opencode/skills`)

Para instalar no OpenCode:

```bash
mkdir -p ~/.config/opencode/skills
ln -s ~/.agents/skills/conselheiro-do-crt-bh ~/.config/opencode/skills/conselheiro-do-crt-bh
```

---

## ⚖️ Legislação de Referência

| Norma / Fonte | Aplicação |
|---|---|
| **Lei Municipal nº 1.310/1966 (CTM)** | Art. 106, I (prazo de 30 dias para impugnação de IPTU); art. 336 (aplicação subsidiária do CPC). |
| **CTN (Lei nº 5.172/1966)** | Art. 168, I (restituição de indébito - 5 anos); Art. 173 (decadência do Fisco); Art. 149 (revisão de ofício). |
| **Decreto Municipal nº 19.460/2026** | Regulamento do CART-BH (vigente). Arts. 71, 78 a 81. |
| **Decretos nº 18.783/2024 e 18.716/2024** | Regulamentos anteriores do CART-BH. |
| **Decretos nº 17.026/2018 / 17.206/2018** | Regulamento do ITBI em Belo Horizonte. |
| **CPC (Lei nº 13.105/2015)** | Arts. 188, 277 e 322, § 2º (Princípio da Instrumentalidade das Formas). |
| **STJ — Tema Repetitivo 1.113** | Base de cálculo do ITBI (REsp 1.937.821/SP). |

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
