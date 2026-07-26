#!/usr/bin/env python3
"""Monta a descrição do YouTube a partir da tabela de estrutura do roteiro.

    python3 automacao/gerar_metadados.py roteiros/dia-03-roleplay-medico.md

Lê os timecodes da tabela "## Estrutura" e devolve a descrição pronta para
colar, com capítulos, aviso de afiliado e hashtags. Segue o modelo de
`producao/modelo-metadados.md`.
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

LINHA_TABELA = re.compile(r"^\|\s*(\d+:\d{2})-\d+:\d{2}\s*\|([^|]+)\|")
LIMITE_TITULO = 60

RODAPE = """
🔔 Vídeo novo TODO DIA! Se inscreva pra não perder.

👶 Este é um canal de conteúdo infantil, feito para ser assistido
com o acompanhamento de um adulto responsável.

🛒 Brinquedos que aparecem no vídeo:
[LINKS] — links de afiliado: podemos receber comissão pelas compras,
sem custo adicional para você.
"""


def limpar(texto):
    """Tira markdown e comentários do nome do bloco."""
    texto = re.sub(r"<!--.*?-->", "", texto)
    texto = texto.replace("**", "").replace("`", "")
    return texto.strip()


def extrair_capitulos(conteudo):
    capitulos = []
    for linha in conteudo.splitlines():
        m = LINHA_TABELA.match(linha)
        if not m:
            continue
        tempo, bloco = m.group(1), limpar(m.group(2))
        if bloco.lower() == "intro":
            continue  # capítulo de 10s só polui a lista
        capitulos.append((tempo, bloco))
    return capitulos


def extrair_campo(conteudo, rotulo):
    m = re.search(rf"^\*\*{rotulo}:?\*\*\s*(.+)$", conteudo, re.MULTILINE)
    return limpar(m.group(1)) if m else ""


def extrair_tags(conteudo):
    m = re.search(r"^- \*\*Tags:\*\*\s*(.+)$", conteudo, re.MULTILINE)
    return limpar(m.group(1)) if m else ""


def extrair_titulo_arquivo(conteudo):
    m = re.search(r"^#\s+(.+)$", conteudo, re.MULTILINE)
    return m.group(1).strip() if m else "(sem título)"


def hashtags(tags):
    """3 primeiras tags viram hashtag — mais que isso o YouTube ignora."""
    limpas = []
    for tag in tags.split(",")[:3]:
        # normaliza o acento antes de filtrar, senão "médico" vira "mdico"
        sem_acento = unicodedata.normalize("NFKD", tag.strip().lower())
        sem_acento = sem_acento.encode("ascii", "ignore").decode("ascii")
        palavra = re.sub(r"[^a-z0-9]", "", sem_acento)
        if palavra:
            limpas.append(f"#{palavra}")
    return " ".join(limpas)


def main():
    p = argparse.ArgumentParser(description="Gera a descrição do YouTube a partir do roteiro")
    p.add_argument("roteiro", help="caminho do arquivo de roteiro (.md)")
    p.add_argument("--titulo", help="título do vídeo (se já tiver decidido)")
    args = p.parse_args()

    caminho = Path(args.roteiro)
    if not caminho.exists():
        sys.exit(f"erro: roteiro não encontrado: {caminho}")

    conteudo = caminho.read_text(encoding="utf-8")
    capitulos = extrair_capitulos(conteudo)
    if not capitulos:
        sys.exit(
            f"erro: nenhuma tabela de estrutura encontrada em {caminho}.\n"
            "O roteiro precisa da seção '## Estrutura' com linhas no formato | 0:00-0:15 | Bloco | ... |"
        )

    tags = extrair_tags(conteudo)
    titulo = args.titulo or ""

    print("=" * 60)
    print(f"ROTEIRO: {extrair_titulo_arquivo(conteudo)}")
    print("=" * 60)

    print("\n--- TÍTULO ---")
    if titulo:
        print(titulo)
        if len(titulo) > LIMITE_TITULO:
            print(f"  aviso: {len(titulo)} caracteres. Acima de {LIMITE_TITULO} o celular corta.")
    else:
        print("(defina com --titulo) — fórmula: AÇÃO em caixa alta + tema + emoji")

    print("\n--- DESCRIÇÃO (copiar daqui) ---")
    print("[Frase 1: o que acontece no vídeo, com a palavra-chave principal]")
    print("[Frase 2: o que a criança vai ver ou aprender]")
    print(RODAPE.rstrip())
    print("\n⏱️ CAPÍTULOS")
    for tempo, bloco in capitulos:
        print(f"{tempo} {bloco}")
    if tags:
        print(f"\n{hashtags(tags)}")

    print("\n--- TAGS ---")
    print(tags or "(não encontradas no roteiro)")

    print("\n--- ANTES DE PUBLICAR ---")
    print("[ ] Marcado como \"feito para crianças\"")
    print("[ ] Links de afiliado com aviso, ou o bloco 🛒 removido")
    print("[ ] Thumbnail no padrão (automacao/gerar_thumbnail.py)")
    print("[ ] Short cortado (automacao/cortar_short.sh)")


if __name__ == "__main__":
    main()
