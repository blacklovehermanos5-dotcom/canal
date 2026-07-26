# Automação da produção

Scripts que tiram o trabalho repetitivo da rotina diária. O que dá pra automatizar aqui é a **embalagem** do vídeo — esqueleto de roteiro, thumbnail, corte de Short, descrição. A gravação em si não é automatizável, e a seção final explica por que tentar automatizá-la seria ruim para o canal.

## Instalação

```bash
pip install pillow          # thumbnail
# ffmpeg: brew install ffmpeg | sudo apt install ffmpeg
```

## Os quatro scripts

### 1. Esqueleto de roteiro

```bash
python3 automacao/gerar_roteiro.py 12
```

Lê o dia 12 do calendário, identifica que é roleplay e gera `roteiros/dia-12-veterinario-....md` com a estrutura de blocos daquele formato, timecodes, planos de câmera, receita do Short, tags e a checagem de segurança. Sobra preencher materiais e falas.

Os dias 8 a 30 saem em um comando:

```bash
for d in $(seq 8 30); do python3 automacao/gerar_roteiro.py $d; done
```

### 2. Thumbnail no padrão

```bash
python3 automacao/gerar_thumbnail.py foto.jpg "BRINQUEDO NOVO" --cor amarelo
python3 automacao/gerar_thumbnail.py foto.jpg "VIREI MEDICO" --objeto kit.png --cor azul
```

Monta 1280x720 seguindo `producao/padrao-thumbnail.md`: fundo da paleta fixa, rosto grande à esquerda, objeto e texto na coluna direita, contorno preto. A fonte se ajusta e quebra em linhas sozinha. Avisa se o texto passar de 3 palavras ou se o arquivo passar de 2 MB.

Cores: `amarelo`, `azul`, `rosa`, `verde`, `roxo`.

### 3. Corte de Short

```bash
./automacao/cortar_short.sh video.mp4 3:45 4:10
./automacao/cortar_short.sh video.mp4 3:45 4:10 --texto "ELE ABRIU!" --modo desfoque
```

Corta o trecho, converte para 9:16 em 1080x1920 e queima a legenda. Recusa trechos acima de 60s (deixa de ser Short) e avisa acima de 35s.

- `--modo recorte` (padrão): corta as laterais, foco no centro
- `--modo desfoque`: mantém o quadro inteiro sobre fundo desfocado

### 4. Descrição com capítulos

```bash
python3 automacao/gerar_metadados.py roteiros/dia-03-roleplay-medico.md \
  --titulo "Virei MÉDICO(A) por um dia! 🩺 Consultório dos bichinhos"
```

Lê os timecodes da tabela do roteiro e devolve a descrição pronta para colar: capítulos, aviso de afiliado, hashtags e a checagem de publicação. Avisa se o título passar de 60 caracteres.

## Rotina diária com os scripts

| Etapa | Comando | Tempo |
|---|---|---|
| Véspera: roteiro | `gerar_roteiro.py <dia>` + preencher | ~10 min |
| Gravação | — | 60-90 min |
| Edição | seu editor | 40-60 min |
| Short | `cortar_short.sh` | ~2 min |
| Thumbnail | `gerar_thumbnail.py` | ~2 min |
| Descrição | `gerar_metadados.py` | ~2 min |

O ganho real está nas três últimas linhas: o que costuma levar 30-40 minutos por vídeo cai para menos de 10.

## Estado dos testes

| Script | Verificado |
|---|---|
| `gerar_roteiro.py` | ✅ executado, saída conferida |
| `gerar_metadados.py` | ✅ executado nos roteiros reais |
| `gerar_thumbnail.py` | ✅ executado, imagens inspecionadas |
| `cortar_short.sh` | ⚠️ lógica testada com `ffmpeg` simulado — o filtro e a codificação **não** foram rodados de verdade. Teste em um vídeo curto antes de confiar nele. |

## O que NÃO automatizar

Existe a tentação de gerar o vídeo inteiro com IA — voz sintética, personagem animado, roteiro automático, publicação em massa. Para este canal, isso é um caminho ruim, por três motivos concretos:

1. **É exatamente o alvo da política do YouTube** contra conteúdo infantil repetitivo e produzido em massa, sem valor educativo ou narrativo. É o tipo de canal que perde monetização em bloco, não vídeo a vídeo.
2. **Conteúdo sintético exige divulgação.** Vídeo com voz ou imagem gerada realista precisa ser declarado no upload, e conteúdo infantil recebe escrutínio maior.
3. **O ativo do canal é a criança real.** O vínculo que faz uma criança assistir ao mesmo canal todo dia vem de reconhecer uma pessoa. Substituir isso por avatar sintético destrói justamente o que diferencia o canal.

Uso de IA que faz sentido aqui, sem esses riscos: **vinheta de 5s** animada, **música de fundo** instrumental, **efeitos sonoros**, **imagens de apoio** para os blocos educativos (uma ilustração de animal, uma forma geométrica). Nada disso envolve gerar a criança nem simular o conteúdo principal.

O limite prático: automatize a **embalagem e a distribuição**, nunca a **atuação e a autoria**.
