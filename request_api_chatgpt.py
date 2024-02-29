from openai import OpenAI
import json
import time
import os
import tiktoken

key = json.load(open('cfg.json'))['key']
org = json.load(open('cfg.json'))['org']
fine_tuned_model='ft:gpt-3.5-turbo-0613:personal:teste-pablo:8xFa0aLd'
client = OpenAI(api_key=key, organization = org)
components = ['abastecimento de água', 'esgotamento sanitário', 'manejo das águas pluviais', 'manejo de resíduos sólidos']
objectives = {'abastecimento-de-agua': [],  'esgotamento-sanitario': [],  'manejo-das-aguas-pluviais': [],  'manejo-de-residuos-solidos': [] }
messages = []
encoding = tiktoken.get_encoding("cl100k_base")
MAX_TOKENS_PER_EXAMPLE = 4096

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
    f"Você é um engenheiro ambiental e precisa identificar os objetivos do componente '{component}' de um plano municipal de saneamento básico. "
    "Se a informação não estiver clara no trecho fornecido, indique que não é possível determinar os objetivos. "
    "Considere que o trecho pode vir de um PDF com tabelas, o que pode afetar a formatação. "
    "Os objetivos devem ser apresentados de forma clara e concisa, sem introduções, títulos, descrições, explicações ou comentários adicionais, isto é, apenas liste os objetivos separados por uma quebra de linha"
  )

  user = (
    f"Identifique e liste apenas os objetivos relacionados ao componente '{component}' encontrados no trecho do plano municipal de saneamento básico fornecido. "
    f"Trecho do plano: '{plan}'. Evite adicionar comentários ou explicações extras."
  )

  user_without_plan = (
    f"Identifique e liste apenas os objetivos relacionados ao componente '{component}' encontrados no trecho do plano municipal de saneamento básico fornecido. "
  )

  return system, user, user_without_plan

def get_system_user_from_deadline(plan, objective, component):
  system = (
    "Você é um engenheiro ambiental com a tarefa de analisar um plano municipal de saneamento básico. "
    "Sua missão é identificar o prazo previsto para a realização de um objetivo específico. "
    "Considere que o trecho fornecido pode conter informações em formatos variados, incluindo tabelas, devido à origem em um PDF. "
    "Se o prazo não estiver claro ou não for mencionado, indique isso na sua resposta."
    "Os prazos devem ser apresentados de forma clara e concisa, sem introduções, títulos, descrições, explicações ou comentários adicionais, isto é, apenas informe o prazo em anos ou em (médio prazo, longo prazo, etc)"
  )

  user = (
    f"Encontre o prazo para o objetivo específico '{objective}' do componente de '{component}' no seguinte trecho do plano municipal de saneamento básico: '{plan}'. "
    "Liste apenas o prazo relacionado a esse objetivo específico, sem incluir informações adicionais."
  )
  
  user_without_plan = (
    f"Encontre o prazo para o objetivo específico '{objective}' do componente de '{component}' no seguinte trecho do plano municipal de saneamento básico. "
    "Liste apenas o prazo relacionado a esse objetivo específico, sem incluir informações adicionais."
  )
  
  return system, user, user_without_plan

def get_system_user_from_actions(plan, objective, component):
  system = (
    "Você é um engenheiro ambiental com a tarefa de analisar um plano municipal de saneamento básico. "
    "Sua missão é identificar as ações previstas para alcançar um objetivo específico. "
    "Considere que o trecho fornecido pode conter informações em formatos variados, incluindo tabelas, devido à origem em um PDF. "
    "Se as ações não estiverem claras ou não forem mencionadas, indique isso na sua resposta."
    "As ações devem ser apresentados de forma clara e concisa, sem introduções, títulos, descrições, explicações ou comentários adicionais, isto é, apenas liste-as separados por uma quebra de linha"
  )

  user = (
    f"Encontre as ações previstas para alcançar o objetivo específico '{objective}' do componente de '{component}' no seguinte trecho do plano municipal de saneamento básico: '{plan}'. "
    "Liste apenas as ações relacionadas a esse objetivo específico, sem incluir informações adicionais."
  )
  
  user_without_plan = (
    f"Encontre as ações previstas para alcançar o objetivo específico '{objective}' do componente de '{component}' no seguinte trecho do plano municipal de saneamento básico. "
    "Liste apenas as ações relacionadas a esse objetivo específico, sem incluir informações adicionais."
  )

  return system, user, user_without_plan

