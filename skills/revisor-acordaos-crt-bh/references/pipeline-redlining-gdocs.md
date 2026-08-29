# Pipeline Técnico de Redlining (Modo Sugestão) no Word e Google Docs

Este guia descreve os requisitos técnicos para manipulação de arquivos `.docx` em modo de revisão rastreada e sincronização com o Google Drive/Docs.

---

## 1. Regras de OpenXML para Sugestões (Tracked Changes) e Comentários

Em arquivos Word (`.docx`), revisões e sugestões são representadas pelos elementos `<w:del>` (exclusão) e `<w:ins>` (inserção), e **devem ser acompanhadas de comentários (`<w:comment>`) com a respectiva justificativa**.

### Estrutura de Injeção XML com Comentário de Justificativa

Para sugerir a substituição de um texto `antigo` por `novo` acompanhado de comentário justificativo:

```xml
<w:commentRangeStart w:id="1"/>
<w:del w:id="101" w:author="Revisor CRT-BH" w:date="2026-08-20T10:00:00Z">
  <w:r>
    <w:rPr>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
    <w:delText xml:space="preserve">antigo</w:delText>
  </w:r>
</w:del>
<w:ins w:id="102" w:author="Revisor CRT-BH" w:date="2026-08-20T10:00:00Z">
  <w:r>
    <w:rPr>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
    <w:t xml:space="preserve">novo</w:t>
  </w:r>
</w:ins>
<w:commentRangeEnd w:id="1"/>
<w:r>
  <w:rPr>
    <w:rStyle w:val="CommentReference"/>
  </w:rPr>
  <w:commentReference w:id="1"/>
</w:r>
```

### Estrutura do Arquivo `word/comments.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:comments xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
            xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:comment w:id="1" w:author="Revisor CRT-BH" w:date="2026-08-20T10:00:00Z" w:initials="CRT">
    <w:p>
      <w:pPr>
        <w:pStyle w:val="CommentText"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rStyle w:val="CommentReference"/>
        </w:rPr>
        <w:annotationRef/>
      </w:r>
      <w:r>
        <w:t xml:space="preserve">Correção ortográfica e padronização institucional da sigla (CRT).</w:t>
      </w:r>
    </w:p>
  </w:comment>
</w:comments>
```

### Pontos Críticos do Esquema XML:
1. **Unicidade de IDs**: Cada `<w:del>`, `<w:ins>` e `<w:comment>` deve possuir um atributo `w:id` numérico e globalmente único no documento.
2. **Atributo do Autor**: `w:author` deve conter o nome do revisor (ex.: `"Revisor CRT-BH"` ou nome do usuário).
3. **Atributo de Data**: `w:date` em formato ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`).
4. **Elemento de Texto Excluído**: Dentro de `<w:del><w:r>`, usa-se `<w:delText>`, **nunca** `<w:t>`.
5. **Comentários Obrigatórios em 100% das Sugestões**: Toda alteração inserida deve ter seu comentário correspondente em `word/comments.xml` justificando o motivo da intervenção.
6. **Mapeamento de Relacionamentos e Content Types**:
   - `[Content_Types].xml`: deve conter `<Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>`.
   - `word/_rels/document.xml.rels`: deve conter `<Relationship Id="rIdComments" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/>`.
   - **Atenção aos Namespaces na Serialização**: Arquivos de pacote (`[Content_Types].xml` e `.rels`) não admitem prefixos (`ns0:`), devendo usar `xmlns` padrão. O `document.xml` deve manter o prefixo `xmlns:w="..."`.

---

## 2. Validação com `validate.py`

Antes de reempacotar qualquer arquivo modificado, execute sempre o validador da skill `docx`:

```bash
python3 /caminho/para/docx/scripts/office/validate.py output.docx --original original.docx --author "Nome do Usuário"
```

A flag `--author` valida se **100% das alterações de texto** foram envelopadas em tags `<w:del>`/`<w:ins>` e que nenhuma alteração não rastreada ocorreu.

---

## 3. Sincronização com Google Drive / Google Docs

### Download de Arquivo do Drive
Quando o documento é um `.docx` hospedado no Google Drive:
- Utilize a Drive API v3: `GET https://www.googleapis.com/drive/v3/files/{fileId}?alt=media&supportsAllDrives=true`
- Salve localmente como `.docx`.

### Upload / Atualização em Lugar (In-Place Update)
Para atualizar o documento no Google Drive preservando o mesmo ID de arquivo:
- Utilize a Drive API v3 via método `PATCH`:
  ```http
  PATCH https://www.googleapis.com/upload/drive/v3/files/{fileId}?uploadType=media&supportsAllDrives=true
  Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
  Authorization: Bearer {token}
  ```
- O Google Docs atualizará a visualização imediatamente e exibirá os balões de sugestão na margem direita com a autoria configurada.
