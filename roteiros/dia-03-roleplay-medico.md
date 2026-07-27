# Dia 3 — Roleplay: Um dia como médico(a)

- **Tags:** roleplay médico, brincadeira de médico, faz de conta, hospital de brinquedo, kit médico infantil, brincadeira infantil, canal infantil, roleplay para crianças, ursinho doente, aprendendo a cuidar
- **Duração alvo:** 9 min
- **Público:** infantil
- **Short do dia:** o espirro do ursinho (bloco 4)

## Cenário e materiais

- Mesa com toalha branca = "consultório"
- Kit médico de brinquedo (estetoscópio, termômetro, seringa sem agulha)
- 4 pacientes: ursinho, boneca, dinossauro, carrinho (o "acidentado")
- Jaleco branco (camisa grande do adulto serve)
- Placa escrita "HOSPITALZINHO" feita em cartolina na frente da câmera

> Nada de material médico de verdade em cena — nem curativo usado, nem
> remédio, nem seringa real. Só brinquedo.

## Estrutura

| Tempo | Bloco | Observações |
|---|---|---|
| 0:00-0:08 | **Intro** | vinheta do canal, 8s |
| 0:08-0:45 | Abertura no consultório | mostra o jaleco e o kit, chama a criança pra brincar junto |
| 0:45-2:10 | Paciente 1: o ursinho com febre | termômetro, "38 graus!", cobertor e chá de mentirinha |
| 2:10-3:40 | O espirro do ursinho | <!-- cena do Short: cortar 2:35-3:05 --> ensina a espirrar no cotovelo |
| 3:40-5:15 | Paciente 2: a boneca com dodói no joelho | curativo de brinquedo, "sopra que sara" |
| 5:15-6:50 | Paciente 3: o dinossauro que não quer tomar vacina | medo e coragem, sem dramatizar dor |
| 6:50-8:10 | Emergência: o carrinho capotou | maca improvisada, todos ajudam |
| 8:10-8:50 | Alta dos pacientes | cada um sai com um desenho de "atestado" |
| 8:50-9:00 | Despedida e chamada | pergunta pro próximo vídeo |

## Roteiro por bloco

### Abertura (0:08)

Entra vestindo o jaleco, de costas, e vira pra câmera.

> **Doutor(a):** Bom dia! Hoje o hospitalzinho abriu e olha só quantos
> pacientes já estão na fila. Você quer ser meu ajudante? Então pega o seu
> estetoscópio aí de casa — pode ser a mão mesmo!

Mostra o kit item por item, nomeando cada um devagar (é o trecho educativo:
estetoscópio, termômetro, otoscópio).

### Paciente 1 — o ursinho com febre (0:45)

Ursinho deitado, coberto.

> **Doutor(a):** Ursinho, o que você tá sentindo? ... Ele falou baixinho no meu
> ouvido que a barriga tá quente. Vamos medir?

Coloca o termômetro. Pausa de 3 segundos olhando pra câmera — espaço pro
espectador adivinhar.

> **Doutor(a):** TRINTA E OITO! Isso é febre. Quando a gente tá com febre, o
> que precisa? Descansar, beber água e chamar um adulto.

Cobre o ursinho, oferece "chá" numa xícara de brinquedo.

### O espirro (2:10) — cena do Short

Ursinho "espirra" (efeito com a boca fora de quadro), e o algodão voa da mesa.

> **Doutor(a):** ATCHIM! Ursinho, assim não! Espirrou pra onde? No ar!
> Espirro é no cotovelo, ó — assim.

Repete o gesto três vezes, exagerado, e pede pra criança repetir junto.
Encerra com o ursinho acertando no cotovelo e todo mundo comemorando.

> Esse é o trecho do Short. Corte de 2:35 a 3:05 — a piada fecha em 30s e o
> gancho ("espirrou pra onde?") funciona sem contexto.

### Paciente 2 — dodói no joelho (3:40)

Boneca com um risco de caneta lavável no joelho.

> **Doutor(a):** Caiu andando de bicicleta? Deixa eu ver... Não é grave, viu?
> Vou limpar e colocar o curativo. Sopra comigo: uuuuuu.

Curativo de brinquedo, adesivo colorido por cima.

### Paciente 3 — o dinossauro medroso (5:15)

Dinossauro escondido atrás da caixa.

> **Doutor(a):** Sai daí, dinossauro! Você tá com medo da vacina? Todo mundo
> fica um pouquinho. Sabe o que ajuda? Contar até três e apertar a mão de
> alguém. Você conta comigo? UM... DOIS... TRÊS!

Aplica a seringa de brinquedo. O dinossauro comemora que não doeu tanto quanto
achava.

> Sem gritos e sem choro na encenação. O objetivo é tirar o medo, não fazer
> graça com ele.

### Emergência (6:50)

Barulho de batida fora de quadro. Entra correndo com o carrinho.

> **Doutor(a):** EMERGÊNCIA! O carrinho capotou na curva! Ajudante, me ajuda a
> colocar na maca!

Todos os pacientes já atendidos "ajudam" no resgate. Conserta a roda, dá o
alta.

### Alta e despedida (8:10)

Entrega um papelzinho desenhado pra cada paciente.

> **Doutor(a):** Todo mundo curado! E você, qual paciente você quis atender
> primeiro? Conta aqui embaixo. Amanhã tem desafio novo no canal — não perde!

## Depois de gravar

```bash
python3 automacao/gerar_metadados.py roteiros/dia-03-roleplay-medico.md \
    --publico infantil \
    --titulo "BRINCANDO DE MÉDICO no hospitalzinho 🏥"

python3 automacao/gerar_thumbnail.py "BRINCANDO DE MÉDICO" \
    --subtexto "o ursinho tá com febre!" --publico infantil \
    --fundo frames/dia-03-ursinho.png

automacao/cortar_short.sh videos/dia-03.mp4 --inicio 2:35 --duracao 30
```
