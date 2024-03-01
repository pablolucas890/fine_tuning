import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

MAX_TOKENS_PER_EXAMPLE = 4096


def orange(string):
    return "\033[38;5;208m" + string + "\033[0m"


# pylint: disable-next=redefined-outer-name
def num_tokens_from_messages(messages, tokens_per_message=3, tokens_per_name=1):
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for index, value in message.items():
            num_tokens += len(encoding.encode(value))
            if index == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens


if __name__ == "__main__":

    with open("data/plan_actions.txt", encoding="utf-8") as f:
        plan_actions = f.read()
    with open("data/plan_objectives_and_deadlines.txt", encoding="utf-8") as f:
        plan_objectives_and_deadlines = f.read()

    SYSTEM = (
        "Você é um engenheiro ambiental e precisa identificar os objetivos do componente  de um plano"
        + " municipal de saneamento básico. "
        "Se a informação não estiver clara no trecho fornecido, indique que não é possível determinar os objetivos. "
        "Considere que o trecho pode vir de um PDF com tabelas, o que pode afetar a formatação. "
        "Os objetivos devem ser apresentados de forma clara e concisa, sem introduções, títulos, descrições,"
        + " explicações ou comentários adicionais, isto é, apenas liste os objetivos separados por uma quebra de linha"
    )
    USER_1 = (
        "Identifique e liste apenas os objetivos relacionados ao componente  encontrados no trecho do"
        + " plano municipal de saneamento básico fornecido. "
        f"Trecho do plano: '{plan_actions}'. Evite adicionar comentários ou explicações extras."
    )
    USER_2 = (
        "Identifique e liste apenas os objetivos relacionados ao componente  encontrados no trecho do"
        + " plano municipal de saneamento básico fornecido. "
        f"Trecho do plano: '{plan_objectives_and_deadlines}'. Evite adicionar comentários ou explicações extras."
    )

    messages_1 = []
    messages_1.append({"role": "system", "content": SYSTEM})
    messages_1.append({"role": "user", "content": USER_1})

    messages_2 = []
    messages_2.append({"role": "system", "content": SYSTEM})
    messages_2.append({"role": "user", "content": USER_2})

    tokens_1 = num_tokens_from_messages(messages_1)
    tokens_2 = num_tokens_from_messages(messages_2)

    print(f"Number of tokens in plan_actions: {orange(str(tokens_1))}")
    print(f"Number of tokens in plan_objectives_and_deadlines: {orange(str(tokens_2))}")

    if tokens_1 > MAX_TOKENS_PER_EXAMPLE:
        print(
            f"Warning: the plan_actions has {orange(str(tokens_1))} tokens, which is over the"
            + f" {orange(str(MAX_TOKENS_PER_EXAMPLE))} token limit"
        )
    if tokens_2 > MAX_TOKENS_PER_EXAMPLE:
        print(
            f"Warning: the plan_objectives_and_deadlines has {orange(str(tokens_2))} tokens, which is over the"
            + f" {orange(str(MAX_TOKENS_PER_EXAMPLE))} token limit"
        )
