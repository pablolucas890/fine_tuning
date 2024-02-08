from openai import OpenAI
import json

key = json.load(open('cfg.json'))['key']
org = json.load(open('cfg.json'))['org']
fine_tuned_model='ft:gpt-3.5-turbo-0613:personal:teste-pablo:8lI1iTgz'

def get_objectives(trecho, componente):
  system = (
      f"Você é um engenheiro ambiental e precisa identificar os objetivos do componente '{componente}' de um plano municipal de saneamento básico. "
      "Se a informação não estiver clara no trecho fornecido, indique que não é possível determinar os objetivos. "
      "Considere que o trecho pode vir de um PDF com tabelas, o que pode afetar a formatação. "
      "Os objetivos devem ser apresentados de forma clara e concisa, sem introduções ou comentários adicionais, isto é, apenas liste os objetivos separados por uma quebra de linha"
  )

  user = (
      f"Identifique e liste apenas os objetivos relacionados ao componente '{componente}' encontrados no trecho do plano municipal de saneamento básico fornecido. "
      f"Trecho do plano: '{trecho}'. Evite adicionar comentários ou explicações extras."
  )

  return system, user

def get_deadline(trecho, objetivo, componente):
  system = (
      "Você é um engenheiro ambiental com a tarefa de analisar um plano municipal de saneamento básico. "
      "Sua missão é identificar o prazo previsto para a realização de um objetivo específico. "
      "Considere que o trecho fornecido pode conter informações em formatos variados, incluindo tabelas, devido à origem em um PDF. "
      "Se o prazo não estiver claro ou não for mencionado, indique isso na sua resposta."
  )

  user = (
      f"Encontre o prazo para o objetivo específico '{objetivo}' do componente de '{componente}' no seguinte trecho do plano municipal de saneamento básico: '{trecho}'. "
      "Liste apenas o prazo relacionado a esse objetivo específico, sem incluir informações adicionais."
  )

  return system, user

def get_actions(trecho, objetivo, componente):
  system = (
      "Você é um engenheiro ambiental com a tarefa de analisar um plano municipal de saneamento básico. "
      "Sua missão é identificar as ações previstas para alcançar um objetivo específico. "
      "Considere que o trecho fornecido pode conter informações em formatos variados, incluindo tabelas, devido à origem em um PDF. "
      "Se as ações não estiverem claras ou não forem mencionadas, indique isso na sua resposta."
      "As ações devem ser apresentados de forma clara e concisa, sem introduções ou comentários adicionais, isto é, apenas liste-as separados por uma quebra de linha"
  )

  user = (
      f"Encontre as ações previstas para alcançar o objetivo específico '{objetivo}' do componente de '{componente}' no seguinte trecho do plano municipal de saneamento básico: '{trecho}'. "
      "Liste apenas as ações relacionadas a esse objetivo específico, sem incluir informações adicionais."
    )

  return system, user

if __name__ == '__main__':
  
  client = OpenAI(api_key=key, organization = org)

  with open('data/trecho.txt', 'r') as file:
    trecho = file.read().replace('\n', '')
  with open('data/componente.txt', 'r') as file:
    componente = file.read().replace('\n', '')
  with open('data/objetivo.txt', 'r') as file:
    objetivo = file.read().replace('\n', '')
    
  system, user = get_objectives(trecho, componente)
  # system, user = get_deadline(trecho, objetivo, componente)
  # system, user = get_actions(trecho, objetivo, componente)
  
  response = client.chat.completions.create(
    model=fine_tuned_model,
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": user}
    ]
  )

  for chunk in response:
    if(chunk[0] == 'choices'):
      print(chunk[1][0].message.content)
      with open('data/resultado.txt', 'w') as file:
        file.write(chunk[1][0].message.content)
