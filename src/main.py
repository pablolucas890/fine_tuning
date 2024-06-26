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
    get_system_user_from_investment,
)

with open("cfg.json", encoding="utf-8") as f:
    key = json.load(f)["key"]
with open("cfg.json", encoding="utf-8") as f:
    org = json.load(f)["org"]
with open("cfg.json", encoding="utf-8") as f:
    tokens_limit = json.load(f)["tokens_limit"]
with open("cfg.json", encoding="utf-8") as f:
    model_to_conversation = json.load(f)["model_to_conversation"]

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

TOP_P = 0
PRESENCE_PENALTY = 0
FREQUENCY_PENALTY = 0
TEMPERATURE = 0


def get_completion_not_stream(client, messages):
    old_tokens = num_tokens_from_messages(messages)
    if old_tokens > tokens_limit:
        for _ in enumerate(messages):
            _tokens = num_tokens_from_messages(messages)
            if _tokens > tokens_limit:
                messages.pop(2)
                messages.pop(2)
    chat = client.chat.completions.create(
        model=model_to_conversation,
        messages=messages,
        stream=False,
        presence_penalty=PRESENCE_PENALTY,
        frequency_penalty=FREQUENCY_PENALTY,
        temperature=TEMPERATURE,
    )

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


def write_funasa_and_open_sheet(funasa):
    with open("data/funasa.json", encoding="utf-8", mode="w") as f:
        funasa = json.dumps(funasa, ensure_ascii=False, indent=2).encode("utf8")
        f.write(funasa.decode())
    print("\nDados salvos em " + orange("data/funasa.json"))
    print("Abrindo planilha...")
    os.system("python3 tools/generate_sheet.py")


def get_option(menu_type):
    if menu_type == "main_menu":
        os.system("clear")
        print("Digite a opção desejada: \n")
        print(f"{orange('1')} - Identificar os objetivos do componente")
        print(f"{orange('2')} - Identificar o prazo de um objetivo específico")
        print(f"{orange('3')} - Identificar o investimento de um objetivo específico")
        print(f"{orange('4')} - Identificar as ações de um objetivo específico")
        print(f"{orange('5')} - Gerar planilha com quadros da FUNASA")
        print(f"{orange('6')} - Atualizar planilha com dados editados")
        print(f"{orange('7')} - Sair")
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
        plan = f.read()
        system_token, user_token, _ = get_system_user_from_objectives(plan, "")
        messages_token = []
        messages_token.append({"role": "system", "content": system_token})
        messages_token.append({"role": "user", "content": user_token})
        plan = plan[: (tokens_limit * 3) - 500]
        return plan


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


def generate_inv_ddl_act(index, plan, key, year=None):
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
        elif key == "deadline":
            system, user, user_without_plan = get_system_user_from_deadline(
                plan, objective["objective"], components[index], year
            )
            objective[key] = get_assistant_message(system, user, user_without_plan)
        else:
            system, user, user_without_plan = get_system_user_from_investment(
                plan, objective["objective"], components[index]
            )
            objective[key] = get_assistant_message(system, user, user_without_plan)


if __name__ == "__main__":

    params = sys.argv
    OPTION1 = None
    OPTION2 = None
    YEAR = None

    if len(params) > 1:
        OPTION1 = params[1]
    if len(params) > 2:
        OPTION2 = params[2]
    if len(params) > 3:
        YEAR = params[3]
    if len(params) > 4:
        model_to_conversation = params[4]
    if len(params) > 5:
        tokens_limit = int(params[5])

    funasa = get_funasa()

    option = OPTION1 if OPTION1 else get_option("main_menu")

    while option != "7":
        if option == "1":
            plan = get_plan("obj_ddl_inv")
            option = OPTION2 if OPTION2 else get_option("components_menu")
            if option == "1":
                for index, _ in enumerate(components):
                    generate_objectives(index, plan)
            elif option != "7":
                index = int(option) - 2
                generate_objectives(index, plan)
            write_funasa_and_open_sheet(funasa)
        elif option == "2":
            plan = get_plan("obj_ddl_inv")
            option = OPTION2 if OPTION2 else get_option("components_menu")
            if YEAR:
                year = YEAR
            else:
                print("Digite o ano de publicação do plano: ")
                year = input()
            if option == "1":
                for index, _ in enumerate(components):
                    generate_inv_ddl_act(index, plan, "deadline", year)
            elif option != "7":
                index = int(option) - 2
                generate_inv_ddl_act(index, plan, "deadline", year)
            write_funasa_and_open_sheet(funasa)
        elif option == "3":
            plan = get_plan("obj_ddl_inv")
            option = OPTION2 if OPTION2 else get_option("components_menu")
            if option == "1":
                for index, _ in enumerate(components):
                    generate_inv_ddl_act(index, plan, "investment")
            elif option != "7":
                index = int(option) - 2
                generate_inv_ddl_act(index, plan, "investment")
            write_funasa_and_open_sheet(funasa)

        elif option == "4":
            plan = get_plan("actions")
            option = OPTION2 if OPTION2 else get_option("components_menu")
            if option == "1":
                for index, _ in enumerate(components):
                    generate_inv_ddl_act(index, plan, "actions")
            elif option != "7":
                index = int(option) - 2
                generate_inv_ddl_act(index, plan, "actions")
            write_funasa_and_open_sheet(funasa)
        elif option == "5":
            print("Abrindo planilha...")
            os.system("python3 tools/generate_sheet.py")
        elif option == "6":
            print("TODO: Atualizar funasa.json")
        option = "7" if OPTION1 else get_option("main_menu")
