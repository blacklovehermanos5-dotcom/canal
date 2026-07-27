#!/usr/bin/env bash
# Dá movimento a um quadro parado com pan/zoom (efeito Ken Burns).
#
#   ./automacao/animar_still.sh quadro-07.png 4
#   ./automacao/animar_still.sh quadro-07.png 3 --movimento zoom-out
#   ./automacao/animar_still.sh close.png 2 --movimento zoom-in-rapido
#
# Substitui a geração de vídeo na maior parte dos planos: um clipe de 5s
# gerado por IA custa ~7,5 créditos, isto custa zero. No gênero novela, o
# close de reação com zoom lento é exatamente o que se espera.
#
# Requer: ffmpeg

set -euo pipefail

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "erro: ffmpeg não encontrado." >&2
  echo "  macOS:  brew install ffmpeg" >&2
  echo "  Ubuntu: sudo apt install ffmpeg" >&2
  exit 1
fi

if [ $# -lt 2 ]; then
  echo "uso: $0 <imagem> <duracao_seg> [--movimento TIPO] [--saida arquivo.mp4]" >&2
  echo "movimentos: zoom-in (padrão), zoom-out, zoom-in-rapido, pan-direita, pan-esquerda" >&2
  exit 1
fi

IMAGEM="$1"; DURACAO="$2"; shift 2
MOVIMENTO="zoom-in"; SAIDA=""

while [ $# -gt 0 ]; do
  case "$1" in
    --movimento) MOVIMENTO="${2:-}"; shift 2 ;;
    --saida)     SAIDA="${2:-}";     shift 2 ;;
    *) echo "erro: opção desconhecida: $1" >&2; exit 1 ;;
  esac
done

[ -f "$IMAGEM" ] || { echo "erro: imagem não encontrada: $IMAGEM" >&2; exit 1; }

case "$DURACAO" in
  ''|*[!0-9]*) echo "erro: duração precisa ser um número inteiro de segundos" >&2; exit 1 ;;
esac
[ "$DURACAO" -ge 1 ] || { echo "erro: duração mínima é 1s" >&2; exit 1; }

[ -z "$SAIDA" ] && SAIDA="${IMAGEM%.*}-${MOVIMENTO}.mp4"

FPS=30
QUADROS=$((DURACAO * FPS))
LARGURA=1920
ALTURA=1080

# O zoompan trabalha melhor sobre uma imagem ampliada: sem isso o
# resultado treme, porque o deslocamento é arredondado por pixel.
BASE="scale=${LARGURA}*4:${ALTURA}*4,setsar=1"

case "$MOVIMENTO" in
  zoom-in)
    Z="min(zoom+0.0008,1.25)"; X="iw/2-(iw/zoom/2)"; Y="ih/2-(ih/zoom/2)" ;;
  zoom-in-rapido)
    Z="min(zoom+0.0025,1.6)";  X="iw/2-(iw/zoom/2)"; Y="ih/2-(ih/zoom/2)" ;;
  zoom-out)
    Z="if(lte(zoom,1.0),1.25,max(zoom-0.0008,1.0))"; X="iw/2-(iw/zoom/2)"; Y="ih/2-(ih/zoom/2)" ;;
  pan-direita)
    Z="1.2"; X="(iw-iw/zoom)*on/${QUADROS}"; Y="ih/2-(ih/zoom/2)" ;;
  pan-esquerda)
    Z="1.2"; X="(iw-iw/zoom)*(1-on/${QUADROS})"; Y="ih/2-(ih/zoom/2)" ;;
  *)
    echo "erro: movimento inválido: $MOVIMENTO" >&2
    echo "use: zoom-in, zoom-out, zoom-in-rapido, pan-direita, pan-esquerda" >&2
    exit 1 ;;
esac

echo "animando $IMAGEM — $MOVIMENTO, ${DURACAO}s"

ffmpeg -hide_banner -loglevel error -stats \
  -loop 1 -i "$IMAGEM" \
  -filter_complex "${BASE},zoompan=z='${Z}':x='${X}':y='${Y}':d=${QUADROS}:s=${LARGURA}x${ALTURA}:fps=${FPS}" \
  -t "$DURACAO" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -movflags +faststart \
  -y "$SAIDA"

echo "pronto: $SAIDA (custo: 0 créditos)"
