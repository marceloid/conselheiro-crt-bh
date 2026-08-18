# Procedimento: Pesquisa Jurisprudencial com JusRatio (JusMCP)

Este procedimento orienta a **pesquisa jurisprudencial prévia** na base JusRatio antes de redigir qualquer minuta (agavo, REsp) e o **gate de validação de precedentes** — nenhum julgado entra no voto sem que o Relator tenha visto ementa e inteiro teor.

---

## 1. Verificação Prévia da Conexão (OBRIGATÓRIA)

Antes de qualquer pesquisa, confirme que o servidor JusMCP está acessível:

1. **Preferencial — MCP conectado**: tente listar tribunais com a ferramenta MCP (`mcp__jusratio__listar_tribunais`). Se responder, use as ferramentas MCP nativas: `pesquisar_documentos` → `obter_resultado_pesquisa` → `obter_documento` / `obter_documento_chunk`.
2. **Fallback — API HTTP direta**: se o MCP não estiver conectado na sessão (ex.: acabou de ser configurado e requer restart), use a API REST stateless via `curl`:
   - `POST /search` (assíncrono → `job_id`) → poll `GET /result/{job_id}` até `status=done`
   - `GET /document/{doc_id}` — recupera o documento completo
   - Header: `Authorization: Bearer $MCP_JUSRATIO_API_KEY` (chave no `.env` do Hermes; variável `MCP_JUSRATIO_API_KEY`)
3. **Sem acesso de jeito nenhum**: informe o Relator e pergunte se deseja prosseguir sem pesquisa jurisprudencial ou aguardar.

> Ferramentas MCP nativas só aparecem no startup seguinte à configuração; o fallback HTTP cobre a sessão corrente.

---

## 2. Fluxo de Pesquisa (Eixos Temáticos)

1. **Antes de redigir**, monte 2–3 eixos de pesquisa a partir da controvérsia (ex.: "notificação presumida em domicílio eletrônico", "parcialidade da negativa de seguimento").
2. Registre a pesquisa na nota do processo (Obsidian) com data, eixos e julgados encontrados, **marcando qual entrou no voto**.
3. **Fluxo assíncrono**: `pesquisar_documentos` devolve `job_id`; repita `obter_resultado_pesquisa(job_id, wait_seconds=50)` até `status=done` (~1–2 min). Não insira sleeps manuais.
4. **Docs TJMG**: o campo `texto_busca` traz o texto integral (ementa + resto). Para outros tribunais pode vir só resumo; use `obter_documento_chunk` quando `total_chunks > 1`.

---

## 2.1 Portal TJMG (inteiro teor oficial)

O portal `www5.tjmg.jus.br` bloqueia a maioria das requisições automatizadas (406/reset). Quando funcionar, o endpoint retorna **PDF** (não HTML):

```bash
curl -s --http1.1 --max-time 30 \
  -A "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0" \
  -H "Accept: text/html" -H "Accept-Language: pt-BR,pt;q=0.9" \
  -c /tmp/tjmg_cookies.txt \
  -o saida.pdf \
  "https://www5.tjmg.jus.br/jurisprudencia/relatorioEspelhoAcordao.do?inteiroTeor=true&ano=22&ttriCodigo=1&codigoOrigem=0&numero=136906&sequencial=1&sequencialAcordao=0"
```

- Se falhar (HTTP 000/406), o texto integral está na base JusRatio (`texto_busca` do `obter_documento`).
- Para extrair texto do PDF: fitz/pymupdf (venv pdf-bench).
- **Anexar sempre ao vault**: `attachments/[Tribunal] [classe] [nº CNJ] - [Relator] - inteiro teor.pdf`.

---

## 2.2 Utilização do texto integral recuperado

- **Ementa verbatim**: sempre transcrever do `texto_busca` do JusRatio ou do PDF oficial — nunca redigir de memória.
- **Verificar o dispositivo**: localizar a frase de fechamento (ex.: "NEGARAM PROVIMENTO AO RECURSO") e os votos dos demais desembargadores — confere a realia do julgado.
- **Comparação 1:1**: antes de entregar a minuta, comparar programaticamente trechos-chave da ementa transcrita contra o inteiro teor (normalizando espaçamento/quebras de linha).

---

## 2.3 Gate de Validação de Precedentes (CRÍTICO)

**Nenhum julgado é citado no voto sem que o Relator tenha visto e aprovado a citação.** Fluxo:

1. **Recuperar o documento completo** (`obter_documento`) e apresentar ao Relator: bibliografia completa (tribunal, câmara, classe+CNJ, relator, datas j./DJe) + **ementa verbatim** + link/inteiro teor.
2. **Aguardar decisão expressa do Relator** (incluir / excluir / substituir / incluir com ressalva).
3. **Só então** aplicar o patch na minuta e na nota. A decisão fica registrada na seção de pesquisa da nota.
4. **Aprovação de síntese ≠ aprovação de ementa**: no AG 1094, o Relator aprovou a síntese mas pediu ementa verbatim no voto também. Confirmar ambas.

---

## 2.4 Checagens de Qualidade do Precedente

Antes de propor qualquer julgado ao Relator, verificar no payload do JusRatio:

1. **`tipo_decisorio`**: se `nao_merito` (óbice processual — ex.: AgInt que só confirma intempestividade), o julgado **não é citável como tese**; só como apoio, se tanto.
2. **`authority_level`**: priorize A/B (vinculantes, temas repetitivos) e C (órgão de cúpula). D = colegiado ordinário — citável, mas frágil sozinho.
3. **Superação temporal**: buscar se a tese foi superada por julgados mais recentes do mesmo tribunal/órgão (ex.: a linha "informações de páginas eletrônicas são meramente informativas" do STJ foi superada pela Corte Especial a partir de 2020 — EREsp 1.805.589/MT, AgInt nos EEREsp). Citar tese superada abre flanco.
4. **Analogia entre esferas**: precedente estadual (Lei 6.763/75, Dec. 44.747/08) aplicável ao regime municipal (Lei 1.310/1966) exige **ressalva expressa** de analogia no voto — "ainda que trate de legislação diversa, a disciplina é idêntica, aplicando-se o mesmo entendimento por analogia".

---

## 2.5 Padrões de Citação no Voto

- **CTN c/c CTM**: ao citar contagem/prorrogação de prazo do art. 210 do CTN, citar junto o **art. 327 da Lei nº 1.310/1966** (prazos contínuos; exclui o dia do começo, inclui o do votecimento; vencimento em feriado/domingo prorroga ao 1º dia útil) — análogo municipal do parágrafo único do art. 210.
- **Ementa no voto**: quando o Relator aprovar, transcrever a ementa verbatim **logo após o parágrafo citante**, com recuo (ex.: 1,25 cm) e a frase de abertura em negrito.

---

## 2.6 Pós-Julgamento (confirmação do resultado)

Após a sessão de julgamento, atualizar a nota com o resultado e **confirmar se o precedente citado foi mantido** pela câmara (ou se houve divergência que obrigue revisão da linha do voto em casos futuros).
