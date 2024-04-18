import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

# Texts consts to assistant
IF_NOT_FOUND = (
    "Se a informação não estiver clara no trecho fornecido, apenas indique isso na sua resposta, ou seja,"
    " não tente inventar informações não presentes. "
)
BAD_TEXT = "Considere que o trecho pode vir de um PDF com tabelas, o que pode afetar a formatação. "
WHO_ARE_YOU = "Você é um engenheiro ambiental com a tarefa de analisar um plano municipal de saneamento básico. "


# Colors for terminal output
def orange(string):
    return "\033[38;5;208m" + string + "\033[0m"


def purple(string):
    return "\033[94m" + string + "\033[0m"


# utility functions
def num_tokens_from_messages(messages, tokens_per_message=3, tokens_per_name=1):
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens


# System and user messages for each task
def get_system_user_from_objectives(plan, component):

    what_to_do = (
        f"Identifique e liste os objetivos relacionados ao componente de {component} encontrados no "
        "plano municipal de saneamento básico fornecido"
    )

    how_to_do = "Liste apenas os objetivos relacionados a esse componente, sem incluir informações adicionais."

    system = (
        # Voce é:
        f"{WHO_ARE_YOU}"
        # Oque fazer:
        f"Sua missão é identificar e listar os objetivos relacionados ao componente de {component}. "
        # Se nao achar
        f"{IF_NOT_FOUND}"
        # Texto ruim
        f"{BAD_TEXT}"
        # Como fazer:
        "Os objetivos devem ser apresentados de forma clara e concisa, sem introduções, títulos, descrições, "
        "explicações ou comentários adicionais, isto é, apenas liste os objetivos separados por uma quebra de linha. "
        # Exemplo de resposta:
        "Exemplo de resposta: Objetivo 1\nObjetivo 2\nObjetivo 3\n..."
    )

    user = (
        # Oque fazer:
        f"{what_to_do}"
        # Variação
        f", trecho do plano que contém esta informação: ({plan})."
        # Como fazer:
        f"{how_to_do}"
    )

    user_without_plan = (
        # Oque fazer:
        f"{what_to_do}"
        # Variação
        " anteriormente."
        # Como fazer:
        f"{how_to_do}"
    )

    return system, user, user_without_plan


def get_system_user_from_deadline(plan, objective, component, year):

    what_to_do = (
        f"Encontre o prazo para o cumprimento do objetivo específico de ({objective}) do componente de {component} no "
        f"plano municipal de saneamento básico publicado em {year} fornecido"
    )

    how_to_do = "Liste apenas o prazo relacionado a esse objetivo específico, sem incluir informações adicionais."

    system = (
        # Voce é:
        f"{WHO_ARE_YOU}"
        # Oque fazer:
        "Sua missão é identificar o prazo previsto para a realização de um objetivo específico. "
        # Se nao achar
        f"{IF_NOT_FOUND}"
        # Texto ruim
        f"{BAD_TEXT}"
        # Como fazer:
        "Os prazos devem ser apresentados de forma clara e concisa, sem introduções, títulos, descrições, explicações "
        "ou comentários adicionais, isto é, apenas informe o prazo previsto (Imediato, Curto Prazo, Médio Prazo ou "
        "Longo Prazo). "
        "Se o prazo para cumprimento do objetivo for fornecido em anos e não no modelo pré definido (Imediato, "
        "Curto Prazo, Médio Prazo ou Longo Prazo), utilize o seguinte calculo a partir do ano de publicação do plano: "
        "Imediato: até 3 anos, Curto Prazo: de 4 a 8 anos, Médio Prazo: de 9 a 13 anos, Longo Prazo: acima de 13 anos."
        # Exemplo de resposta:
        "Exemplo de resposta: Curto Prazo."
    )

    user = (
        # Oque fazer:
        f"{what_to_do}"
        # Variação
        f", trecho do plano que contém esta informação: ({plan})."
        # Como fazer:
        f"{how_to_do}"
    )

    user_without_plan = (
        # Oque fazer:
        f"{what_to_do}"
        # Variação
        " anteriormente. "
        # Como fazer:
        f"{how_to_do}"
    )

    return system, user, user_without_plan


def get_system_user_from_investment(plan, objective, component):

    what_to_do = (
        f"Encontre o investimento previsto para o objetivo específico de '{objective}' do componente de {component} "
        f"no plano municipal de saneamento básico fornecido"
    )

    how_to_do = (
        "Indique apenas o valor previsto em reais para a realização desse objetivo, sem incluir informações"
        " adicionais."
    )

    system = (
        # Voce é:
        f"{WHO_ARE_YOU}"
        # Oque fazer:
        "Sua missão é identificar o investimento previsto para a realização de um objetivo específico. "
        # Se nao achar
        f"{IF_NOT_FOUND}"
        # Texto ruim
        f"{BAD_TEXT}"
        # Como fazer:
        "Os investimentos devem ser apresentados em reais e de forma clara e concisa, sem introduções, títulos, "
        "descrições, explicações, ou comentários adicionais, isto é, apenas informe o valor no formato: R$ X,XX. "
        # Exemplo de resposta:
        "Exemplo de resposta: R$ 100.000,00."
    )

    user = (
        # Oque fazer:
        f"{what_to_do}"
        # Variação
        f", trecho do plano que contém esta informação: ({plan})."
        # Como fazer:
        f"{how_to_do}"
    )

    user_without_plan = (
        # Oque fazer:
        f"{what_to_do}"
        # Variação
        " anteriormente."
        # Como fazer:
        f"{how_to_do}"
    )

    return system, user, user_without_plan


def get_system_user_from_actions(plan, objective, component):

    what_to_do = (
        f"Encontre as ações previstas para alcançar o objetivo específico de '{objective}' do componente de "
        f"{component} no plano municipal de saneamento básico fornecido"
    )

    how_to_do = "Liste apenas as ações relacionadas a esse objetivo específico, sem incluir informações adicionais."

    system = (
        # Voce é:
        f"{WHO_ARE_YOU}"
        # Oque fazer:
        "Sua missão é identificar as ações previstas para alcançar um objetivo específico. "
        # Se nao achar
        f"{IF_NOT_FOUND}"
        # Texto ruim
        f"{BAD_TEXT}"
        # Como fazer:
        "As ações devem ser apresentados de forma clara e concisa, sem introduções, títulos, descrições, explicações "
        "ou comentários adicionais, isto é, apenas liste-as separados por uma quebra de linha."
        # Exemplo de resposta:
        "Exemplo de resposta: Ação 1\nAção 2\nAção 3\n..."
    )

    user = (
        # Oque fazer:
        f"{what_to_do}"
        # Variação
        f", trecho do plano que contém esta informação: ({plan}). "
        # Como fazer:
        f"{how_to_do}"
    )

    user_without_plan = (
        # Oque fazer:
        f"{what_to_do}"
        # Variação
        " anteriormente."
        # Como fazer:
        f"{how_to_do}"
    )

    return system, user, user_without_plan
