#!/usr/bin/env python3
"""Gera o esqueleto de roteiro de um dia do calendário.

    python3 automacao/gerar_roteiro.py 12
    python3 automacao/gerar_roteiro.py 8 --saida roteiros/

O roteiro sai com a estrutura de blocos do formato (unboxing, roleplay,
desafio, educativo, vlog), timecodes, planos de câmera, receita do Short e
metadados. O que fica em branco é o que só você sabe: os materiais
específicos e as falas. O esqueleto é o que consome tempo, não o recheio.
"""

import argparse
import sys
from pathlib import Path

from calendario import (
    DESAFIO,
    EDUCATIVO,
    ESPECIAL,
    ROLEPLAY,
    UNBOXING,
    VLOG,
    get_dia,
    slug,
)

# Cada bloco: (inicio_seg, fim_seg, titulo, descricao)
ESTRUTURAS = {
    UNBOXING: [
        (0, 15, "**Gancho**", "Já com a caixa nas mãos: \"Olha o que chegou!\" — chacoalhar perto do ouvido"),
        (15, 25, "Intro", "Vinheta 5s"),
        (25, 90, "Adivinhação", "Pistas antes de abrir + \"escreve aí embaixo o que você acha que é!\""),
        (90, 240, "**Abertura**", "Abrir devagar, close nas mãos, reação genuína. NUNCA cortar este bloco."),
        (240, 360, "Montagem / primeiro contato", "Montar ou ligar, mostrar o que cada parte faz"),
        (360, 570, "**Brincando de verdade**", "Brincadeira com começo, meio e fim usando o brinquedo. É o bloco que segura retenção."),
        (570, 630, "Nota final + gancho", "Dar nota ao brinquedo + anunciar o vídeo de amanhã"),
        (630, 660, "Encerramento", "Bordão + gesto fixo"),
    ],
    ROLEPLAY: [
        (0, 15, "**Gancho**", "Já em personagem, no meio da ação"),
        (15, 25, "Intro", "Vinheta 5s"),
        (25, 90, "**Ato 1 — Setup**", "Montar o cenário, vestir o figurino, apresentar os objetos um a um"),
        (90, 270, "**Ciclo 1** — o direto", "Primeiro caso/cliente. Ciclo completo: problema → descoberta → solução. Estabelece a fórmula."),
        (270, 450, "**Ciclo 2** — o engraçado", "Mesma estrutura, situação cômica. Esta é a cena que vira o Short."),
        (450, 630, "**Virada**", "Elemento surpresa (alguém da família entra, algo dá errado). Reacende a atenção no minuto 8."),
        (630, 720, "Desfecho", "Tudo resolvido + fala educativa curta e leve"),
        (720, 750, "Gancho + encerramento", "Anunciar o vídeo de amanhã + bordão"),
    ],
    DESAFIO: [
        (0, 15, "**Gancho**", "Mostrar o momento da derrota/vitória, sem contexto"),
        (15, 25, "Intro", "Vinheta 5s"),
        (25, 75, "Regras", "Explicar: quantas vidas, como pontua, qual o prêmio"),
        (75, 450, "**Rodadas**", "8-10 tentativas de 30-45s. Placar atualizado a cada rodada — é o que cria micro-gancho a cada 40s."),
        (450, 510, "Rodada final", "A \"arma secreta\", guardada para o fim"),
        (510, 555, "Resultado + prêmio", "Anunciar vencedor e entregar o prêmio"),
        (555, 585, "Gancho + encerramento", "Anunciar o vídeo de amanhã + bordão"),
    ],
    EDUCATIVO: [
        (0, 15, "**Gancho**", "Um problema a resolver: \"tudo se misturou, preciso de ajuda!\""),
        (15, 25, "Intro", "Vinheta 5s"),
        (25, 210, "**Conceito A**", "Um por vez: mostrar → nomear devagar → repetir 3x → pausa de 2-3s olhando pra câmera"),
        (210, 390, "**Conceito B**", "Mesma mecânica com o segundo conceito"),
        (390, 510, "**Jogo final**", "Junta os dois conceitos em 4-5 rodadas rápidas"),
        (510, 540, "Revisão", "Repetir rápido tudo que foi aprendido — a repetição fecha o aprendizado"),
        (540, 570, "Gancho + encerramento", "Anunciar o vídeo de amanhã + bordão"),
    ],
    VLOG: [
        (0, 15, "**Gancho**", "Já no meio da melhor cena do dia"),
        (15, 25, "Intro", "Vinheta 5s"),
        (25, 90, "Saída de casa", "\"Hoje a gente vai...\" — preparar, mostrar o que vai levar"),
        (90, 150, "Chegada", "Primeira visão do lugar, escolher por onde começar"),
        (150, 420, "**Blocos de atividade**", "4-5 blocos curtos, cada um com um mini-objetivo declarado"),
        (420, 510, "Momento calmo", "Lanche/conversa sobre o que foi mais legal. O contraste de ritmo segura o vídeo."),
        (510, 570, "Última atividade", "Voltar ao pico antes de encerrar"),
        (570, 600, "Gancho + encerramento", "Anunciar o vídeo de amanhã + bordão"),
    ],
    ESPECIAL: [
        (0, 15, "**Gancho**", "Energia máxima, direto na ação, sem intro antes"),
        (15, 25, "Intro", "Vinheta 5s"),
        (25, 120, "Contexto", "Por que este vídeo é diferente dos outros"),
        (120, 400, "**Bloco principal**", "O conteúdo central do especial"),
        (400, 560, "Bloco secundário", "Complemento / participação de convidado"),
        (560, 620, "Chamada para ação", "Enquete, pergunta nos comentários do adulto, anúncio do que vem"),
        (620, 650, "Encerramento", "Bordão + gesto fixo"),
    ],
}