def get_completion_not_stream(client, messages):
  old_tokens = num_tokens_from_messages(messages)
  if(old_tokens > MAX_TOKENS_PER_EXAMPLE):
    for message in enumerate(messages):
      _tokens = num_tokens_from_messages(messages)
      if(_tokens > MAX_TOKENS_PER_EXAMPLE):
        messages.pop(2)
        messages.pop(2)
  new_tokens = num_tokens_from_messages(messages)
  response = client.chat.completions.create(
    model=fine_tuned_model,
    messages=messages
  )

  for chunk in response:
    if(chunk[0] == 'choices'):
      return chunk[1][0].message.content

def get_assistant_message(system, user, user_without_plan):
  len_messages = len(messages)
  if(len_messages == 0):
    messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
  else:
    messages.append({"role": "user", "content": user_without_plan})
  response = get_completion_not_stream(client, messages)
  messages.append({"role": "assistant", "content": response})
  return response

def write_objectives(objectives):
  with open('data/funasa.json', 'w') as file:
    objectives = json.dumps(objectives, ensure_ascii=False, indent=2).encode('utf8')
    file.write(objectives.decode())  

def get_option():
  os.system('clear')
  print("Digite a opção desejada: \n")
  print(orange("1") + " - Identificar os objetivos do componente")
  print(orange("2") + " - Identificar o prazo para a realização de um objetivo específico")
  print(orange("3") + " - Identificar as ações previstas para alcançar um objetivo específico")
  option = input()
  os.system('clear')
  return option

def get_plan():
  with open('data/plan.txt', 'r') as file:
    return file.read()

def get_key(string):
  return string.replace(' ', '-').replace('á', 'a').replace('í', 'i').replace('ó', 'o')

def orange(string):
  return "\033[38;5;208m" + string + "\033[0m"

if __name__ == '__main__':
  
  option = get_option()
  plan = get_plan()
  
  if option == '1':
    print("\nOpção " + orange("1") + " selecionada, indentificando os " + orange("objetivos")
          + " do plano localizado em " + orange("data/plan.txt") + "\n")
    time.sleep(2)
    for i, component in enumerate(components):
      print("Gerando objetivos do componente de " + orange(component) + " ...")
      time.sleep(1)
      system, user, user_without_plan = get_system_user_from_objectives(plan, component)
      response = get_assistant_message(system, user, user_without_plan)
      response_array = response.split('\n')
      for res in response_array:
        if(res != ''):
          objectives[get_key(component)].append({ "objective": res })
    write_objectives(objectives)
    print("\nObjetivos salvos em " + orange("data/funasa.json"))
  
  elif option == '2':
    print("Opção " + orange("2") + " selecionada, indentificando os " + orange("prazos") + " para a realização dos "
          + orange("objetivos") + " localizados em " + orange("data/funasa.json") + " do plano localizado em "
          + orange("data/plan.txt") + "\n")
    time.sleep(2)
    with open('data/funasa.json', 'r') as file:
      objectives = json.load(file)
      for i, component in enumerate(components):
        print("Gerando prazos para os objetivos do componente de " + orange(component) + " ...")
        time.sleep(1)
        for objective in objectives[get_key(component)]:
          system, user, user_without_plan = get_system_user_from_deadline(plan, objective['objective'], component)
          response = get_assistant_message(system, user, user_without_plan)
          objective['deadline'] = response
    write_objectives(objectives)
    print("\nPrazos salvos em " + orange("data/funasa.json"))

  elif option == '3':
    print("Opção " + orange("3") + " selecionada, indentificando as " + orange("ações") + " previstas para alcançar os "
          + orange("objetivos") + " localizados em " + orange("data/funasa.json") + " do plano localizado em " + orange("data/plan.txt") + "\n")
    time.sleep(2)
    with open('data/funasa.json', 'r') as file:
      objectives = json.load(file)
      for i, component in enumerate(components):
        print("Gerando ações para os objetivos do componente de " + orange(component) + " ...")
        time.sleep(1)
        for objective in objectives[get_key(component)]:
          system, user, user_without_plan = get_system_user_from_actions(plan, objective['objective'], component)
          response = get_assistant_message(system, user, user_without_plan)
          objective['actions'] = response.split('\n')
    write_objectives(objectives)
    print("\nAções salvas em " + orange("data/funasa.json"))
