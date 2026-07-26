# Pipeline de produção com IA

Um capítulo de 4 minutos tem ~25 planos. O ciclo abaixo é o que torna isso viável em algumas horas por dia.

## Etapas

### 1. Roteiro (~30 min)
400-500 palavras, na estrutura de `plano.md`: cold open → cena A → cena B → cena C → gancho. Escrever já dividido em planos numerados, com a fala de cada personagem.

### 2. Quadros-chave (~45 min)
Um plano de cada vez, sempre com a ficha do personagem como **mídia de referência** (`prompts.md`). Não redescrever o personagem no texto.

| Modelo | Créditos | Uso |
|---|---|---|
| `z_image` | 0,15 | todos os quadros de cena |
| `nano_banana_pro` | 2,00 | thumbnail e os 2-3 quadros que aparecem grandes |

25 quadros em `z_image` custam **~3,75 créditos**. Essa parte é barata.

**Sempre rode com `get_cost: true` antes de gerar em lote.**

### 3. Movimento — a decisão que define o orçamento

Aqui está o número que muda tudo: **um clipe de 5s em `kling3_0_turbo` custa 7,50 créditos — 50 vezes uma imagem parada.**

| Capítulo de 25 planos | Créditos |
|---|---|
| Todos os planos animados | **~190** |
| 6 planos animados, resto parado | ~49 |
| 2 planos animados, resto com pan/zoom | ~19 |
| Nenhum plano animado, só pan/zoom | ~4 |

Trinta capítulos com tudo animado passam de 5.600 créditos. Não é o caminho.

**A saída é pan/zoom sobre a imagem parada** — o efeito Ken Burns, que a novela usa o tempo todo em close de reação. Sai de graça, no `ffmpeg`, e no gênero fica indistinguível:

```bash
./automacao/animar_still.sh quadro-07.png 4 --movimento zoom-in
```

Reserve a animação de verdade para o que realmente precisa de movimento: a chegada de um personagem, uma porta batendo, o gancho final do capítulo. Dois ou três por episódio bastam.

### 4. Vozes (~30 min)
Uma voz fixa por personagem, definida no primeiro capítulo e nunca trocada. Guardar o identificador da voz junto do `job_id` da ficha, em `fichas.md`.

Tom do gênero: exagerado, pausado, com respiração dramática. Voz neutra demais mata a piada.

### 5. Trilha e efeitos (~20 min)

**Não são geráveis com as ferramentas desta sessão** — a geração de áudio disponível aqui faz apenas voz (text-to-speech), não música nem efeito sonoro. A trilha vem de:

- **Biblioteca de áudio do YouTube Studio** — gratuita, livre de Content ID, resolve o começo
- Bibliotecas licenciadas (Epidemic Sound, Artlist, Uppbeat) quando o canal justificar a assinatura

Escolher de uma vez e reutilizar em toda a temporada:
- 1 tema de abertura (5s, usado na vinheta)
- 3 leitmotivs: suspense, romance, revelação
- Efeitos: batida de porta, vidro quebrando, trovão, "tan-tan-tan" de novela

Trilha repetida é característica do gênero, não defeito. **Nunca** usar trilha de novela comercial: o Content ID reivindica e a receita do capítulo vai embora.

### 6. Montagem e corte (~1 h)
Montar no editor, exportar em 1080p, depois:

```bash
./automacao/cortar_short.sh capitulo-07.mp4 2:14 2:38 --texto "ELA SABIA?"
python3 automacao/gerar_metadados.py serie-frutas/roteiros/cap-07.md
```

## Consistência: o que quebra a série

| Erro | Consequência |
|---|---|
| Regerar a ficha do personagem no meio da temporada | O público percebe na hora e o vínculo cai |
| Trocar a voz de um personagem | Pior que trocar o rosto |
| Mudar o bloco de estilo entre capítulos | A série parece feita por pessoas diferentes |
| Animar todos os planos | Custo insustentável, sem ganho de retenção |

## Ritmo realista

Não tente publicar diariamente desde o dia 1. Sugestão:

- **Semana 1-2:** produzir 10 capítulos antes de publicar o primeiro
- **A partir daí:** publicar 1 por dia enquanto produz 1 por dia, mantendo os 10 de reserva
- O banco de reserva é o que evita o buraco de publicação quando um capítulo dá errado

Um capítulo leva ~4 h no começo e cai para ~2 h depois que as fichas, vozes e cenários estão prontos e reutilizáveis.
