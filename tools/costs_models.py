from collections import defaultdict
import json
import sys
import tiktoken
import numpy as np

sys.path.append("/".join(__file__.split("/")[0:-2]))
# pylint: disable-next=wrong-import-position
from lib.aux import purple, orange, num_tokens_from_messages

with open("cfg.json", encoding="utf-8") as f:
    tokens_limit = json.load(f)["tokens_limit"]

encoding = tiktoken.get_encoding("cl100k_base")


def data_loading(path):
    data_path = path
    with open(data_path, "r", encoding="utf-8") as file:
        data = [json.loads(line) for line in file]
    return data


def initial_statistics(data):
    print("\n" + purple("Num examples: ") + "\n", len(data))
    print("\n" + orange("First example:"))
    for message in data[0]["messages"]:
        print(str(message)[:100] + "...")


def search_erors(data):
    print(purple("Errors:"))
    format_errors = defaultdict(int)
    for ex in data:
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

            if any(
                k not in ("role", "content", "name", "function_call") for k in message
            ):
                format_errors["message_unrecognized_key"] += 1

            if message.get("role", None) not in (
                "system",
                "user",
                "assistant",
                "function",
            ):
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


def count_tokens_and_more_informations(data):
    print("\n" + orange("Statistics:"))
    # Warnings and tokens counts
    n_missing_system = 0
    n_missing_user = 0
    n_messages = []
    convo_lens_array = []
    assistant_message_lens = []

    for ex in data:
        messages = ex["messages"]
        if not any(message["role"] == "system" for message in messages):
            n_missing_system += 1
        if not any(message["role"] == "user" for message in messages):
            n_missing_user += 1
        n_messages.append(len(messages))
        convo_lens_array.append(num_tokens_from_messages(messages))
        assistant_message_lens.append(num_assistant_tokens_from_messages(messages))

    print("Num examples missing system message:", n_missing_system)
    print("Num examples missing user message:", n_missing_user)
    print_distribution(n_messages, "num_messages_per_example")
    print_distribution(convo_lens_array, "num_total_tokens_per_example")
    print_distribution(assistant_message_lens, "num_assistant_tokens_per_example")
    n_too_long = sum(l > tokens_limit for l in convo_lens_array)
    print(
        f"\n{n_too_long} examples may be over the {tokens_limit} token limit, they will be truncated during fine-tuning"
    )
    return convo_lens_array


def cost_estimate(data, convo_lens_array):
    target_epochs = 3
    min_target_examples = 100
    max_target_examples = 25000
    min_default_epochs = 1
    max_default_epochs = 25
    n_epochs = target_epochs
    n_train_examples = len(data)
    if n_train_examples * target_epochs < min_target_examples:
        n_epochs = min(max_default_epochs, min_target_examples // n_train_examples)
    elif n_train_examples * target_epochs > max_target_examples:
        n_epochs = max(min_default_epochs, max_target_examples // n_train_examples)
    n_billing_tokens_in_data = sum(
        min(tokens_limit, length) for length in convo_lens_array
    )
    print(
        f"Dataset has ~{n_billing_tokens_in_data} tokens that will be charged for during training"
    )
    print(f"By default, you'll train for {n_epochs} epochs on this data")
    print(
        f"By default, you'll be charged for ~{n_epochs * n_billing_tokens_in_data} tokens"
    )
    dollar_value = 0.000008 * n_epochs * n_billing_tokens_in_data
    print("\n" + orange("Cost estimate: ") + str(dollar_value) + " U$")


if __name__ == "__main__":
    dataset = data_loading("data/data_training.jsonl")
    initial_statistics(dataset)
    search_erors(dataset)
    convo_lens = count_tokens_and_more_informations(dataset)
    cost_estimate(dataset, convo_lens)
