import json
import tiktoken # for token counting
import numpy as np
from collections import defaultdict

#Variável global
encoding = tiktoken.get_encoding("cl100k_base")
def data_loading(path):
    #Carregando os dados
    data_path = path
    with open(data_path, 'r', encoding='utf-8') as f:
        dataset = [json.loads(line) for line in f]
    return dataset

def initial_statistics(dataset):
    # Estatísticas iniciais
    print("\n\033[94m" + "Num examples: " + "\033[0m\n", len(dataset))
    print("\n\033[38;5;208m" + "First example:" + "\033[0m")
    for message in dataset[0]["messages"]:
        print(str(message)[:100] + "...")

def search_erors(dataset):
    print("\033[94m" + "Errors:" + "\033[0m")
    format_errors = defaultdict(int)
    for ex in dataset:
        if not isinstance(ex, dict):
            format_errors["data_type"] += 1
            continue

        messages = ex.get("messages", None)
        if not messages:
            format_errors["missing_messages_list"] += 1
            continue

        for message in messages:
            if "role" not in message or "content" not in message:
                format_errors["message_missing_key"] += 1

            if any(k not in ("role", "content", "name", "function_call") for k in message):
                format_errors["message_unrecognized_key"] += 1

            if message.get("role", None) not in ("system", "user", "assistant", "function"):
                format_errors["unrecognized_role"] += 1

            content = message.get("content", None)
            function_call = message.get("function_call", None)

            if (not content and not function_call) or not isinstance(content, str):
                format_errors["missing_content"] += 1

        if not any(message.get("role", None) == "assistant" for message in messages):
            format_errors["example_missing_assistant_message"] += 1

    if format_errors:
        print("Found errors:")
        for k, v in format_errors.items():
            print(f"{k}: {v}")
    else:
        print("No errors found")

#Funções auxiliares(começa em num_tokens_from_messages)
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

def num_assistant_tokens_from_messages(messages):
    num_tokens = 0
    for message in messages:
        if message["role"] == "assistant":
            num_tokens += len(encoding.encode(message["content"]))
    return num_tokens

def print_distribution(values, name):
    print(f"\n#### Distribution of {name}:")
    print(f"min / max: {min(values)}, {max(values)}")
    print(f"mean / median: {np.mean(values)}, {np.median(values)}")
    print(f"p5 / p95: {np.quantile(values, 0.1)}, {np.quantile(values, 0.9)}")
#Final das funções auxiliares

def count_tokens_and_more_informations(dataset):
    print("\n\033[38;5;208m" + "Statistics:" + "\033[0m")
    # Warnings and tokens counts
    n_missing_system = 0
    n_missing_user = 0
    n_messages = []
    convo_lens = []
    assistant_message_lens = []

    for ex in dataset:
        messages = ex["messages"]
        if not any(message["role"] == "system" for message in messages):
            n_missing_system += 1
        if not any(message["role"] == "user" for message in messages):
            n_missing_user += 1
        n_messages.append(len(messages))
        convo_lens.append(num_tokens_from_messages(messages))
        assistant_message_lens.append(num_assistant_tokens_from_messages(messages))

    print("Num examples missing system message:", n_missing_system)
    print("Num examples missing user message:", n_missing_user)
    print_distribution(n_messages, "num_messages_per_example")
    print_distribution(convo_lens, "num_total_tokens_per_example")
    print_distribution(assistant_message_lens, "num_assistant_tokens_per_example")
    n_too_long = sum(l > 4096 for l in convo_lens)
    print(f"\n{n_too_long} examples may be over the 4096 token limit, they will be truncated during fine-tuning")
    return convo_lens#tamanho da conversa

#Estimativa de custo
def cost_estimate(dataset, convo_lens):
    # Pricing and default n_epochs estimate
    MAX_TOKENS_PER_EXAMPLE = 4096
    TARGET_EPOCHS = 3
    MIN_TARGET_EXAMPLES = 100
    MAX_TARGET_EXAMPLES = 25000
    MIN_DEFAULT_EPOCHS = 1
    MAX_DEFAULT_EPOCHS = 25
    n_epochs = TARGET_EPOCHS
    n_train_examples = len(dataset)
    if n_train_examples * TARGET_EPOCHS < MIN_TARGET_EXAMPLES:
        n_epochs = min(MAX_DEFAULT_EPOCHS, MIN_TARGET_EXAMPLES // n_train_examples)
    elif n_train_examples * TARGET_EPOCHS > MAX_TARGET_EXAMPLES:
        n_epochs = max(MIN_DEFAULT_EPOCHS, MAX_TARGET_EXAMPLES // n_train_examples)
    n_billing_tokens_in_dataset = sum(min(MAX_TOKENS_PER_EXAMPLE, length) for length in convo_lens)
    print(f"Dataset has ~{n_billing_tokens_in_dataset} tokens that will be charged for during training")
    print(f"By default, you'll train for {n_epochs} epochs on this dataset")
    print(f"By default, you'll be charged for ~{n_epochs * n_billing_tokens_in_dataset} tokens")
    dollar_value = 0.000008 * n_epochs * n_billing_tokens_in_dataset#(quantidade total de caracteres que será feita a cobrança)
    #O valor de 0.000008 foi retirado da documentação da openAI,  onde fornecem o seguinte exeplo: Se um modelo for treinado com 100.000
    #tokens na base de dados e a quantidade de épocas for 3, o valor em dólar será aproximadamente U$2,40. Com isso, fiz uma regra de três simples
    #para chegar nesse valor de 0.000008
    #Ainda não entendi se da pra obter esse valor de outra forma. Pesquisar melhor isso
    print("\n\033[38;5;208m" + "Cost estimate: "+"\033[0m" + str(dollar_value) + " U$")

if __name__ == "__main__":
    #Verificando base de treinamento
    dataset = data_loading('data_training.jsonl')
    initial_statistics(dataset)
    search_erors(dataset)
    convo_lens = count_tokens_and_more_informations(dataset)
    cost_estimate(dataset, convo_lens)
