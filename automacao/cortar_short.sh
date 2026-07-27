#!/usr/bin/env bash
#
# Corta um trecho do vídeo longo e entrega no formato do Shorts (1080x1920).
#
#   automacao/cortar_short.sh videos/dia-03.mp4 --inicio 2:35 --duracao 30
#
# O timecode de início é o mesmo que está na tabela "## Estrutura" do roteiro.
# Precisa do ffmpeg: apt install ffmpeg  (ou brew install ffmpeg)

set -euo pipefail

LARGURA=1080
ALTURA=1920

# O Shorts aceita até 3 min, mas trecho curto retém melhor — daí o padrão baixo.
DURACAO_PADRAO=45
LIMITE_SHORTS=180

uso() {
    cat <<'FIM'
uso: cortar_short.sh VIDEO --inicio TEMPO [opções]

  --inicio TEMPO    onde o corte começa: 2:35, 1:02:35 ou 155 (segundos)
  --duracao SEG     duração do corte em segundos (padrão: 45)
  --saida ARQUIVO   arquivo de saída (padrão: shorts/<nome>-short.mp4)
  --modo MODO       corte    = corta as laterais, imagem cheia (padrão)
                    desfoque = vídeo inteiro no meio, fundo borrado
  -h, --help        mostra esta ajuda
FIM
}

# aceita 155, 2:35 e 1:02:35
para_segundos() {
    local t="$1"
    if [[ "$t" =~ ^[0-9]+$ ]]; then
        echo "$t"
    elif [[ "$t" =~ ^([0-9]+):([0-5][0-9])$ ]]; then
        echo $(( 10#${BASH_REMATCH[1]} * 60 + 10#${BASH_REMATCH[2]} ))
    elif [[ "$t" =~ ^([0-9]+):([0-5][0-9]):([0-5][0-9])$ ]]; then
        echo $(( 10#${BASH_REMATCH[1]} * 3600 + 10#${BASH_REMATCH[2]} * 60 + 10#${BASH_REMATCH[3]} ))
    else
        echo "erro: tempo inválido: $t (use 2:35, 1:02:35 ou 155)" >&2
        return 1
    fi
}

video=""
inicio=""
duracao="$DURACAO_PADRAO"
saida=""
modo="corte"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --inicio)  inicio="${2:-}"; shift 2 ;;
        --duracao) duracao="${2:-}"; shift 2 ;;
        --saida)   saida="${2:-}"; shift 2 ;;
        --modo)    modo="${2:-}"; shift 2 ;;
        -h|--help) uso; exit 0 ;;
        -*)        echo "erro: opção desconhecida: $1" >&2; uso >&2; exit 1 ;;
        *)
            if [[ -n "$video" ]]; then
                echo "erro: só um vídeo por vez (recebi '$video' e '$1')" >&2
                exit 1
            fi
            video="$1"; shift ;;
    esac
done

for programa in ffmpeg ffprobe; do
    if ! command -v "$programa" >/dev/null 2>&1; then
        echo "erro: $programa não encontrado. Instale com: apt install ffmpeg" >&2
        exit 1
    fi
done

if [[ -z "$video" ]]; then
    echo "erro: informe o arquivo de vídeo" >&2
    uso >&2
    exit 1
fi

if [[ ! -f "$video" ]]; then
    echo "erro: vídeo não encontrado: $video" >&2
    exit 1
fi

if [[ -z "$inicio" ]]; then
    echo "erro: informe --inicio (o timecode da cena na tabela do roteiro)" >&2
    exit 1
fi

if [[ "$modo" != "corte" && "$modo" != "desfoque" ]]; then
    echo "erro: --modo aceita 'corte' ou 'desfoque', recebi: $modo" >&2
    exit 1
fi

if ! [[ "$duracao" =~ ^[0-9]+$ ]] || [[ "$duracao" -eq 0 ]]; then
    echo "erro: --duracao precisa ser um número de segundos maior que zero" >&2
    exit 1
fi

if [[ "$duracao" -gt "$LIMITE_SHORTS" ]]; then
    echo "erro: $duracao s passa do limite de $LIMITE_SHORTS s do Shorts" >&2
    exit 1
fi

if [[ "$duracao" -gt 60 ]]; then
    echo "aviso: acima de 60s a retenção cai bastante. Considere cortar mais."
fi

inicio_s="$(para_segundos "$inicio")"

total="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$video" | cut -d. -f1)"
if [[ -n "$total" && "$total" =~ ^[0-9]+$ ]]; then
    if [[ "$inicio_s" -ge "$total" ]]; then
        echo "erro: início em ${inicio} passa do fim do vídeo (${total}s)" >&2
        exit 1
    fi
    if [[ $(( inicio_s + duracao )) -gt "$total" ]]; then
        echo "aviso: o corte passa do fim do vídeo — sai com $(( total - inicio_s ))s."
    fi
fi

if [[ -z "$saida" ]]; then
    base="$(basename "${video%.*}")"
    saida="shorts/${base}-short.mp4"
fi
mkdir -p "$(dirname "$saida")"

if [[ "$modo" == "corte" ]]; then
    # corta o máximo de 9:16 que couber e sobe para 1080x1920
    filtro="crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=${LARGURA}:${ALTURA},setsar=1"
else
    # o quadro inteiro no centro, com cópia borrada preenchendo o fundo
    filtro="[0:v]split=2[bg][fg];\
[bg]scale=${LARGURA}:${ALTURA}:force_original_aspect_ratio=increase,\
crop=${LARGURA}:${ALTURA},gblur=sigma=28[fundo];\
[fg]scale=${LARGURA}:${ALTURA}:force_original_aspect_ratio=decrease[frente];\
[fundo][frente]overlay=(W-w)/2:(H-h)/2,setsar=1"
fi

if [[ "$modo" == "corte" ]]; then
    filtro_arg=(-vf "$filtro")
else
    filtro_arg=(-filter_complex "$filtro")
fi

echo "cortando ${inicio} + ${duracao}s (modo: ${modo})..."

ffmpeg -hide_banner -loglevel error -stats -y \
    -ss "$inicio_s" -i "$video" -t "$duracao" \
    "${filtro_arg[@]}" \
    -c:v libx264 -preset medium -crf 21 -pix_fmt yuv420p -r 30 \
    -c:a aac -b:a 128k -ac 2 \
    -movflags +faststart \
    "$saida"

tamanho="$(du -h "$saida" | cut -f1)"
echo "short: $saida (${LARGURA}x${ALTURA}, ${tamanho})"
echo "  lembre do #shorts no título ou na descrição"
echo "  se o vídeo longo é 'feito para crianças', o short também precisa ser marcado"
