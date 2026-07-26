# Série animada de frutas — público adulto

> Mudança de direção. O plano em `agosto/` era canal infantil com criança real.
> Este é outro produto: série animada de frutas com humor e drama de novela,
> para público adulto. O material antigo fica no repositório como histórico.

## Por que a mudança melhora o negócio

Sair do rótulo "feito para crianças" devolve tudo que o YouTube desliga em conteúdo infantil:

| | Canal infantil | Série adulta |
|---|---|---|
| Comentários | desativados | **ativos** (motor de engajamento) |
| Anúncios personalizados | desativados | **ativos** (RPM muito maior) |
| Telas finais e cards | indisponíveis | disponíveis |
| Membros, Super Thanks | indisponíveis | disponíveis |
| Sino de notificação | não dispara | dispara |
| Alvará judicial / jornada infantil | risco real | **não se aplica** |
| Privacidade da criança | risco permanente | **não se aplica** |

A meta de receita fica bem mais alcançável pela mesma quantidade de views, e some a parte mais delicada do plano anterior.

## Formato

- **Episódios de 3 a 6 min**, publicados diariamente
- **1 Short por dia**, recortado do episódio (a cena de maior reação)
- Novela: enredo contínuo, cada capítulo termina em gancho
- Tom: comédia com drama exagerado de novela. Traição, dívida, fofoca, herança, vingança — os clichês do gênero, levados a sério pelos personagens e não pelo espectador

## Elenco

Personagens originais. **Não copiar nome, design ou bordão de canais existentes do gênero** — a referência é o formato, não a identidade.

| Personagem | Arquétipo | Traço visual | Motor de conflito |
|---|---|---|---|
| **Dona Melancia** | Matriarca fofoqueira | Grande, casca listrada, avental, óculos na ponta do nariz | Sabe o segredo de todo mundo e cobra por isso |
| **Coronel Abacaxi** | O rico da vila | Coroa de folhas, terno apertado, charuto | Dono das terras, espinhoso por fora e por dentro |
| **Banana** | O galã caloteiro | Casca meio aberta como jaqueta, corrente de ouro | Deve dinheiro para todos, promete casamento para todas |
| **Abacate** | O rancoroso | Caroço rachado à mostra, olheiras | Foi traído pelo sócio e nunca superou |
| **Morango** | A mocinha ambiciosa | Pequena, brilhante, sorriso ensaiado | Finge ingenuidade enquanto arma tudo |
| **Limão** | O vilão azedo | Magro, verde-ácido, terno preto | Agiota da vila, cobra juros e favores |
| **Coco Seco** | O forasteiro | Casca dura, rachadura na testa, mala velha | Chegou para cobrar uma dívida antiga |

## Estrutura de cada capítulo

| Tempo | Bloco |
|---|---|
| 0:00-0:12 | **Cold open** — resolve pela metade o gancho do capítulo anterior. Sem intro antes. |
| 0:12-0:17 | Vinheta de 5s |
| 0:17-1:30 | **Cena A** — o conflito do dia é apresentado |
| 1:30-3:00 | **Cena B** — a reviravolta (alguém mente, alguém descobre) |
| 3:00-3:40 | **Cena C** — a consequência imediata |
| 3:40-4:00 | **Gancho** — a revelação que só se resolve amanhã |

Regra do gênero: **todo capítulo termina em um close de reação com música de suspense**. É a assinatura da novela e o que traz o espectador de volta.

## Arco de 30 dias

| Semana | Arco | Clímax |
|---|---|---|
| 1 (dias 1-7) | **A chegada** — Coco Seco desembarca na vila cobrando uma dívida antiga do Coronel Abacaxi | Descobre-se que a dívida não é do Coronel, é da Dona Melancia |
| 2 (dias 8-14) | **A dívida** — Banana se oferece para pagar em troca de um favor; Limão financia | O favor era casar com Morango |
| 3 (dias 15-21) | **A traição** — Abacate reconhece em Coco Seco o sócio que o traiu anos atrás | Abacate revela o passado no meio da festa de noivado |
| 4 (dias 22-30) | **A herança** — o Coronel adoece e o testamento some | Quem roubou o testamento fecha o mês e abre o mês 2 |

Enredo contínuo é o que diferencia a série de conteúdo gerado em lote — e o que sustenta a monetização (ver `compliance.md`).

## Produção

O pipeline completo está em `producao-ia.md`, e os prompts fixos dos personagens em `prompts.md`.

Resumo do ciclo diário:

1. Roteiro do capítulo (texto, ~400 palavras)
2. Quadros-chave gerados como imagem, usando a ficha do personagem como referência para manter consistência
3. Imagem → vídeo, plano a plano
4. Vozes por personagem
5. Trilha, efeitos e montagem
6. Corte do Short (`automacao/cortar_short.sh` continua servindo)

## O que ainda vale do material antigo

- `automacao/cortar_short.sh` — corte de Short em 9:16, serve igual
- `automacao/gerar_thumbnail.py` — mudando a paleta para as cores da série
- `automacao/gerar_metadados.py` — descrição com capítulos, serve igual
- `producao/controle-postagem.md` — a planilha e as métricas continuam válidas
- `producao/checklist-gravacao.md` — **não serve mais**, não há gravação
