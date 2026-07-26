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
python3 automacao/gerar_metadados.py serie-frutas/roteiros/cap-01-a-chegada.md \
  --titulo "CHEGOU UM ESTRANHO NA VILA 😳 | A Vila — Capítulo 1"
```

Lê os timecodes da tabela do roteiro e devolve a descrição pronta para colar: capítulos, chamada de comentário, hashtags e a checagem de publicação. Avisa se o título passar de 60 caracteres.

Usa o molde adulto por padrão. Para o formato antigo: `--publico infantil`.

### 5. Movimento sem gastar créditos

```bash
./automacao/animar_still.sh quadro-07.png 4 --movimento zoom-in
```

Pan/zoom (Ken Burns) sobre um quadro parado. **Substitui a geração de vídeo na maior parte dos planos**: um clipe de 5s por IA custa ~7,5 créditos, isto custa zero. No gênero novela, o close de reação com zoom lento é exatamente o esperado.

Movimentos: `zoom-in`, `zoom-out`, `zoom-in-rapido`, `pan-direita`, `pan-esquerda`.

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
| `gerar_metadados.py` | ✅ executado nos roteiros reais, nos dois modos |
| `gerar_thumbnail.py` | ✅ executado, imagens inspecionadas |
| `cortar_short.sh` | ⚠️ lógica testada com `ffmpeg` simulado — o filtro e a codificação **não** foram rodados de verdade |
| `animar_still.sh` | ⚠️ idem: argumentos e validação testados, o filtro `zoompan` **não** foi executado |

Os dois scripts de `ffmpeg` foram escritos sem `ffmpeg` disponível no ambiente. Teste cada um em um arquivo curto antes de usar em produção.

## Escopo destes scripts

Foram escritos para o formato antigo (canal infantil com criança real). Com a virada para a [série animada de frutas](../serie-frutas/plano.md), o que continua servindo:

| Script | Serve na série? |
|---|---|
| `cortar_short.sh` | ✅ igual — o Short é cortado do mesmo jeito |
| `gerar_metadados.py` | ✅ igual — basta o roteiro ter a tabela `## Estrutura` |
| `gerar_thumbnail.py` | ✅ trocando a paleta pelas cores da série e usando um quadro do capítulo no lugar da foto |
| `gerar_roteiro.py` | ❌ os formatos são de vídeo gravado; a série usa a estrutura de `serie-frutas/plano.md` |

## O limite que continua valendo

A série é gerada por IA de ponta a ponta — é o próprio gênero. Mas há uma linha que separa uma série de um lote de vídeos, e ela decide a monetização:

- **Automatize a execução**: quadros, animação, vozes, trilha, corte, metadados.
- **Não automatize a autoria**: enredo, personagens, ritmo e revisão final são seus.

Um roteiro gerado e publicado sem revisão, com personagens diferentes a cada vídeo, cai na política de conteúdo inautêntico do YouTube e derruba o canal inteiro, não um vídeo. O detalhamento está em [`serie-frutas/compliance.md`](../serie-frutas/compliance.md).
