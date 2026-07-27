#!/usr/bin/env python3
"""Gera a thumbnail no padrão do canal (1280x720).

    python3 automacao/gerar_thumbnail.py "BRINCANDO DE MÉDICO" --fundo frames/dia-03.png

Sem --fundo, usa um fundo chapado da paleta do público escolhido. O texto é
quebrado e redimensionado sozinho até caber na área segura, com contorno grosso
para continuar legível no tamanho de miniatura do celular.

Precisa do Pillow: pip3 install Pillow
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("erro: Pillow não instalado. Rode: pip3 install Pillow")

LARGURA, ALTURA = 1280, 720
MARGEM = 64

# O YouTube desenha a duração do vídeo neste canto. Texto aqui some.
ZONA_DURACAO = (200, 60)

# tamanho mínimo antes de desistir: abaixo disso não se lê na miniatura
TAMANHO_MIN = 44
TAMANHO_MAX = 190

LIMITE_PALAVRAS = 4

PALETAS = {
    "adulto": {
        "fundo": (14, 16, 24),
        "texto": (255, 255, 255),
        "contorno": (0, 0, 0),
        "destaque": (220, 38, 38),
    },
    "infantil": {
        "fundo": (255, 209, 51),
        "texto": (255, 255, 255),
        "contorno": (28, 20, 60),
        "destaque": (236, 72, 153),
    },
}

FONTES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def achar_fonte(caminho_manual):
    if caminho_manual:
        if not Path(caminho_manual).exists():
            sys.exit(f"erro: fonte não encontrada: {caminho_manual}")
        return caminho_manual
    for caminho in FONTES:
        if Path(caminho).exists():
            return caminho
    sys.exit(
        "erro: nenhuma fonte negrito encontrada no sistema.\n"
        "Passe uma com --fonte caminho/para/fonte.ttf"
    )


def slug(texto):
    sem_acento = unicodedata.normalize("NFKD", texto.lower())
    sem_acento = sem_acento.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", sem_acento).strip("-") or "thumbnail"


def preparar_fundo(caminho, paleta):
    """Carrega a imagem de fundo cobrindo o quadro inteiro, sem distorcer."""
    if not caminho:
        return Image.new("RGB", (LARGURA, ALTURA), paleta["fundo"])

    origem = Path(caminho)
    if not origem.exists():
        sys.exit(f"erro: imagem de fundo não encontrada: {origem}")

    img = Image.open(origem).convert("RGB")
    escala = max(LARGURA / img.width, ALTURA / img.height)
    novo = (max(1, round(img.width * escala)), max(1, round(img.height * escala)))
    img = img.resize(novo, Image.LANCZOS)
    esq = (img.width - LARGURA) // 2
    topo = (img.height - ALTURA) // 2
    return img.crop((esq, topo, esq + LARGURA, topo + ALTURA))


def escurecer(img, forca):
    """Véu escuro atrás do texto — foto crua quase nunca tem contraste suficiente."""
    if forca <= 0:
        return img
    veu = Image.new("RGB", img.size, (0, 0, 0))
    return Image.blend(img, veu, min(forca, 0.9))


def quebrar(texto, fonte, desenho, largura_max):
    """Quebra por medida real da fonte, não por contagem de caracteres."""
    linhas = []
    atual = ""
    for palavra in texto.split():
        teste = f"{atual} {palavra}".strip()
        if desenho.textlength(teste, font=fonte) <= largura_max or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def espessura_contorno(tamanho):
    return max(3, round(tamanho * 0.09))


def caber(texto, caminho_fonte, desenho, caixa):
    """Maior tamanho de fonte em que o texto ainda cabe na caixa.

    O contorno cresce para fora do que `textlength` mede, então ele sai do
    espaço disponível antes da quebra — senão a borda encosta na margem.
    """
    largura_max, altura_max = caixa
    for tamanho in range(TAMANHO_MAX, TAMANHO_MIN - 1, -2):
        fonte = ImageFont.truetype(caminho_fonte, tamanho)
        contorno = espessura_contorno(tamanho)
        linhas = quebrar(texto, fonte, desenho, largura_max - 2 * contorno)
        entrelinha = round(tamanho * 1.16)
        if len(linhas) * entrelinha + 2 * contorno <= altura_max:
            return fonte, linhas, entrelinha
    fonte = ImageFont.truetype(caminho_fonte, TAMANHO_MIN)
    contorno = espessura_contorno(TAMANHO_MIN)
    linhas = quebrar(texto, fonte, desenho, largura_max - 2 * contorno)
    return fonte, linhas, round(TAMANHO_MIN * 1.16)


def main():
    p = argparse.ArgumentParser(description="Gera a thumbnail 1280x720 do canal")
    p.add_argument("texto", help="frase principal da thumbnail (3-4 palavras)")
    p.add_argument("--subtexto", help="linha menor abaixo da frase principal")
    p.add_argument("--fundo", help="imagem de fundo (frame do vídeo)")
    p.add_argument("--saida", help="arquivo de saída (padrão: thumbs/<slug>.png)")
    p.add_argument(
        "--publico",
        default="adulto",
        choices=["adulto", "infantil"],
        help="paleta da thumbnail (padrão: adulto, o formato atual do canal)",
    )
    p.add_argument("--fonte", help="caminho de uma fonte .ttf negrito")
    p.add_argument(
        "--escurecer",
        type=float,
        default=0.45,
        help="véu escuro sobre o fundo, de 0 a 1 (padrão: 0.45)",
    )
    args = p.parse_args()

    paleta = PALETAS[args.publico]
    caminho_fonte = achar_fonte(args.fonte)
    texto = args.texto.strip().upper()

    if len(texto.split()) > LIMITE_PALAVRAS:
        print(
            f"aviso: {len(texto.split())} palavras. Acima de {LIMITE_PALAVRAS} "
            "a fonte encolhe e some na miniatura do celular.",
            file=sys.stderr,
        )

    img = preparar_fundo(args.fundo, paleta)
    if args.fundo:
        img = escurecer(img, args.escurecer)

    desenho = ImageDraw.Draw(img)

    # área útil: margens de todo lado, menos o canto da duração
    largura_util = LARGURA - 2 * MARGEM
    altura_util = ALTURA - 2 * MARGEM - (ZONA_DURACAO[1] if args.subtexto else 0)

    fonte, linhas, entrelinha = caber(texto, caminho_fonte, desenho, (largura_util, altura_util))
    contorno = espessura_contorno(fonte.size)

    altura_bloco = len(linhas) * entrelinha
    y = (ALTURA - altura_bloco) // 2
    if args.subtexto:
        y -= 30  # abre espaço embaixo sem descentralizar demais

    for linha in linhas:
        largura_linha = desenho.textlength(linha, font=fonte)
        x = (LARGURA - largura_linha) / 2
        desenho.text(
            (x, y),
            linha,
            font=fonte,
            fill=paleta["texto"],
            stroke_width=contorno,
            stroke_fill=paleta["contorno"],
        )
        y += entrelinha

    if args.subtexto:
        sub = ImageFont.truetype(caminho_fonte, 46)
        rotulo = args.subtexto.strip()
        largura_sub = desenho.textlength(rotulo, font=sub)
        # tarja de destaque atrás do subtexto, longe do canto da duração
        pad = 22
        x0 = (LARGURA - largura_sub) / 2 - pad
        y0 = y + 18
        desenho.rounded_rectangle(
            (x0, y0, x0 + largura_sub + 2 * pad, y0 + sub.size + 2 * pad * 0.55),
            radius=16,
            fill=paleta["destaque"],
        )
        desenho.text((x0 + pad, y0 + pad * 0.5), rotulo, font=sub, fill=(255, 255, 255))

    saida = Path(args.saida) if args.saida else Path("thumbs") / f"{slug(args.texto)}.png"
    saida.parent.mkdir(parents=True, exist_ok=True)
    img.save(saida, "PNG", optimize=True)

    kb = saida.stat().st_size / 1024
    print(f"thumbnail: {saida} ({LARGURA}x{ALTURA}, {kb:.0f} KB)")
    if kb > 2048:
        print("  aviso: acima de 2 MB o YouTube recusa o upload.")
    print("  confira em miniatura antes de subir: reduza para 210x118 e veja se ainda lê.")


if __name__ == "__main__":
    main()
