# Pipeline Técnico de Redlining (Modo Sugestão) no Word e Google Docs

Este guia descreve os requisitos técnicos para manipulação de arquivos `.docx` em modo de revisão rastreada e sincronização com o Google Drive/Docs.

---

## 1. Regras de OpenXML para Sugestões (Tracked Changes)

Em arquivos Word (`.docx`), revisões e sugestões são representadas pelos elementos `<w:del>` (exclusão) e `<w:ins>` (inserção).

### Estrutura de Injeção XML

Para sugerir a substituição de um texto `antigo` por `novo`:

```xml
<w:del w:id="101" w:author="Nome do Usuário" w:date="2026-08-20T10:00:00Z">
  <w:r>
    <w:rPr>
      <w:color w:val="000000"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
      <w:vertAlign w:val="baseline"/>
      <w:rtl w:val="0"/>
    </w:rPr>
    <w:delText xml:space="preserve">antigo</w:delText>
  </w:r>
</w:del>
<w:ins w:id="102" w:author="Nome do Usuário" w:date="2026-08-20T10:00:00Z">
  <w:r>
    <w:rPr>
      <w:color w:val="000000"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
      <w:vertAlign w:val="baseline"/>
      <w:rtl w:val="0"/>
    </w:rPr>
    <w:t xml:space="preserve">novo</w:t>
  </w:r>
</w:ins>
```

### Pontos Críticos do Esquema XML:
1. **Unicidade de IDs**: Cada `<w:del>` e `<w:ins>` deve possuir um atributo `w:id` numérico e globalmente único no documento.
2. **Atributo do Autor**: `w:author` deve conter o nome do revisor (ex.: `"João Marcelo Araújo Vieira"`).
3. **Atributo de Data**: `w:date` em formato ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`).
4. **Elemento de Texto Excluído**: Dentro de `<w:del><w:r>`, usa-se `<w:delText>`, **nunca** `<w:t>`.

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
