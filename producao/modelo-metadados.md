# Modelo de metadados

Este é o contrato entre o roteiro e o `automacao/gerar_metadados.py`. O script
lê o roteiro em markdown e devolve título, descrição, capítulos, tags e
checklist prontos para colar no YouTube. Se o roteiro seguir o formato abaixo,
o gerador funciona sozinho.

## O que o roteiro precisa ter

### 1. Título como primeiro heading

```markdown
# Dia 3 — Roleplay: Um dia como médico(a)
```

É o nome interno do capítulo, usado só para você se achar na saída do script.
O título público do vídeo vai em `--titulo`.

### 2. Linha de tags

```markdown
- **Tags:** roleplay médico, brincadeira infantil, faz de conta, kids
```

Uma linha só, separada por vírgula. As **3 primeiras** viram hashtag na
descrição — o YouTube ignora o que passa disso, então coloque as mais
importantes na frente. Os acentos são removidos automaticamente
(`roleplay médico` → `#roleplaymedico`).

### 3. Seção `## Estrutura`

```markdown
## Estrutura

| Tempo | Bloco | Observações |
|---|---|---|
| 0:00-0:08 | Intro | vinheta |
| 0:08-1:30 | Chegada ao consultório | apresenta o cenário |
| 1:30-4:00 | Primeiro paciente | cena principal |
```

O timecode **de início** de cada linha vira um capítulo. Regras que o script
aplica sozinho:

- blocos chamados `Intro` ou `Vinheta` são descartados — capítulo de 8s só
  polui a lista;
- `**negrito**`, `` `código` `` e comentários `<!-- -->` são limpos do nome do
  bloco;
- o formato precisa ser `0:00-0:15` (início e fim). Linha fora desse padrão é
  ignorada em silêncio, então confira se o número de capítulos bate.

O YouTube só liga os capítulos se houver **pelo menos 3**, o primeiro começar
em `0:00` e cada um durar **10s ou mais**. Como a intro é descartada, comece o
segundo bloco em `0:00` se quiser os capítulos ativos — ou aceite que eles
sirvam só de índice visual.

## Como rodar

```bash
# formato adulto (padrão do canal hoje)
python3 automacao/gerar_metadados.py roteiros/dia-03-roleplay-medico.md \
    --titulo "ELA DESCOBRIU A VERDADE no hospital 🏥"

# formato infantil
python3 automacao/gerar_metadados.py roteiros/dia-03-roleplay-medico.md \
    --publico infantil \
    --titulo "BRINCANDO DE MÉDICO no hospital de mentirinha 🏥"
```

## Título

Fórmula: **AÇÃO em caixa alta + tema + emoji**.

- Limite prático de **60 caracteres** — acima disso o celular corta, e é lá que
  está a maior parte da audiência. O script avisa quando você passa.
- A palavra-chave principal nos primeiros 30 caracteres.
- Caixa alta só no verbo/ação, não na frase inteira: o YouTube trata título
  todo em maiúsculas como sinal de clickbait.

## Descrição

A ordem importa — os **primeiros 150 caracteres** aparecem na busca e no card
de sugestão, antes do "mostrar mais".

1. **Duas frases de abertura** com a palavra-chave principal. O script imprime
   os colchetes `[Frase 1: ...]` como lembrete; substitua antes de colar.
2. **Rodapé fixo** do público escolhido (inscrição, playlist ou aviso infantil
   + bloco de afiliados).
3. **⏱️ CAPÍTULOS** gerados da tabela.
4. **Hashtags** (3, tiradas das tags).

### Aviso de afiliado

O bloco 🛒 do molde infantil já traz a frase exigida ("podemos receber comissão
pelas compras, sem custo adicional para você"). **Se não houver link de
afiliado no vídeo, apague o bloco inteiro** — deixar o aviso sem link confunde
o espectador, e deixar o link sem aviso é problema com a plataforma e com o
CONAR.

## Tags

10 a 15 tags, da mais específica para a mais genérica. As tags têm peso baixo
no algoritmo hoje; servem principalmente para corrigir grafias e apanhar
buscas por variação do nome. Não repita a mesma tag em singular e plural.

## Antes de publicar

O script fecha com o checklist do público escolhido. Dois itens merecem
atenção porque não dá para desfazer depois sem custo:

- **"Feito para crianças"** — marcar isso desliga comentários, sino de
  notificação e anúncios personalizados (RPM menor). Marcar errado é violação
  do COPPA. O molde `infantil` pede para marcar; o `adulto` pede para **não**
  marcar. Escolha o molde certo na hora de gerar.
- **Declaração de conteúdo sintético** — obrigatória se houver voz ou imagem
  gerada por IA que possa passar por real.
