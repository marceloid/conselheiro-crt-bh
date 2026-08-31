# Procedimento: Análise de Admissibilidade de Recurso Especial (REsp)

Este procedimento orienta a elaboração de minutas para a **Análise de Admissibilidade de Recurso Especial (REsp)** julgado perante o Conselho de Recursos Tributários de Belo Horizonte (CRT-BH).

> **Atenção — Sigla Padrão**: Utilize exclusivamente a sigla **REsp** para se referir ao Recurso Especial.

---

## 1. Regime de Julgamento da Admissibilidade

### A. Sob a Regência do Decreto Municipal nº 19.460/2026 (Regulamento Vigente)
- **Natureza do Julgamento**: Julgamento **colegiado** realizado pela **Câmara de Presidentes** do CRT-BH. Nunca é decisão monocrática.
- **Forma do Ato**: Acórdão de Admissibilidade.
- **Peças a Redigir**: As minutas devem ser compostas por **Relatório, Voto e Ementa** direcionados especificamente ao exame do cabimento e admissibilidade do REsp.

### B. Sob a Regência de Regulamentos Anteriores (ex: Decreto nº 18.783/2024 e anteriores)
- **Natureza do Julgamento**: Decisão monocrática exarada pelo Presidente da Câmara de Julgamento que proferiu o acórdão recorrido (art. 68 do regulamento anterior).
- **Forma do Ato**: Despacho de Admissibilidade (Positivo ou Negativo).

---

## 2. Fluxo Operacional de Análise e Obtenção dos Acórdãos

Quando o usuário iniciar a demanda indicando a necessidade de análise de admissibilidade de REsp:

### Passo 1: Obtenção dos Documentos e Download Automático
- Se o usuário não anexar ou fornecer a íntegra dos acórdãos (recorrido e paradigma), o agente deve obtê-los diretamente do repositório oficial do CART-BH.
- **Padrão da URL**: `https://fazenda.pbh.gov.br/cart/acordao/AC{NUMERO_SEM_PONTUACAO}.pdf`
  - *Exemplo*: para o Acórdão nº 10.018, a URL é `https://fazenda.pbh.gov.br/cart/acordao/AC10018.pdf`; para o Acórdão nº 9.876, a URL é `https://fazenda.pbh.gov.br/cart/acordao/AC9876.pdf`.
