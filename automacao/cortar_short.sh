#!/usr/bin/env bash
# Corta um trecho do vídeo longo e entrega o Short pronto em 9:16.
#
#   ./automacao/cortar_short.sh video.mp4 3:45 4:10
#   ./automacao/cortar_short.sh video.mp4 3:45 4:10 --texto "ELE ABRIU!"
#   ./automacao/cortar_short.sh video.mp4 3:45 4:10 --modo desfoque
#
# modo recorte  (padrão) — corta as laterais, foco no centro do quadro
# modo desfoque           — mantém o quadro inteiro, preenche com fundo desfocado
#
# Requer: ffmpeg

set -euo pipefail

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "erro: ffmpeg não encontrado." >&2
  echo "  macOS:  brew install ffmpeg" >&2
  echo "  Ubuntu: sudo apt install ffmpeg" >&2
  echo "  Windows: https://ffmpeg.org/download.html" >&2
  exit 1
fi

if [ $# -lt 3 ]; then
  echo "uso: $0 <video> <inicio> <fim> [--texto \"LEGENDA\"] [--modo recorte|desfoque] [--saida arquivo.mp4]" >&2
  echo "     tempos em MM:SS ou HH:MM:SS" >&2
  exit 1
fi

VIDEO="$1"; INICIO="$2"; FIM="$3"; shift 3
TEXTO=""; MODO="recorte"; SAIDA=""

while [ $# -gt 0 ]; do
  case "$1" in
    --texto)  TEXTO="${2:-}"; shift 2 ;;
    --modo)   MODO="${2:-}";  shift 2 ;;
    --saida)  SAIDA="${2:-}"; shift 2 ;;
    *) echo "erro: opção desconhecida: $1" >&2; exit 1 ;;
  esac
done

[ -f "$VIDEO" ] || { echo "erro: vídeo não encontrado: $VIDEO" >&2; exit 1; }
[ -z "$SAIDA" ] && SAIDA="short-$(basename "${VIDEO%.*}")-${INICIO//:/}.mp4"

# --- duração: Shorts acima de 60s deixam de ser Short ---
para_segundos() {
  local t="$1" total=0
  IFS=':' read -ra partes <<< "$t"
  for parte in "${partes[@]}"; do
    total=$((total * 60 + 10#$parte))
  done
  echo "$total"
}

SEG_INICIO=$(para_segundos "$INICIO")
SEG_FIM=$(para_segundos "$FIM")
DURACAO=$((SEG_FIM - SEG_INICIO))

if [ "$DURACAO" -le 0 ]; then
  echo "erro: o fim ($FIM) precisa ser depois do início ($INICIO)" >&2
  exit 1
fi
if [ "$DURACAO" -gt 60 ]; then
  echo "erro: $DURACAO s. O YouTube só trata como Short até 60s." >&2
  exit 1
fi
if [ "$DURACAO" -gt 35 ]; then
  echo "aviso: $DURACAO s. Shorts infantis performam melhor abaixo de 30s."
fi

# --- montagem do filtro ---
case "$MODO" in
  recorte)
    FILTRO="crop=ih*9/16:ih,scale=1080:1920:flags=lanczos"
    ;;
  desfoque)
    FILTRO="split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=25[bg];[b]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2"
    ;;
  *)
    echo "erro: modo inválido: $MODO (use recorte ou desfoque)" >&2; exit 1 ;;
esac

# --- legenda queimada, se pedida ---
if [ -n "$TEXTO" ]; then
  FONTE=""
  for f in /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf \
           /usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf \
           "/System/Library/Fonts/Supplemental/Arial Bold.ttf" \
           "C:/Windows/Fonts/arialbd.ttf"; do
    [ -f "$f" ] && { FONTE="$f"; break; }
  done

  if [ -z "$FONTE" ]; then
    echo "aviso: nenhuma fonte negrito encontrada, gerando sem legenda."
  else
    ESCAPADO=$(printf '%s' "$TEXTO" | sed "s/'/\\\\'/g; s/:/\\\\:/g")
    FILTRO="${FILTRO},drawtext=fontfile='${FONTE}':text='${ESCAPADO}':fontsize=86:fontcolor=white:borderw=8:bordercolor=black:x=(w-text_w)/2:y=h*0.72"
  fi
fi

echo "cortando ${DURACAO}s de $VIDEO ($INICIO → $FIM), modo $MODO"

ffmpeg -hide_banner -loglevel error -stats \
  -ss "$INICIO" -to "$FIM" -i "$VIDEO" \
  -filter_complex "$FILTRO" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  -y "$SAIDA"

echo "pronto: $SAIDA"
echo
echo "Antes de publicar:"
echo "  - conferir se não entrou nada identificável no recorte (placa, uniforme, fachada)"
echo "  - marcar como \"feito para crianças\" no upload"
