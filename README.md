# Gerador de Cartelas de Bingo | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Este projeto Python permite gerar cartelas de bingo a partir de um arquivo .txt contendo uma lista de palavras. O script gera n cartelas de bingo 5x5 com uma imagem no centro, e as salva em um único arquivo PDF.

![Exemplo de imagem gerada](conteudo/thumbnail.png)

Script originalmente desenvolvido para dinâmica de Bingo da Roda de Conversa do PET-SI 2025.

### Requisitos
- Python 3.x
- Bibliotecas Python necessárias:
    - pandas
    - reportlab

> Você pode instalar as dependências usando
 `pip install -r requirements.txt`

### Tutorial de uso

Para personalizar sua tabela, é importante:
1. Substituir o conteúdo de [palavras.txt](conteudo/palavras.txt) por uma lista de texto a ser aleatorizado em cada quadrante das cartelas. Cada palavra deve ser apresentada em uma linha, de maneira única.
2. Substituir o arquivo [logo.png](conteudo/logo.png) pela imagem desejada a ser acrescentada no centro da cartela.

Para executar o código e gerar as cartelas, basta digitar no seu terminal:
`python script.py`

