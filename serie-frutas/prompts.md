# Prompts fixos — bíblia visual da série

O maior problema de série animada gerada por IA é **consistência**: o personagem muda de cara entre um plano e outro e a série perde credibilidade. A solução é sempre a mesma:

1. Gerar **uma ficha canônica** por personagem, escolher a melhor e guardar o `job_id`
2. Em toda geração seguinte, passar esse `job_id` como **mídia de referência**, nunca redescrever o personagem do zero
3. Só variar expressão, ângulo e cenário no texto do prompt

## Bloco de estilo (colar em TODO prompt)

```
Stylized 3D animated cartoon render, Pixar-like glossy surfaces, expressive
human-like eyes and eyebrows, warm saturated tropical palette, dramatic
telenovela lighting with strong key light and deep shadows, shallow depth of
field, cinematic composition, high detail, series still frame
```

## Fichas de personagem

Gerar cada uma em 1:1 ou 4:3, plano médio, fundo neutro. Guardar o `job_id` da melhor.

### Dona Melancia
```
A large watermelon character with a striped green rind body, expressive
elderly face with reading glasses perched on the nose, floral apron, arms
crossed, knowing smug half-smile, matriarch energy
```

### Coronel Abacaxi
```
An arrogant pineapple character, spiky golden body, crown of stiff leaves
styled like slicked-back hair, tight formal suit jacket straining at the
buttons, cigar in one hand, raised eyebrow, wealthy landowner energy
```

### Banana
```
A smug banana character, peel opening downward like an unbuttoned jacket,
thick gold chain, slicked hair curl at the tip, charming untrustworthy grin,
one eyebrow raised, small-time charmer energy
```

### Abacate
```
A bitter avocado character, dark green textured skin, a large cracked pit
visible in the chest like an old wound, heavy eye bags, permanent scowl,
resentful and tired energy
```

### Morango
```
A small strawberry character, glossy red body with seed freckles, delicate
green leaf hair, rehearsed innocent smile that does not reach the eyes,
calculating ingenue energy
```

### Limão
```
A sour lime character, thin angular green body, sharp narrow eyes, black
tailored suit, thin ledger book under one arm, cold predatory calm,
loan-shark villain energy
```

### Coco Seco
```
A weathered coconut character, hard brown fibrous shell, a deep crack across
the forehead like a scar, dusty travel coat, old suitcase in hand, silent
menacing stranger energy
```

## Cenários recorrentes

Gerar uma vez cada e reutilizar como referência de fundo.

| Cenário | Prompt |
|---|---|
| Praça da vila | `sunlit tropical village square, small colorful stucco houses, cobblestone, a dry fountain in the center, hanging laundry lines, late afternoon golden light` |
| Quitanda da Dona Melancia | `cluttered small grocery shop interior, wooden crates, hanging scales, dim warm light through a dusty window, gossip corner` |
| Casarão do Coronel | `opulent but faded colonial mansion interior, dark wood, heavy curtains, oil portraits on the wall, single dramatic window light` |
| Beco do Limão | `narrow dark alley at night, single flickering lamp, wet cobblestone, deep shadows, threatening mood` |

## Prompts de expressão (para os closes de gancho)

O fim de todo capítulo é um close de reação. Reaproveitar:

```
extreme close-up on [PERSONAGEM], eyes widening in shock, slow dramatic
zoom, telenovela suspense lighting, dark vignette
```

Variações: `narrowing eyes in suspicion` · `tears welling up` · `slow furious
realization` · `smug satisfied smirk`

## Imagem → vídeo

Descrever **só o movimento**, nunca redescrever o personagem — a imagem de origem já o define:

```
slow push-in on the character, subtle head turn toward camera, eyebrows
rising, fabric and leaves shifting slightly, cinematic camera movement
```

## Regras que evitam retrabalho

- **Uma ficha por personagem, para sempre.** Regerar a ficha no meio da temporada quebra a continuidade visual.
- **Mesmo bloco de estilo em tudo**, inclusive nos cenários.
- **Nunca** descrever o personagem por escrito quando a referência já está anexada — o texto compete com a imagem e o resultado desanda.
- Guardar os `job_id` em `serie-frutas/fichas.md` conforme forem aprovados.
- Não usar o nome, o design nem o bordão de personagens de canais existentes do gênero.
