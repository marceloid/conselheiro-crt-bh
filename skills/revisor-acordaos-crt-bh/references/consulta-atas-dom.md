# Procedimento de Consulta de Atas e Pautas no DOM (Diário Oficial do Município)

Este guia define o procedimento operacional e a API para consulta automática de publicações de atas, pautas, sorteios e intimações de processos do CRT no **Diário Oficial do Município de Belo Horizonte (DOM)** (`https://dom-web.pbh.gov.br`).

A consulta ao DOM é parte fundamental da conferência realizada pela Secretaria e Presidência para validação das datas, do quórum, das suspensões e da fidelidade da **Certidão de Julgamento** e do **Acórdão**.

---

## 1. Especificação da API REST do DOM (PBH)

A aplicação web do DOM consome uma API REST pública no domínio `https://api-dom.pbh.gov.br`.

* **Base URL:** `https://api-dom.pbh.gov.br/api`
* **Headers Obrigatórios:**
  * `User-Agent`: Qualquer User-Agent de navegador moderno (ex.: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...`). *Nota: requisições sem User-Agent válido podem ser bloqueadas pelo CDN (GoCache).*
  * `Accept`: `application/json, text/plain, */*`

---

## 2. Endpoints Principais

### A. Pesquisa de Atos por Processo ou Termo
Permite localizar todos os atos e atas publicados que mencionam um determinado número de processo.

* **Método:** `GET`
* **URL:** `https://api-dom.pbh.gov.br/api/v1/edicoes/atos/pesquisar`
* **Parâmetros de Query:**

| Parâmetro | Tipo | Descrição / Valor Padrão |
|---|---|---|
| `termo` | string | Número do processo (ex.: `01.169550.14.08` ou `31.00188020/2023-04`) |
| `pesquisa_exata` | boolean | `false` (permite encontrar mesmo com variações de pontuação) ou `true` |
| `documentos[]` | array | `A` (Atos) e/ou `AA` (Anexos de Atos) |
| `local_pesquisa[]` | array | `T` (Título) e `C` (Conteúdo do ato) |
| `paginacao[pagina]` | integer | Página da pesquisa (padrão: `1`) |
| `paginacao[itens_por_pagina]` | integer | Quantidade de itens por página (ex.: `20`) |

#### Exemplo de Requisição:
```http
GET https://api-dom.pbh.gov.br/api/v1/edicoes/atos/pesquisar?termo=01.169550.14.08&pesquisa_exata=false&documentos[]=A&documentos[]=AA&local_pesquisa[]=T&local_pesquisa[]=C HTTP/1.1
Host: api-dom.pbh.gov.br
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36
```

#### Estrutura da Resposta:
A API retorna um objeto Elasticsearch com os `hits` encontrados:
* `_source.edicao.numero_edicao`: Número da edição do DOM (ex.: `7459`).
* `_source.edicao.dt_hr_publicacao`: Data e hora da publicação (ex.: `"2026-03-14 00:01"`).
* `_source.ato.titulo_ato`: Título do ato (ex.: `"CONSELHO DE RECURSOS TRIBUTÁRIOS - 3ª CÂMARA - ATA DE 05/03/2026 - PAUTA DE 23/04/2026"`).
* `_source.documento_ato.nome_minio`: Hash do arquivo armazenado no MinIO.
* `_source.documento_ato.prefix`: Prefixo da data no MinIO (ex.: `"20260313"`).
* `_source.documento_ato.extensao`: Extensão do arquivo (`html` ou `pdf`).

---

### B. Download / Obtenção do Conteúdo HTML do Ato
Recupera a íntegra do texto publicado no diário para conferência detalhada.

* **Método:** `GET`
* **URL:** `https://api-dom.pbh.gov.br/api/v1/documentos/{nome_minio}?prefix={prefix}`

#### Exemplo:
```http
GET https://api-dom.pbh.gov.br/api/v1/documentos/924d1d5070d4cae3a45772d658c2680c004472349cc7618be07e88a0f0b9d777?prefix=20260313 HTTP/1.1
Host: api-dom.pbh.gov.br
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36
```

---

## 3. Roteiro de Conferência Cruzada com o DOM

Ao revisar um acórdão do CRT, execute a consulta do processo no DOM para validar os 4 marcos cronológicos obrigatórios da **Certidão de Julgamento**:

1. **Data do Sorteio**:
   - Localize a ata da sessão em que o processo foi distribuído/sorteado ao Relator.
   - *Verificar na Certidão:* `Sorteado ao Relator, Conselheiro [Nome], em DD/MM/AAAA...`
2. **Inclusão em Pauta**:
   - Localize a pauta publicada no DOM que designou a data do julgamento.
   - *Verificar na Certidão:* `...e incluído na pauta do dia DD/MM/AAAA.`
3. **Suspensões / Vistas / Retiradas de Pauta**:
   - Localize as atas intermediárias que registraram eventuais pedidos de vista/reanálise, conversões em diligência ou adiamentos/retiradas de pauta a pedido da parte.
   - *Verificar na Certidão:* `Julgamento suspenso em DD/MM/AAAA, em razão de pedido de vista...` ou `Retirado de pauta, a pedido da Recorrente...`
4. **Sessão de Julgamento / Proclamação do Resultado**:
   - Localize a ata da sessão de julgamento e confronte:
     - **Data da conclusão**: Confirmação da data da sessão.
     - **Presidente da Sessão**: Quem presidiu o julgamento.
     - **Conselheiros Presentes e Ordem de Votação**: Comparar com os nomes no Acórdão e Certidão.
     - **Quórum**: Se foi unânime, por maioria ou por voto de qualidade.
     - **Sustentação Oral e Advogados Presentes**: Nome exato e OAB de quem sustentou oralmente ou assistiu aos trabalhos.
     - **Número do Acórdão**: Conferir se o número coincide com a proclamação oficial (ex.: `Acórdão nº 11.618/3ª`).

---

## 4. Script Utilitário para Consulta Rápida (Node.js)

```javascript
async function consultarAtasProcesso(numeroProcesso) {
  const params = new URLSearchParams();
  params.append("termo", numeroProcesso);
  params.append("pesquisa_exata", "false");
  params.append("documentos[]", "A");
  params.append("documentos[]", "AA");
  params.append("local_pesquisa[]", "T");
  params.append("local_pesquisa[]", "C");

  const url = `https://api-dom.pbh.gov.br/api/v1/edicoes/atos/pesquisar?${params.toString()}`;
  const res = await fetch(url, {
    headers: {
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
      "Accept": "application/json"
    }
  });

  const json = await res.json();
  const hits = json.data?.hits?.hits || [];

  console.log(`Encontrados ${hits.length} atos para o processo ${numeroProcesso}:`);
  for (const h of hits) {
    const src = h._source;
    console.log(`- DOM ${src.edicao.numero_edicao} (${src.edicao.dt_hr_publicacao}): ${src.ato.titulo_ato}`);
  }
}
```
