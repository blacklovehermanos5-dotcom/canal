# Capítulo 1 — A chegada

**Arco:** semana 1, "A chegada"
**Duração alvo:** 4 min
**Cenários:** praça da vila, quitanda
**Personagens:** Coco Seco, Dona Melancia, Banana, Coronel Abacaxi

## Estrutura

| Tempo | Bloco | O que acontece |
|---|---|---|
| 0:00-0:12 | **Cold open** | Coco Seco desce do ônibus na praça vazia. Ninguém fala nada. Ele pergunta: "Onde mora o Coronel?" |
| 0:12-0:17 | Vinheta | Tema de abertura, 5s |
| 0:17-1:30 | **Cena A** | Dona Melancia vê tudo da quitanda e espalha a notícia. Banana chega curioso e finge que sabe quem é o forasteiro. |
| 1:30-3:00 | **Cena B** | Coco Seco chega ao casarão. O Coronel abre a porta, reconhece o rosto e fecha na cara dele. |
| 3:00-3:40 | **Cena C** | Dona Melancia interroga o Coronel. Ele nega tudo, nervoso demais para convencer. |
| 3:40-4:00 | **Gancho** | Coco Seco, sozinho na praça, tira um papel velho do bolso: uma dívida assinada. A assinatura **não** é do Coronel. |

## Planos

Numerados para a geração. `[A]` = animar de verdade · `[P]` = parado com pan/zoom (`automacao/animar_still.sh`)

| # | Plano | Cenário | Movimento |
|---|---|---|---|
| 1 | Praça vazia ao entardecer, ônibus velho parando | praça | [A] chegada do ônibus |
| 2 | Coco Seco descendo, mala na mão, de costas | praça | [P] zoom-in |
| 3 | Close nos olhos dele varrendo a praça | praça | [P] zoom-in-rapido |
| 4 | Dona Melancia espiando pela janela da quitanda | quitanda | [P] zoom-in |
| 5 | Banana chegando, apoiado no batente, sorriso | quitanda | [P] pan-esquerda |
| 6 | Dois planos de fofoca, Melancia gesticulando | quitanda | [P] zoom-in |
| 7 | Coco Seco subindo a rua para o casarão | praça | [P] pan-direita |
| 8 | Porta do casarão abrindo, Coronel no vão | casarão | [A] porta abrindo |
| 9 | Close do Coronel reconhecendo — pavor | casarão | [P] zoom-in-rapido |
| 10 | Porta batendo na cara de Coco Seco | casarão | [A] porta batendo |
| 11 | Coronel encostado na porta por dentro, ofegante | casarão | [P] zoom-in |
| 12 | Melancia entrando sem pedir licença | casarão | [P] pan-direita |
| 13 | Coronel negando, suando | casarão | [P] zoom-in |
| 14 | Coco Seco sozinho na praça, noite caindo | praça | [P] zoom-out |
| 15 | Close do papel na mão: a assinatura | praça | [P] zoom-in-rapido |
| 16 | Close final nos olhos dele — gancho | praça | [P] zoom-in-rapido |

**Orçamento deste capítulo:** 16 quadros em `z_image` = 2,40 créditos · 3 planos animados = 22,50 · **total ~25 créditos**

Cortando os planos animados para 1 (só a porta batendo), cai para ~10 créditos.

## Falas

**[1-3] Praça**
> **COCO SECO:** (baixo, sem olhar para ninguém) Onde é que mora o Coronel?

**[4-6] Quitanda**
> **DONA MELANCIA:** Chegou homem na vila. Com mala. *Mala*, Banana.
> **BANANA:** Ah, esse aí eu conheço.
> **DONA MELANCIA:** Conhece nada.
> **BANANA:** ...Conheço de vista.
> **DONA MELANCIA:** De vista todo mundo conhece. Some daqui.

**[7-11] Casarão**
> **CORONEL ABACAXI:** (abrindo) Pois não, quem...
> *(silêncio de dois segundos — ele reconhece)*
> **CORONEL ABACAXI:** Não. Não, não, não.
> **COCO SECO:** Vinte anos, Coronel.
> *(porta bate)*

**[12-13] Dentro do casarão**
> **DONA MELANCIA:** Quem era?
> **CORONEL ABACAXI:** Ninguém.
> **DONA MELANCIA:** O senhor tá branco.
> **CORONEL ABACAXI:** Eu sou amarelo, Melancia.
> **DONA MELANCIA:** Pois hoje o senhor tá branco.

**[14-16] Praça, noite**
> **COCO SECO:** (lendo o papel, para si) Não é ele que me deve.
> *(close na assinatura — corta)*

## Metadados

- **Título:** `CHEGOU UM ESTRANHO NA VILA 😳 | A Vila — Capítulo 1`
- **Tags:** novela animada, série animada, frutas, comédia, capítulo 1
- Público adulto — **não** marcar como "feito para crianças"
- Checklist completo em `serie-frutas/compliance.md`

## Short do dia

Planos 8-10: a porta abrindo, o reconhecimento e a porta batendo. 18s, sem contexto.

```bash
./automacao/cortar_short.sh cap-01.mp4 1:52 2:10 --texto "ELE RECONHECEU"
```
