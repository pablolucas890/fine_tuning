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
