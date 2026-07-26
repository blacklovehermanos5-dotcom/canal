# Fichas aprovadas — referências canônicas

Registro dos assets aprovados. Toda geração nova referencia o `job_id` daqui, **nunca** redescreve o personagem do zero. Ver `prompts.md`.

## Personagens

Geradas em `z_image`, 3:4, 1536x2048, plano médio sobre fundo neutro. **Duas variações por personagem — escolha uma, apague a outra da tabela e marque ✅.** A variação escolhida vira a referência canônica e não se regera mais.

| Personagem | Variação A | Variação B | Voz | Status |
|---|---|---|---|---|
| Dona Melancia | `1d17e519-6a24-4a10-a9a1-370a3e3b87c6` | `47913cd3-acd1-4b2c-afd9-325c2fd05c83` | | ⬜ escolher |
| Coronel Abacaxi | `5d6693ca-941a-40ee-a60c-e966a51df8de` | `b533fd8b-4265-402d-ab44-741a1b7e9b5d` | | ⬜ escolher |
| Banana | `e13527ed-2104-4371-b422-be02fedf9143` | `9f16c86c-5e1a-4bbe-bf74-1a708a6a002e` | | ⬜ escolher |
| Abacate | `c86793cf-df5c-4dd7-aaa5-1d5339f0ee52` | `32976ffc-e078-4109-847f-7f6f2b0c3e5f` | | ⬜ escolher |
| Morango | `cfb5f644-d583-442c-acb6-58f0f41d2bd3` | `a537c499-3101-4744-af42-be232aa03261` | | ⬜ escolher |
| Limão | `85839caf-cd82-4cc7-a3c1-1bcd89b75b5a` | `22acd283-4924-41b3-a83d-cd66b9dd216d` | | ⬜ escolher |
| Coco Seco | `21ce0a00-5d91-4690-ae10-de8fd08f3022` | — (só 1 variação) | | ⬜ conferir |

Os prompts exatos que geraram estas fichas estão em `prompts.md`. Para regerar uma que não ficou boa, use o mesmo prompt — não reescreva a descrição, senão o personagem muda de identidade.

## Cenários

Placas de fundo vazias (sem personagem), `z_image`, 16:9, 2048x1152. Duas variações cada.

| Cenário | Variação A | Variação B | Status |
|---|---|---|---|
| Praça da vila | `9659cb2f-994f-4818-a220-e42a4c6c94ab` | `c533e388-14c1-4d3b-8caa-e06659c448ad` | ⬜ escolher |
| Quitanda da Dona Melancia | `50fa373f-8f71-4c2f-ac94-bd4bcd25b776` | `2e96cccf-0b21-447d-947f-2e9aa256fe8b` | ⬜ escolher |
| Casarão do Coronel | `71295f60-18e4-4581-94eb-31d8b2bfda47` | `684a5b81-b3e7-4f3b-b6ce-ac55f94cdb55` | ⬜ escolher |
| Beco do Limão | `9d34f8db-50a1-4db7-876a-981ce9dadc66` | `b994488d-7425-489a-9392-b7425053fb0f` | ⬜ escolher |

## Áudio

**As ferramentas de geração disponíveis nesta sessão fazem apenas voz (text-to-speech). Não há geração de música nem de efeitos sonoros.** A trilha e os efeitos precisam vir de outra fonte:

- Biblioteca de áudio do YouTube Studio (gratuita e livre de Content ID)
- Bibliotecas licenciadas (Epidemic Sound, Artlist, Uppbeat)
- Composição própria

| Item | Origem | Status |
|---|---|---|
| Tema de abertura (5s) | biblioteca licenciada | ⬜ escolher |
| Leitmotiv suspense | biblioteca licenciada | ⬜ escolher |
| Leitmotiv romance | biblioteca licenciada | ⬜ escolher |
| Leitmotiv revelação | biblioteca licenciada | ⬜ escolher |
| Vozes dos 7 personagens | TTS (gerável aqui) | ⬜ a gerar |

## Orçamento

Saldo em 26/07 após gerar fichas e cenários: **46,55 créditos**.

Custos medidos (via `get_cost`, não estimados):

| Item | Créditos |
|---|---|
| Imagem `z_image` | 0,15 |
| Imagem `nano_banana_pro` | 2,00 |
| **Vídeo `kling3_0_turbo`, 5s** | **7,50** |

O vídeo custa **50x uma imagem parada**. É o número que decide a viabilidade da série — ver `producao-ia.md`.

## Testes de estilo já feitos

Duas explorações de estilo do elenco (abacaxi + banana + abacate na praça da vila), modelo `z_image`, 2048x1152:

- `f821d41b-e361-4d9e-8c26-3caf78dba953`
- `4934bf55-9c1a-43e9-9c9e-758b6a775f1f`

Serviram para calibrar o bloco de estilo de `prompts.md`. Ainda **não** são fichas canônicas — as fichas são geradas uma por personagem, em plano médio e fundo neutro.
