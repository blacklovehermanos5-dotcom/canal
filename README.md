# canal

Roteiros e automações de produção do canal.

## Estrutura

```
agosto                        plano de conteúdo de 30 dias
producao/modelo-metadados.md  o formato que o roteiro precisa seguir
roteiros/                     um arquivo .md por vídeo
automacao/                    os scripts de pós-produção
```

Pastas que **não** entram no git (ver `.gitignore`): `videos/` (bruto),
`frames/` (prints para thumbnail), `thumbs/` e `shorts/` (saída dos scripts).

## Instalação

```bash
pip3 install Pillow      # gerar_thumbnail.py
apt install ffmpeg       # cortar_short.sh  (macOS: brew install ffmpeg)
```

O `gerar_metadados.py` roda só com Python 3, sem dependência.

## Fluxo por vídeo

**1. Escreva o roteiro** em `roteiros/`, seguindo
[`producao/modelo-metadados.md`](producao/modelo-metadados.md). O que os
scripts leem de lá: o título (primeiro `#`), a linha `- **Tags:**` e a tabela
`## Estrutura` com os timecodes. Use
[`roteiros/dia-03-roleplay-medico.md`](roteiros/dia-03-roleplay-medico.md) como
exemplo.

**2. Grave e edite** o vídeo longo. Guarde em `videos/`.

**3. Rode os três scripts.** Todos aceitam `--publico adulto` (padrão) ou
`--publico infantil`, que troca o rodapé da descrição, a paleta da thumbnail e
o checklist de publicação.

```bash
# descrição, capítulos, tags e checklist
python3 automacao/gerar_metadados.py roteiros/dia-03-roleplay-medico.md \
    --publico infantil --titulo "BRINCANDO DE MÉDICO no hospitalzinho 🏥"

# thumbnail 1280x720
python3 automacao/gerar_thumbnail.py "BRINCANDO DE MÉDICO" \
    --subtexto "o ursinho tá com febre!" --publico infantil \
    --fundo frames/dia-03-ursinho.png

# short 1080x1920 a partir do timecode da cena
automacao/cortar_short.sh videos/dia-03.mp4 --inicio 2:35 --duracao 30
```

Cada script tem `--help` com todas as opções.

## Detalhes que costumam morder

- **"Feito para crianças"** liga e desliga comentários, sino e RPM — e marcar
  errado é violação do COPPA. O `--publico` escolhe o checklist certo, mas a
  marcação em si é manual no Studio.
- **Aviso de afiliado**: se não houver link no vídeo, apague o bloco 🛒 inteiro
  da descrição em vez de deixá-lo vazio.
- **Capítulos**: o YouTube só ativa se forem 3 ou mais, o primeiro começar em
  `0:00` e cada um durar 10s ou mais. Como o script descarta a vinheta, comece
  o segundo bloco em `0:00` se quiser os capítulos clicáveis.
- **Thumbnail**: confira em tamanho de miniatura antes de subir. Mais de 4
  palavras e a fonte encolhe até sumir no celular.
