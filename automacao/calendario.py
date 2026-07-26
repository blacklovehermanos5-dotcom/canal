"""Calendário de 30 dias — fonte única de verdade.

Espelha a tabela do arquivo `agosto`. Os outros scripts leem daqui, então
mudar o calendário em um lugar só propaga para roteiros e metadados.
"""

# formato: usado para escolher a estrutura de blocos do roteiro
UNBOXING = "unboxing"
ROLEPLAY = "roleplay"
DESAFIO = "desafio"
EDUCATIVO = "educativo"
VLOG = "vlog"
ESPECIAL = "especial"

CALENDARIO = [
    (1, ESPECIAL, "Vídeo de apresentação: quem somos, o que vamos fazer", "Teaser do canal"),
    (2, UNBOXING, "Unboxing de brinquedo novo", "Melhor momento do unboxing"),
    (3, ROLEPLAY, "Um dia como médico(a)", "Cena engraçada isolada"),
    (4, DESAFIO, "Desafio simples (não rir)", "Reação em close"),
    (5, EDUCATIVO, "Aprendendo cores e números com brincadeira", "Trecho didático rápido"),
    (6, ROLEPLAY, "Mercado/restaurante de mentirinha", "Bastidor"),
    (7, VLOG, "Passeio no parque", "Melhor cena do passeio"),
    (8, UNBOXING, "Unboxing + montagem de brinquedo", "Timelapse da montagem"),
    (9, ROLEPLAY, "Ajudando a mamãe/papai", "Cena fofa"),
    (10, DESAFIO, "Desafio de comida (saudável vs. não saudável)", "Reação ao sabor"),
    (11, EDUCATIVO, "Aprendendo formas e tamanhos brincando", "Trecho educativo"),
    (12, ROLEPLAY, "Veterinário com bichinhos de pelúcia", "Cena com o paciente"),
    (13, VLOG, "Rotina da manhã", "Trecho acelerado da rotina"),
    (14, UNBOXING, "Unboxing temático (caixa de surpresas)", "Reação de surpresa"),
    (15, ESPECIAL, "Marco da 2ª semana: colab com outra criança", "Bastidor da colab"),
    (16, ROLEPLAY, "Escolinha de faz de conta", "Cena engraçada"),
    (17, DESAFIO, "Desafio de habilidade (equilíbrio, memória)", "Melhor tentativa"),
    (18, EDUCATIVO, "Aprendendo hábitos (escovar dente, lavar mão)", "Trecho didático"),
    (19, ROLEPLAY, "Salão de beleza/cabeleireiro", "Antes e depois"),
    (20, VLOG, "Brincadeira ao ar livre", "Cena de ação"),
    (21, UNBOXING, "Unboxing + teste do brinquedo em uso", "Teste em ação"),
    (22, ROLEPLAY, "Bombeiro/policial (profissões)", "Cena de resgate"),
    (23, DESAFIO, "Desafio em dupla com irmão/amigo", "Momento de disputa"),
    (24, EDUCATIVO, "Aprendendo animais e sons", "Trecho fofo com imitações"),
    (25, ROLEPLAY, "Aniversário de mentirinha", "Cena da festa"),
    (26, VLOG, "Preparando uma receita simples e segura", "Timelapse da receita"),
    (27, UNBOXING, "Unboxing surpresa (caixa misteriosa)", "Reação ao abrir"),
    (28, ROLEPLAY, "Sonhos / profissão dos sonhos", "Cena marcante"),
    (29, DESAFIO, "Desafio final do mês (compilação)", "Melhores momentos"),
    (30, ESPECIAL, "Retrospectiva do mês + enquete", "Bloopers/bastidores"),
]


def get_dia(numero):
    """Retorna (dia, formato, tema, short) ou levanta ValueError."""
    for entrada in CALENDARIO:
        if entrada[0] == numero:
            return entrada
    raise ValueError(f"Dia {numero} não existe no calendário (use 1-30)")


def slug(texto):
    """Converte um tema em nome de arquivo seguro."""
    import re
    import unicodedata

    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii").lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto).strip("-")
    return re.sub(r"-+", "-", texto)[:40]
