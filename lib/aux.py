import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")


def orange(string):
    return "\033[38;5;208m" + string + "\033[0m"


def purple(string):
    return "\033[94m" + string + "\033[0m"


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


def get_system_user_from_objectives(plan, component):

    system = (
        f"Você é um engenheiro ambiental e precisa identificar os objetivos do componente '{component}' de um plano"
        " municipal de saneamento básico. "
        "Se a informação não estiver clara no trecho fornecido, indique que não é possível determinar os objetivos. "
        "Considere que o trecho pode vir de um PDF com tabelas, o que pode afetar a formatação. "
        "Os objetivos devem ser apresentados de forma clara e concisa, sem introduções, títulos, descrições,"
        " explicações ou comentários adicionais, isto é, apenas liste os objetivos separados por uma quebra de linha"
    )

    user = (
        f"Identifique e liste apenas os objetivos relacionados ao componente '{component}' encontrados no trecho do"
        + " plano municipal de saneamento básico fornecido. "
        f"Trecho do plano: '{plan}'. Evite adicionar comentários ou explicações extras."
    )

    user_without_plan = (
        f"Identifique e liste apenas os objetivos relacionados ao componente '{component}' encontrados "
        + " no trecho do plano municipal de saneamento básico fornecido. "
    )

    return system, user, user_without_plan


def get_system_user_from_deadline(plan, objective, component, year):

    system = (
        "Você é um engenheiro ambiental com a tarefa de analisar um plano municipal de saneamento básico. "
        "Sua missão é identificar o prazo previsto para a realização de um objetivo específico. "
        "Os prazos devem ser apresentados de forma clara e concisa, sem introduções, títulos, descrições, explicações"
        " ou comentários adicionais, isto é, apenas informe o prazo previsto (Imediato, Curto Prazo, Médio Prazo ou"
        " Longo Prazo). "
        "Se o prazo para cumprimento do objetivo for fornecido em anos e não no modelo pré definido (Imediato,"
        " Curto Prazo, Médio Prazo ou Longo Prazo), utilize o seguinte calculo a partir do ano de publicação do plano: "
        "Imediato: até 3 anos, Curto Prazo: de 4 a 8 anos, Médio Prazo: de 9 a 13 anos, Longo Prazo: acima de 13 anos."
    )

    user = (
        f"Encontre o prazo para o objetivo específico '{objective}' do componente de '{component}' no seguinte trecho"
        f" do plano municipal de saneamento básico publicado em {year}: '{plan}'. "
        "Liste apenas o prazo relacionado a esse objetivo específico, sem incluir informações adicionais."
    )

    user_without_plan = (
        f"Encontre o prazo para o objetivo específico '{objective}' do componente de '{component}' no plano municipal"
        " de saneamento básico fornecido. "
        "Liste apenas o prazo relacionado a esse objetivo específico, sem incluir informações adicionais."
    )

    return system, user, user_without_plan


def get_system_user_from_actions(plan, objective, component):

    system = (
        "Você é um engenheiro ambiental com a tarefa de analisar um plano municipal de saneamento básico. "
        "Sua missão é identificar as ações previstas para alcançar um objetivo específico. "
        "Considere que o trecho fornecido pode conter informações em formatos variados, incluindo tabelas, devido à"
        " origem em um PDF. "
        "Se as ações não estiverem claras ou não forem mencionadas, indique isso na sua resposta. "
        "As ações devem ser apresentados de forma clara e concisa, sem introduções, títulos, descrições, explicações"
        " ou comentários adicionais, isto é, apenas liste-as separados por uma quebra de linha."
    )

    user = (
        f"Encontre as ações previstas para alcançar o objetivo específico '{objective}' do componente de '{component}'"
        f" no seguinte trecho do plano municipal de saneamento básico: '{plan}'. "
        "Liste apenas as ações relacionadas a esse objetivo específico, sem incluir informações adicionais."
    )

    user_without_plan = (
        f"Encontre as ações previstas para alcançar o objetivo específico '{objective}' do componente de '{component}'"
        " no trecho do plano municipal de saneamento básico fornecido. "
        "Liste apenas as ações relacionadas a esse objetivo específico, sem incluir informações adicionais."
    )

    return system, user, user_without_plan
