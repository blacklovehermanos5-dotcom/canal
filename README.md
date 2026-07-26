# Canal — material de produção

> **Direção atual: série animada de frutas para público adulto** (`serie-frutas/`).
> O material de canal infantil (`agosto`, `roteiros/`, `producao/`) fica no
> repositório como histórico — parte dele ainda serve, ver o plano.

## Estrutura

| Arquivo | O que é |
|---|---|
| [`serie-frutas/`](serie-frutas/plano.md) | **Formato atual**: elenco, arco de 30 dias, pipeline de IA, prompts e compliance |
| [`automacao/`](automacao) | Scripts que geram roteiro, thumbnail, Short e descrição |
| [`agosto`](agosto) | *(histórico)* Plano de 30 dias do canal infantil |
| [`roteiros/`](roteiros) | *(histórico)* Roteiros dos vídeos com criança real |
| [`producao/`](producao) | *(histórico)* Kit de gravação; o controle de postagem ainda serve |

## Série de frutas — comece por aqui

- [Plano da série](serie-frutas/plano.md) — elenco, estrutura do capítulo, arco de 30 dias
- [Prompts](serie-frutas/prompts.md) — bíblia visual e as regras de consistência
- [Pipeline de produção](serie-frutas/producao-ia.md) — as 6 etapas de um capítulo, com custos
- [Compliance](serie-frutas/compliance.md) — política de conteúdo inautêntico e adequação para anunciantes
- [Fichas](serie-frutas/fichas.md) — registro dos personagens, vozes e cenários aprovados

## Ciclo de um capítulo

1. Escrever o roteiro na estrutura de [`plano.md`](serie-frutas/plano.md): cold open → cena A → cena B → cena C → gancho
2. Gerar os quadros-chave usando as fichas como referência ([`prompts.md`](serie-frutas/prompts.md))
3. Animar os planos que valem a pena; o resto fica parado com voz por cima
4. Montar com as vozes fixas, os leitmotivs e os efeitos da temporada
5. Cortar o Short e montar a descrição com os scripts abaixo
6. Publicar no mesmo horário e preencher o [controle de postagem](producao/controle-postagem.md)

## Automação

```bash
./automacao/animar_still.sh quadro-07.png 4 --movimento zoom-in   # movimento sem créditos
./automacao/cortar_short.sh capitulo-07.mp4 2:14 2:38 --texto "ELA SABIA?"
python3 automacao/gerar_metadados.py serie-frutas/roteiros/cap-01-a-chegada.md
python3 automacao/gerar_thumbnail.py quadro.png "ELA SABIA" --cor roxo
```

Detalhes e limitações em [`automacao/README.md`](automacao/README.md). O `gerar_roteiro.py` e o `checklist-gravacao.md` foram feitos para o formato antigo, com gravação real, e não se aplicam à série.

## Material do canal infantil (histórico)

Formato anterior, com criança real. Mantido para referência:

- [Plano de 30 dias](agosto) e [roteiros dos dias 1 a 7](roteiros)
- [Kit de produção](producao): [checklist](producao/checklist-gravacao.md), [metadados](producao/modelo-metadados.md), [thumbnail](producao/padrao-thumbnail.md), [compliance infantil](producao/compliance.md)
- [Controle de postagem](producao/controle-postagem.md) — este continua servindo para a série
