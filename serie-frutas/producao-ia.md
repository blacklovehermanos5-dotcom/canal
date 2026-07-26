# Pipeline de produção com IA

Um capítulo de 4 minutos tem ~25 planos. O ciclo abaixo é o que torna isso viável em algumas horas por dia.

## Etapas

### 1. Roteiro (~30 min)
400-500 palavras, na estrutura de `plano.md`: cold open → cena A → cena B → cena C → gancho. Escrever já dividido em planos numerados, com a fala de cada personagem.

### 2. Quadros-chave (~45 min)
Um plano de cada vez, sempre com a ficha do personagem como **mídia de referência** (`prompts.md`). Não redescrever o personagem no texto.

Custo aproximado por imagem, para dimensionar:

| Modelo | Créditos | Uso |
|---|---|---|
| `z_image` | ~0,15 | exploração, quadros secundários |
| `nano_banana_pro` | ~2 | quadro de abertura, thumbnail, arte que aparece grande |

Com ~25 planos, um capítulo feito só em `z_image` custa por volta de 4 créditos. Use o modelo caro só nos 2-3 quadros que aparecem grandes.

**Sempre rode com `get_cost: true` antes de gerar em lote** — os preços mudam por modelo e um lote errado queima o saldo.

### 3. Imagem → vídeo (~1 h)
Cada quadro-chave vira um plano de 3-5s. No prompt, descrever apenas o movimento de câmera e a micro-expressão.

Planos parados com voz por cima também funcionam no gênero — não anime tudo. Alternar plano animado e plano parado corta o custo pela metade e ainda parece novela.

### 4. Vozes (~30 min)
Uma voz fixa por personagem, definida no primeiro capítulo e nunca trocada. Guardar o identificador da voz junto do `job_id` da ficha, em `fichas.md`.

Tom do gênero: exagerado, pausado, com respiração dramática. Voz neutra demais mata a piada.

### 5. Trilha e efeitos (~20 min)
- 1 tema de abertura (5s, usado na vinheta)
- 3 leitmotivs: suspense, romance, revelação
- Efeitos: batida de porta, vidro quebrando, trovão, "tan-tan-tan" de novela

Gerar uma vez e reutilizar em toda a temporada. Trilha repetida é característica do gênero, não defeito.

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