CAMERAS = {
    UNBOXING: [
        "Plano médio fixo (base)",
        "**Close cenital** (câmera de cima da mesa) para as mãos abrindo — plano mais importante",
        "Close de rosto para a reação",
    ],
    ROLEPLAY: [
        "Plano aberto do cenário montado",
        "Close da ação principal (o exame, o pagamento, o conserto)",
        "Close de reação a cada virada",
    ],
    DESAFIO: [
        "Dois enquadramentos: um no rosto de quem resiste, um no provocador",
        "Close obrigatório no instante da reação",
        "Plano do placar entre rodadas",
    ],
    EDUCATIVO: [
        "Plano cenital dos objetos na mesa/chão (principal)",
        "Close de cada objeto no momento em que é nomeado",
        "Plano médio da criança falando com a câmera",
    ],
    VLOG: [
        "Câmera na mão, seguindo a ação",
        "Plano aberto do lugar na chegada",
        "Close de reação nos melhores momentos",
    ],
    ESPECIAL: [
        "Plano médio fixo (base)",
        "Plano aberto do cenário completo",
        "Closes de reação",
    ],
}

DURACAO_ALVO = {
    UNBOXING: "8-12 min",
    ROLEPLAY: "10-14 min",
    DESAFIO: "8-10 min",
    EDUCATIVO: "8-10 min",
    VLOG: "8-12 min",
    ESPECIAL: "8-12 min",
}

TAGS = {
    UNBOXING: "unboxing, abrindo brinquedo, brinquedo novo, review de brinquedo",
    ROLEPLAY: "faz de conta, roleplay infantil, brincando de faz de conta",
    DESAFIO: "desafio infantil, desafio para crianças, brincadeira em família",
    EDUCATIVO: "vídeo educativo infantil, aprender brincando",
    VLOG: "vlog infantil, rotina infantil, dia a dia",
    ESPECIAL: "canal infantil, vídeo especial",
}

TAGS_FIXAS = "vídeo para crianças, canal infantil, brincadeira infantil"


def mmss(segundos):
    return f"{segundos // 60}:{segundos % 60:02d}"


def gerar(dia_num):
    dia, formato, tema, short = get_dia(dia_num)
    blocos = ESTRUTURAS[formato]

    linhas = [
        f"# Dia {dia} — {tema}",
        "",
        f"**Formato:** {formato}",
        f"**Duração alvo:** {DURACAO_ALVO[formato]}",
        "**Objetivo:** <!-- o que este vídeo precisa entregar -->",
        "",
        "## Materiais",
        "- <!-- listar tudo, separar na véspera -->",
        "- ",
        "- ",
        "",
        "## Estrutura",
        "",
        "| Tempo | Bloco | O que acontece |",
        "|---|---|---|",
    ]

    for inicio, fim, titulo, descricao in blocos:
        linhas.append(f"| {mmss(inicio)}-{mmss(fim)} | {titulo} | {descricao} |")

    linhas += [
        "",
        "## Planos de câmera",
    ]
    linhas += [f"- {c}" for c in CAMERAS[formato]]

    linhas += [
        "",
        "## Short do dia",
        f"{short}. Máximo 30s, 9:16, legenda grande, corte seco, sem intro.",
        "",
        "Timecodes no vídeo longo: `__:__` a `__:__`",
        "",
        "## Metadados",
        f"- **Título:** `<!-- AÇÃO em caixa alta + tema + emoji, até 60 caracteres -->`",
        f"- **Tags:** {TAGS[formato]}, {TAGS_FIXAS}",
        "- Marcar como **\"feito para crianças\"** (ver `producao/compliance.md`)",
        "",
        "## Checagem de segurança",
        "- [ ] Sem endereço, escola, uniforme ou fachada de casa no quadro",
        "- [ ] Sem outra criança sem autorização dos responsáveis",
        "- [ ] Nada perigoso, assustador ou constrangedor para a criança",
        "",
    ]
    return "\n".join(linhas), f"dia-{dia:02d}-{slug(tema)}.md"


def main():
    p = argparse.ArgumentParser(description="Gera esqueleto de roteiro a partir do calendário")
    p.add_argument("dia", type=int, help="número do dia (1-30)")
    p.add_argument("--saida", default="roteiros", help="pasta de destino (padrão: roteiros)")
    p.add_argument("--forcar", action="store_true", help="sobrescrever arquivo existente")
    args = p.parse_args()

    try:
        conteudo, nome = gerar(args.dia)
    except ValueError as e:
        sys.exit(f"erro: {e}")

    destino = Path(args.saida) / nome
    if destino.exists() and not args.forcar:
        sys.exit(f"erro: {destino} já existe (use --forcar para sobrescrever)")

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")
    print(f"criado: {destino}")


if __name__ == "__main__":
    main()
