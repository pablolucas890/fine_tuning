import sys
import json
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

if __name__ == "__main__":

    with open("data/plan_actions.txt", encoding="utf-8") as f:
        plan_actions = f.read()
    with open("data/plan_obj_ddl_inv.txt", encoding="utf-8") as f:
        plan_obj_ddl_inv = f.read()
    with open("cfg.json", encoding="utf-8") as f:
        tokens_limit = json.load(f)["tokens_limit"]

    system, user_1, _ = get_system_user_from_objectives(plan_actions, "")
    _, user_2, _ = get_system_user_from_objectives(plan_obj_ddl_inv, "")

    messages_1 = []
    messages_1.append({"role": "system", "content": system})
    messages_1.append({"role": "user", "content": user_1})

    messages_2 = []
    messages_2.append({"role": "system", "content": system})
    messages_2.append({"role": "user", "content": user_2})

    tokens_1 = num_tokens_from_messages(messages_1)
    tokens_2 = num_tokens_from_messages(messages_2)

    print(f"Number of tokens in plan_actions: {orange(str(tokens_1))}")
    print(f"Number of tokens in plan_obj_ddl_inv: {orange(str(tokens_2))}")

    if tokens_1 > tokens_limit:
        print(
            f"\n{purple('Warning')}: the plan_actions has {purple(str(tokens_1))} tokens, which is over the"
            + f" {purple(str(tokens_limit))} token limit"
        )
    if tokens_2 > tokens_limit:
        print(
            f"\n{purple('Warning')}: the plan_obj_ddl_inv has {purple(str(tokens_2))} tokens, which is "
            + f" over the {orange(str(tokens_limit))} token limit"
        )
