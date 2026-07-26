#!/usr/bin/env python3
"""Gera a thumbnail 1280x720 no padrão fixo do canal.

    python3 automacao/gerar_thumbnail.py foto.jpg "BRINQUEDO NOVO" --cor amarelo
    python3 automacao/gerar_thumbnail.py foto.jpg "VIREI MEDICO" --objeto kit.png --cor azul

Segue a fórmula de `producao/padrao-thumbnail.md`: fundo saturado, rosto
grande à esquerda, objeto à direita, 2-3 palavras em fonte grossa com
contorno. Mantém a paleta fixa do canal para criar reconhecimento na barra
de recomendados.

Requer: pip install pillow
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("erro: falta a Pillow. Instale com: pip install pillow")

LARGURA, ALTURA = 1280, 720

# Paleta fixa do canal — não adicione cores sem mudar o padrão inteiro
PALETA = {
    "amarelo": (255, 202, 40),
    "azul": (41, 182, 246),
    "rosa": (236, 64, 122),
    "verde": (156, 204, 44),
    "roxo": (149, 117, 205),
}

FONTES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",  # macOS
    "C:/Windows/Fonts/arialbd.ttf",  # Windows
]


def achar_fonte(tamanho):
    for caminho in FONTES:
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)
    sys.exit(
        "erro: nenhuma fonte em negrito encontrada. Instale as fontes DejaVu\n"
        "ou edite a lista FONTES neste arquivo apontando para um .ttf negrito."
    )


def encaixar(img, largura, altura):
    """Recorta a imagem para preencher a caixa sem distorcer (cover)."""
    escala = max(largura / img.width, altura / img.height)
    novo = (max(1, round(img.width * escala)), max(1, round(img.height * escala)))
    img = img.resize(novo, Image.LANCZOS)
    esq = (img.width - largura) // 2
    topo = (img.height - altura) // 2
    return img.crop((esq, topo, esq + largura, topo + altura))


def cantos_arredondados(img, raio=40):
    mascara = Image.new("L", img.size, 0)
    ImageDraw.Draw(mascara).rounded_rectangle([(0, 0), img.size], raio, fill=255)
    saida = img.convert("RGBA")
    saida.putalpha(mascara)
    return saida


def quebrar(desenho, palavras, fonte, contorno, largura_max):
    """Quebra as palavras em linhas que caibam na largura. None se não couber."""
    linhas, atual = [], ""
    for palavra in palavras:
        teste = f"{atual} {palavra}".strip()
        caixa = desenho.textbbox((0, 0), teste, font=fonte, stroke_width=contorno)
        if caixa[2] - caixa[0] <= largura_max:
            atual = teste
        else:
            if not atual:
                return None  # uma única palavra já estoura a largura
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def texto_ajustado(desenho, texto, largura_max, altura_max):
    """Maior fonte em que o texto, quebrado em linhas, cabe na caixa."""
    palavras = texto.split()
    for tamanho in range(170, 35, -4):
        fonte = achar_fonte(tamanho)
        contorno = max(5, tamanho // 12)
        linhas = quebrar(desenho, palavras, fonte, contorno, largura_max)
        if linhas and len(linhas) * tamanho * 1.15 <= altura_max:
            return fonte, linhas, contorno
    fonte = achar_fonte(36)
    return fonte, [texto], 5


def gerar(foto, texto, cor, objeto=None, saida="thumbnail.jpg"):
    if cor not in PALETA:
        sys.exit(f"erro: cor '{cor}' fora da paleta. Use: {', '.join(PALETA)}")

    palavras = texto.split()
    if len(palavras) > 3:
        print(f"aviso: '{texto}' tem {len(palavras)} palavras. O padrão pede no máximo 3.")

    fundo = Image.new("RGB", (LARGURA, ALTURA), PALETA[cor])
    margem = 40

    # Coluna esquerda: o rosto, grande, ocupando quase toda a altura
    larg_foto, alt_foto = 600, ALTURA - 2 * margem
    face = cantos_arredondados(encaixar(Image.open(foto).convert("RGB"), larg_foto, alt_foto))
    fundo.paste(face, (margem, margem), face)

    # Coluna direita: objeto em cima (se houver) e o texto embaixo
    col_x = margem + larg_foto + margem
    col_larg = LARGURA - col_x - margem
    texto_topo, texto_alt = margem, ALTURA - 2 * margem

    if objeto:
        obj = Image.open(objeto).convert("RGBA")
        obj.thumbnail((col_larg, 300), Image.LANCZOS)
        fundo.paste(obj, (col_x + (col_larg - obj.width) // 2, margem), obj)
        texto_topo = margem + obj.height + 30
        texto_alt = ALTURA - texto_topo - margem

    desenho = ImageDraw.Draw(fundo)
    fonte, linhas, contorno = texto_ajustado(desenho, texto, col_larg, texto_alt)

    altura_linha = fonte.size * 1.15
    y = texto_topo + (texto_alt - len(linhas) * altura_linha) / 2 + altura_linha / 2
    for linha in linhas:
        desenho.text(
            (col_x + col_larg / 2, y),
            linha,
            font=fonte,
            fill=(255, 255, 255),
            stroke_width=contorno,
            stroke_fill=(20, 20, 20),
            anchor="mm",
        )
        y += altura_linha

    fundo.save(saida, "JPEG", quality=90)
    tamanho_kb = Path(saida).stat().st_size / 1024
    print(f"criado: {saida} ({LARGURA}x{ALTURA}, {tamanho_kb:.0f} KB)")
    if tamanho_kb > 2048:
        print("aviso: acima de 2 MB, o YouTube vai recusar. Reduza a qualidade.")


def main():
    p = argparse.ArgumentParser(description="Gera thumbnail no padrão do canal")
    p.add_argument("foto", help="foto da criança (o rosto grande da thumbnail)")
    p.add_argument("texto", help="2 a 3 palavras, em caixa alta")
    p.add_argument("--cor", default="amarelo", help=f"cor de fundo: {', '.join(PALETA)}")
    p.add_argument("--objeto", help="PNG do brinquedo/objeto, de preferência sem fundo")
    p.add_argument("--saida", default="thumbnail.jpg", help="arquivo de saída")
    args = p.parse_args()

    if not Path(args.foto).exists():
        sys.exit(f"erro: foto não encontrada: {args.foto}")

    gerar(args.foto, args.texto, args.cor, args.objeto, args.saida)


if __name__ == "__main__":
    main()
