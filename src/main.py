# pylint: disable=redefined-outer-name
import json
import time
import os
import sys
from openai import OpenAI

sys.path.append("/".join(__file__.split("/")[0:-2]))
# pylint: disable-next=wrong-import-position
from lib.aux import (
    orange,
    num_tokens_from_messages,
    get_system_user_from_objectives,
    get_system_user_from_deadline,
    get_system_user_from_actions,
)

with open("cfg.json", encoding="utf-8") as f:
    key = json.load(f)["key"]
with open("cfg.json", encoding="utf-8") as f:
    org = json.load(f)["org"]

client = OpenAI(api_key=key, organization=org)

components = [
    "abastecimento de água",
    "esgotamento sanitário",
    "manejo das águas pluviais",
    "manejo de resíduos sólidos",
]
funasa = {
    "abastecimento-de-agua": [],
    "esgotamento-sanitario": [],
    "manejo-das-aguas-pluviais": [],
    "manejo-de-residuos-solidos": [],
}
messages = []

FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0613:personal:teste-pablo:8xFa0aLd"
MAX_TOKENS_PER_EXAMPLE = 4096


def get_completion_not_stream(client, messages):
    old_tokens = num_tokens_from_messages(messages)
    if old_tokens > MAX_TOKENS_PER_EXAMPLE:
        for _ in enumerate(messages):
            _tokens = num_tokens_from_messages(messages)
            if _tokens > MAX_TOKENS_PER_EXAMPLE:
                messages.pop(2)
                messages.pop(2)
    chat = client.chat.completions.create(model=FINE_TUNED_MODEL, messages=messages)

    for chunk in chat:
        if chunk[0] == "choices":
            return chunk[1][0].message.content
    return ""


def get_assistant_message(system, user, user_without_plan):
    len_messages = len(messages)
    if len_messages == 0:
        messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})
    else:
        messages.append({"role": "user", "content": user_without_plan})
    assistent_response = get_completion_not_stream(client, messages)
    messages.append({"role": "assistant", "content": assistent_response})
    return assistent_response


def write_funasa(funasa):
    with open("data/funasa.json", encoding="utf-8", mode="w") as f:
        funasa = json.dumps(funasa, ensure_ascii=False, indent=2).encode("utf8")
        f.write(funasa.decode())
    print("\nDados salvos em " + orange("data/funasa.json"))


def get_option(menu_type):
    if menu_type == "main_menu":
        os.system("clear")
        print("Digite a opção desejada: \n")
        print(f"{orange('1')} - Identificar os objetivos do componente")
        print(f"{orange('2')} - Identificar o prazo de um objetivo específico")
        print(f"{orange('3')} - Identificar as ações de um objetivo específico")
        print(f"{orange('4')} - Gerar planilha com quadros da FUNASA")
        print(f"{orange('5')} - Sair")
        opt = input()
    elif menu_type == "components_menu":
        print("Digite a opção desejada: \n")
        print(f"{orange('1')} - Todos os componentes")
        print(f"{orange('2')} - Apenas o componente de abastecimento de água")
        print(f"{orange('3')} - Apenas o componente de esgotamento sanitário")
        print(f"{orange('4')} - Apenas o componente de manejo das águas pluviais")
        print(f"{orange('5')} - Apenas o componente de manejo de resíduos sólidos")
        print(f"{orange('6')} - Voltar")
        opt = input()
    os.system("clear")
    return opt


def get_plan(plan):
    with open(f"data/plan_{plan}.txt", encoding="utf-8") as f:
        return f.read()


def get_funasa():
    if not os.path.exists("data/funasa.json"):
        return funasa
    with open("data/funasa.json", encoding="utf-8") as file:
        return json.load(file)


def get_key(string):
    return (
        string.replace(" ", "-").replace("á", "a").replace("í", "i").replace("ó", "o")
    )


def generate_objectives(index, plan):
    component = components[index]
    funasa[get_key(component)] = []
    print("Gerando objetivos do componente de " + orange(component) + " ...")
    time.sleep(1)
    system, user, user_without_plan = get_system_user_from_objectives(plan, component)
    response = get_assistant_message(system, user, user_without_plan)
    response_array = response.split("\n")
    for res in response_array:
        if res != "":
            funasa[get_key(component)].append({"objective": res})


def generate_deadlines_and_actions(index, plan, key, year=None):
    print(
        f"Gerando {orange(key)} para os objetivos do componente de {orange(components[index])} ..."
    )
    time.sleep(1)
    for objective in funasa[get_key(components[index])]:
        if key == "actions":
            system, user, user_without_plan = get_system_user_from_actions(
                plan, objective["objective"], components[index]
            )
            objective[key] = get_assistant_message(
                system, user, user_without_plan
            ).split("\n")
        else:
            system, user, user_without_plan = get_system_user_from_deadline(
                plan, objective["objective"], components[index], year
            )
            objective[key] = get_assistant_message(system, user, user_without_plan)


if __name__ == "__main__":

    funasa = get_funasa()

    option = get_option("main_menu")

    while option != "5":
        if option == "1":
            plan = get_plan("objectives_and_deadlines")
            option = get_option("components_menu")
            if option == "1":
                for index, _ in enumerate(components):
                    generate_objectives(index, plan)
            elif option != "6":
                index = int(option) - 2
                generate_objectives(index, plan)
            write_funasa(funasa)
        elif option == "2":
            plan = get_plan("objectives_and_deadlines")
            option = get_option("components_menu")
            print("Digite o ano de publicação do plano: ")
            year = input()
            if option == "1":
                for index, _ in enumerate(components):
                    generate_deadlines_and_actions(index, plan, "deadline", year)
            elif option != "6":
                index = int(option) - 2
                generate_deadlines_and_actions(index, plan, "deadline", year)
            write_funasa(funasa)
        elif option == "3":
            plan = get_plan("actions")
            option = get_option("components_menu")
            if option == "1":
                for index, _ in enumerate(components):
                    generate_deadlines_and_actions(index, plan, "actions")
            elif option != "6":
                index = int(option) - 2
                generate_deadlines_and_actions(index, plan, "actions")
            write_funasa(funasa)
        elif option == "4":
            os.system("python3 tools/generate_sheet.py")
        option = get_option("main_menu")
