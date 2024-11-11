import pdfkit

# Caminho para o executável do wkhtmltopdf
path_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'  # Confirme se esse caminho está correto
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Conteúdo HTML simples para gerar o PDF de teste
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teste de PDF</title>
</head>
<body>
    <h1>Teste de Geração de PDF</h1>
    <p>Este é um teste para verificar se o pdfkit consegue gerar PDFs corretamente.</p>
</body>
</html>
"""

try:
    # Tenta gerar o PDF a partir do conteúdo HTML
    pdfkit.from_string(html_content, "output_test.pdf", configuration=config)
    print("PDF gerado com sucesso como 'output_test.pdf'")
except Exception as e:
    print(f"Erro ao gerar PDF: {e}")
