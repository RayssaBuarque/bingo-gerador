import random

import pandas as pd
from reportlab.lib.pagesizes import landscape, letter
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

    # criação da primeira linha da cartela (cabeçalho)
    cartela = [["B", "I", "N", "G", "O"]]  # Primeira linha com BINGO

    palavras_aleatorias = [palavras[i:i+5] for i in range(0, 25, 5)]
    
    # deixando o centro livre pra imagem
    palavras_aleatorias[2][2] = "LIVRE"

    # adiciona as palavras abaixo do cabeçalho
    cartela.extend(palavras_aleatorias)

    return cartela


"""Gera n cartelas e salva todas em um único PDF"""
def salvar_cartelas_pdf(num_cartelas, palavras, imagem, nome_arquivo="cartelas.pdf"):
    pdf = canvas.Canvas(nome_arquivo, pagesize=landscape(letter))
    largura, altura = landscape(letter)
    
    # Estilos de texto para quebras automáticas
    estilos = getSampleStyleSheet()
    estilo_celula = estilos["Normal"]
    estilo_celula.fontName = "Helvetica"
    estilo_celula.fontSize = 8
    estilo_celula.alignment = 1
    
    # informações de impressão de margem e qtd de cartelas por página
    cartelas_por_pagina = 3
    espacamento_x = 260
    margem_x = 10
    margem_y = altura - 320
    x_pos, y_pos = margem_x, margem_y
    
    for i in range(num_cartelas):
        cartela = gerar_cartela(palavras)  # gerando as palavras da cartela

        # Substituir texto por Parágrafos para quebrar automaticamente
        for linha in range(1,6):
            for coluna in range(5):
                if cartela[linha][coluna]: # se houver texto
                    cartela[linha][coluna] = Paragraph(cartela[linha][coluna], estilo_celula)
        
        # criando uma tabela com as palavras
        tabela = Table(cartela, colWidths=50, rowHeights=[40] + [50]*5) 
        estilo = TableStyle([
            # Cabeçalho "BINGO" colorido
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#992727")),  # Vermelho escuro no cabeçalho
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texto branco no cabeçalho
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Negrito no cabeçalho
            ('FONTSIZE', (0, 0), (-1, 0), 20),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),

            # Corpo da tabela (todas as outras células)
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),

            # Estilização da tabela
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROUND', (0, 0), (4, 4), 50),
        ])
        
        tabela.setStyle(estilo)
        tabela.wrapOn(pdf, largura, altura)
        tabela.drawOn(pdf, x_pos, y_pos)
        
        # inserindo a imagem no centro da cartela com aposição
        # x e y correspondente à linha e coluna do meio
        img_x = x_pos + 100
        img_y = y_pos + 100
        pdf.drawImage(imagem, img_x, img_y, width=50, height=50)
        
        # segue reto pra prox posição no PDF pra encaixar prox cartela
        x_pos += espacamento_x  

        # se já houverem 3 cartelas na página,
        # ele cria uma nova e avança a posição no PDF
        if (i + 1) % cartelas_por_pagina == 0:
            pdf.showPage()
            x_pos, y_pos = margem_x, margem_y
        elif (i + 1) % 3 == 0:
            x_pos = margem_x
            y_pos -= 270
 
    pdf.save()
    print(f"{num_cartelas} cartelas salvas em {nome_arquivo}")



'''EXECUTANDO O SCRIPT'''

arq_palavras = "conteudo/palavras.txt"
logo = "conteudo/logo.png"

palavras = carregar_palavras(arq_palavras)

n = int(input("Quantas cartelas deseja gerar? "))
salvar_cartelas_pdf(n, palavras, logo)
