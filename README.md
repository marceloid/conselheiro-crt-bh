# 🏛️ Skill: Conselheiro do CRT-BH

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Type](https://img.shields.io/badge/type-Agentic--AI--Skill-emerald.svg)

Skill especializada em direito tributário municipal para atuar como **Assessor Jurídico de Conselheiro Relator** no **Conselho de Recursos Tributários de Belo Horizonte (CRT-BH)**.

---

## 📌 Visão Geral

Esta skill instrui assistentes de IA (como Google Antigravity, Claude, ChatGPT ou outros agentes baseados no ecossistema de agentic coding) a elaborar minutas de decisões administrativas tributárias municipais em segunda instância no município de Belo Horizonte/MG.

### Peças Suportadas:
1. **Agravo contra Despacho de Negativa de Seguimento** (Câmara de Presidentes)
   - **Relatório**: Histórico processual, dados de notificação, fatos da controvérsia, fundamentação do despacho denegatório e razões do agravante.
   - **Voto**: Análise da tempestividade, legitimidade, delimitação de escopo, instrumentalidade das formas (CPC/CTN) e julgamento de mérito (ITBI / IPTU).
   - **Ementa**: Síntese padronizada com cabeçalho em caixa alta e dispositivos aplicados.

2. **Recurso Especial** (Câmara Especial de Recursos - CER)
   - **Relatório**: Confronto sintético entre o acórdão recorrido e o acórdão paradigma, análise de admissibilidade e síntese da manifestação da DFAT/Fisco.
   - **Voto**: Análise da divergência jurisprudencial sobre aplicação da legislação tributária e fixação/uniformização da tese.
   - **Ementa**: Estrutura oficial para acórdão da CER.

---

## 🛠️ Como Utilizar

### Estrutura de Arquivos

```
.
├── SKILL.md      # Instruções e diretrizes da skill
├── README.md     # Documentação do repositório
└── LICENSE       # Licença MIT
```

### Instalação no Antigravity / Gemini / Claude

Basta incluir este repositório ou copiar o arquivo [`SKILL.md`](SKILL.md) para o diretório de skills do seu ambiente de IA:

- **Antigravity CLI / IDE**: Adicione o diretório ou copie para `~/.gemini/antigravity/skills/conselheiro-crt-bh/SKILL.md` ou na pasta de skills do seu projeto.
- **Claude / Custom GPTs**: Copie o conteúdo de [`SKILL.md`](SKILL.md) para as instruções do sistema ou prompt da persona.

---

## ⚖️ Legislação e Fundamentação de Referência

| Norma / Fonte | Aplicação |
|---|---|
| **Lei Municipal nº 1.310/1966 (CTM)** | Art. 106, I (prazo de 30 dias para impugnação de IPTU); art. 336 (aplicação subsidiária do CPC). |
| **CTN (Lei nº 5.172/1966)** | Art. 168, I (restituição de indébito - 5 anos); Art. 173 (decadência do Fisco); Art. 149 (revisão de ofício). |
| **Decreto Municipal nº 19.460/2026** | Regulamento do CART-BH (vigente). |
| **Decretos nº 18.783/2024 e 18.716/2024** | Regulamentos do CART-BH (anteriores). |
| **Decretos nº 17.026/2018 / 17.206/2018** | Regulamento do ITBI em Belo Horizonte. |
| **CPC (Lei nº 13.105/2015)** | Arts. 188, 277 e 322, § 2º (Princípio da Instrumentalidade das Formas). |
| **STJ — Tema Repetitivo 1.113** | Base de cálculo do ITBI (REsp 1.937.821/SP). |

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