- **Requisito Técnico de Download (WAF/CDN GoCache)**:
  - O portal da Fazenda PBH é protegido por GoCache. Toda requisição HTTP/curl deve obrigatoriamente incluir um cabeçalho `User-Agent` de navegador (ex.: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36`) para evitar bloqueio por HTTP 403 Forbidden.

### Passo 2: Extração e Resumo dos Acórdãos (Gate de Validação Obrigatório)
Após a leitura e extração do inteiro teor dos acórdãos, **o agente DEVE apresentar ao usuário um resumo estruturado de cada acórdão e a análise preliminar da divergência antes de redigir qualquer minuta definitiva**.

O resumo para validação deve conter os seguintes tópicos:

1. **Resumo do Acórdão Recorrido**:
   - **Identificação**: Número do Acórdão, Câmara Julgadora, Relator(a), PTA/Processo e Data do Julgamento.
   - **Moldura Fática e Tributo**: Situação concreta analisada e tributo em discussão.
   - **Tese Jurídica Adotada (*Ratio Decidendi*)**: Interpretação conferida à legislação municipal de regência.
   - **Dispositivo**: Resultado do julgamento na origem.

2. **Resumo do Acórdão Paradigma**:
   - **Identificação**: Número do Acórdão, Câmara Julgadora, Relator(a), PTA/Processo e Data do Julgamento.
   - **Moldura Fática e Tributo**: Situação concreta analisada e tributo em discussão.
   - **Tese Jurídica Adotada (*Ratio Decidendi*)**: Interpretação conferida à legislação municipal de regência.
   - **Dispositivo**: Resultado do julgamento paradigma.

3. **Cotejo Analítico Preliminar da Divergência**:
   - **Similitude Fática**: Demonstração de que ambos os acórdãos versam sobre a mesma hipótese/premissa fática.
   - **Dissenso Jurídico**: Ponto exato de divergência quanto à aplicação da norma tributária municipal.
   - **Verificação de Vedações**: Checagem quanto ao reexame fático-probatório (art. 78, § 3º) ou contrariedade a súmula da CER (art. 78, § 4º).
   - **Conclusão Preliminar**: Indicação técnica preliminar sobre o cabimento (conhecimento/admissibilidade ou não conhecimento).

> **Aguardar Validação**: O agente deve submeter essa estrutura para que o Conselheiro/usuário valide as premissas e a tese antes de iniciar a redação do Relatório, Voto e Ementa.

---

## 3. Requisitos Formais e Substanciais de Admissibilidade do REsp

A análise de admissibilidade do REsp deve verificar rigorosamente os seguintes requisitos:

1. **Cabimento e Divergência Jurisprudencial Demonstrada** (art. 78 do Decreto nº 19.460/2026):
   - Cabível contra acórdão de Câmara de Julgamento que divergir de acórdão irrecorrível proferido pela mesma ou por outra Câmara, quanto à aplicação da legislação tributária municipal.
   - Exige a confrontação analítica das teses em confronto.
2. **Comprovação do Acórdão Paradigma** (art. 78, § 1º):
   - Necessidade de juntada de cópia do acórdão paradigma irrecorrível e indicação precisa da divergência.
3. **Tempestividade** (art. 78, § 2º):
   - Prazo de 15 (quinze) dias contados da publicação do acórdão recorrido no Diário Oficial do Município (DOM). O recurso possui efeito suspensivo.
4. **Legitimidade e Representação**:
   - Verificação de legitimidade recursal e juntada de instrumento de procuração com poderes específicos.
5. **Vedações Expressas de Admissibilidade**:
   - **Vedação ao Reexame de Provas** (art. 78, § 3º): É vedado o REsp que pretenda o simples reexame de fatos e provas. Se o recorrente buscar rediscutir o conjunto probatório sob o rótulo de divergência jurídica, o recurso **não deve ser conhecido**.
   - **Vedação em Face de Súmula** (art. 78, § 4º): Não cabe REsp em face de súmula da CER ou de decisão fundada em súmula vigente à época da prolação do acórdão recorrido.

---

## 4. Estrutura das Peças de Admissibilidade (Decreto nº 19.460/2026)

### PEÇA 1 — Relatório de Admissibilidade do REsp

**Abertura Padrão**:
> "Versam os autos sobre Recurso Especial (REsp) interposto em [DATA], por meio do [PROCESSO BH DIGITAL Nº / ou sem referência se não houver], por [NOME EM MAIÚSCULAS], contra o Acórdão nº [Nº] proferido pela [CÂMARA DE ORIGEM] do CRT-BH, nos autos do processo administrativo nº [Nº], em razão de alegada divergência jurisprudencial com o Acórdão nº [Nº PARADIGMA], proferido pela [CÂMARA PARADIGMA]."

**Estrutura do Conteúdo**:
1. **Identificação**: Data de interposição do REsp, processo BH Digital, nome da parte em maiúsculas, número e câmara do acórdão recorrido e do processo original.
2. **Síntese da Matéria Decidida no Acórdão Recorrido**: Resumo do entendimento adotado pela Câmara de Julgamento de origem.
3. **Razões do REsp e Acórdão Paradigma Invocado**: Tese defendida pelo recorrente, indicação do acórdão paradigma (número e câmara) e o ponto exato de divergência alegado na aplicação da legislação tributária.
4. **Tempestividade e Dados de Intimação**: Registrar a data de publicação do acórdão recorrido no DOM e a data do protocolo do REsp.
5. **Manifestação da Parte Recorrida / Contrarrazões**: Registrar expressamente se a parte contrária (Fisco ou Contribuinte) apresentou contrarrazões ao REsp ou se decorreu *in albis* / não se manifestou (ex.: *"Devidamente intimado/a para se manifestar, o/a Recorrido/a não apresentou contrarrazões, decorrendo in albis o prazo regulamentar."* ou *"O/A Recorrido/a apresentou contrarrazões no Ato X, pugnando pela manutenção do acórdão recorrido."*).
6. **Encerramento**: **"É o relatório."**

---

### PEÇA 2 — Voto de Admissibilidade do REsp (Câmara de Presidentes)

**Abertura Padrão**:
> "Versam os autos sobre exame de admissibilidade de Recurso Especial (REsp) interposto por [NOME], contra o Acórdão nº [Nº] proferido pela [CÂMARA DE ORIGEM] do CRT-BH, por alegada divergência com o Acórdão nº [Nº PARADIGMA] quanto a [matéria da divergência]."

**Tópicos Obrigatórios do Voto**:

1. **Da Tempestividade, Legitimidade e Representação**:
   - Demonstrar o cumprimento do prazo de 15 dias (art. 78, § 2º, Decreto nº 19.460/2026).
   - Verificar legitimidade e regularidade da representação processual.

2. **Do Exame da Divergência Jurisprudencial e Cabimento**:
   - Confrontar objetivamente a tese do acórdão recorrido com a do acórdão paradigma.
   - Verificar se há efetiva divergência de interpretação da legislação tributária municipal sobre a mesma premissa de fato.

3. **Verificação de Vedações Expressas**:
   - Demonstrar se o recurso envolve ou não reexame de matéria fático-probatória (art. 78, § 3º). Se envolver: "Constatado que a pretensão do Recorrente exige o reexame do conjunto fático-probatório dos autos, incide a vedação expressa do art. 78, § 3º, do Regulamento do CART-BH, impondo-se o não conhecimento do REsp."
   - Verificar ausência de confronto com súmula da CER (art. 78, § 4º).

4. **Conclusão e Dispositivo do Voto**:
   - *Se Admitido (Conhecido)*:
     > "Por todo o exposto, voto pelo **CONHECIMENTO e ADMISSIBILIDADE** do presente Recurso Especial (REsp), determinando a distribuição dos autos à Câmara Especial de Recursos (CER) para julgamento do mérito, na forma do art. 79 do Decreto nº 19.460/2026."
   - *Se Não Admitido (Não Conhecido)*:
     > "Por todo o exposto, voto pelo **NÃO CONHECIMENTO** do presente Recurso Especial (REsp), ante [a ausência de divergência jurisprudencial / a vedação ao reexame de provas do art. 78, § 3º / a intempestividade], mantendo-se a irrecorribilidade do Acórdão nº [Nº]."

---

### PEÇA 3 — Ementa do Acórdão de Admissibilidade do REsp

**Modelo de Cabeçalho**:
> RECURSO ESPECIAL (RESP). ADMISSIBILIDADE. CÂMARA DE PRESIDENTES. DIVERGÊNCIA JURISPRUDENCIAL [CONFIGURADA / NÃO CONFIGURADA]. [MATÉRIA TRIBUTÁRIA]. [INCIDÊNCIA OU NÃO DE VEDAÇÃO RECURSAL]. RECURSO [CONHECIDO E ADMITIDO / NÃO CONHECIDO].

---

## 5. Reserva para Expansão Futura

> 📌 **Nota de Arquitetura**: A análise de mérito do REsp admitido (julgamento pela Câmara Especial de Recursos — CER) será regulada em procedimento próprio no arquivo `references/analise-merito-recurso-especial.md`.
