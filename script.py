import random

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet



"""Carrega as palavras do arquivo .txt e retorna uma lista"""
def carregar_palavras(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        palavras = [linha.strip() for linha in f.readlines()]
    return palavras


"""Gera uma cartela de bingo 5x5 a partir de um .txt com palavras"""
def gerar_cartela(palavras):    
    random.shuffle(palavras)
    cartela = [palavras[i:i+5] for i in range(0, 25, 5)]
    
    # deixando o centro livre pra imagem
    cartela[2][2] = "LIVRE"

    return cartela


"""Gera n cartelas e salva todas em um único PDF"""
def salvar_cartelas_pdf(num_cartelas, palavras, imagem="logo.png", nome_arquivo="cartelas.pdf"):
    pdf = canvas.Canvas(nome_arquivo, pagesize=letter)
    largura, altura = letter

    # Estilos de texto para quebras automáticas
    estilos = getSampleStyleSheet()
    estilo_celula = estilos["Normal"]
    estilo_celula.fontName = "Helvetica"
    estilo_celula.fontSize = 9

    # variável que vai guardar a posição em que escrevemos no PDF
    y_pos = altura - 320

    for i in range(num_cartelas):
        cartela = gerar_cartela(palavras)  # gerando as palavras da cartela

        # Substituir texto por Parágrafos para quebrar automaticamente
        for linha in range(5):
            for coluna in range(5):
                if cartela[linha][coluna]:  # Se houver texto
                    cartela[linha][coluna] = Paragraph(cartela[linha][coluna], estilo_celula)

        tabela = Table(cartela, colWidths=70, rowHeights=60) # criando uma tabela com as palavras

        estilo = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        
        tabela.setStyle(estilo)
        tabela.wrapOn(pdf, largura, altura)
        tabela.drawOn(pdf, 50, y_pos)

        # inserindo a imagem no centro da cartela com aposição
        # x e y correspondente à linha e coluna do meio
        img_x = 195  
        img_y = y_pos + 120 
        pdf.drawImage(imagem, img_x, img_y, width=60, height=60)

        # segue reto pra prox posição no PDF
        y_pos -= 320  

        # se não tiver espaço suficiente, ele cria uma nova página e avança a posição no PDF
        if y_pos < 50:
            pdf.showPage()
            y_pos = altura - 320

    pdf.save()
    print(f"{num_cartelas} cartelas salvas em {nome_arquivo}")

# Executando o script
arq_palavras = "palavras.txt"
palavras = carregar_palavras(arq_palavras)

num_cartelas = int(input("Quantas cartelas deseja gerar? "))
salvar_cartelas_pdf(num_cartelas, palavras)
