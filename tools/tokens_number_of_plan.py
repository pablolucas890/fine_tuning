import sys
import tiktoken

sys.path.append("/".join(__file__.split("/")[0:-2]))
# pylint: disable-next=wrong-import-position
from lib.aux import (
    orange,
    purple,
    get_system_user_from_objectives,
    num_tokens_from_messages,
)

encoding = tiktoken.get_encoding("cl100k_base")
MAX_TOKENS_PER_EXAMPLE = 4096

if __name__ == "__main__":

    with open("data/plan_actions.txt", encoding="utf-8") as f:
        plan_actions = f.read()
    with open("data/plan_objectives_and_deadlines.txt", encoding="utf-8") as f:
        plan_objectives_and_deadlines = f.read()

    system, user_1, _ = get_system_user_from_objectives(plan_actions, "")
    _, user_2, _ = get_system_user_from_objectives(plan_objectives_and_deadlines, "")

    messages_1 = []
    messages_1.append({"role": "system", "content": system})
    messages_1.append({"role": "user", "content": user_1})

    messages_2 = []
    messages_2.append({"role": "system", "content": system})
    messages_2.append({"role": "user", "content": user_2})

    tokens_1 = num_tokens_from_messages(messages_1)
    tokens_2 = num_tokens_from_messages(messages_2)

    print(f"Number of tokens in plan_actions: {orange(str(tokens_1))}")
    print(f"Number of tokens in plan_objectives_and_deadlines: {orange(str(tokens_2))}")

    if tokens_1 > MAX_TOKENS_PER_EXAMPLE:
        print(
            f"\n{purple('Warning')}: the plan_actions has {purple(str(tokens_1))} tokens, which is over the"
            + f" {purple(str(MAX_TOKENS_PER_EXAMPLE))} token limit"
        )
    if tokens_2 > MAX_TOKENS_PER_EXAMPLE:
        print(
            f"\n{purple('Warning')}: the plan_objectives_and_deadlines has {purple(str(tokens_2))} tokens, which is "
            + f" over the {orange(str(MAX_TOKENS_PER_EXAMPLE))} token limit"
        )
