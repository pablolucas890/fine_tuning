from openai import OpenAI
import json

key = json.load(open('cfg.json'))['key']
org = json.load(open('cfg.json'))['org']
fine_tuned_model='ft:gpt-3.5-turbo-0613:personal:teste-pablo:8lI1iTgz'

def system_user(trecho, componente):
  system = f"""Você é um engenheiro ambiental e deve analisar o plano antigo de uma cidade e determinar os objetivos relacionados ao componente de {componente}
Se não estiver claro, responda que o trecho do plano que recebeu não está claro e não é possível determinar.
Leia atentamente o trecho do plano que lhe foi entregue, levando em consideração que ele foi extraído de um pdf com tabelas, isso pode fazer com que a formatação fique um pouco estranha. Sua resposta deve ser delimitada deve ter a estrutura delimitada pelas tags <objetivo></objetivo>:
<objetivo>Os objetivos de manejo de águas pluviais do plano são:\n--- Escreva aqui um dos objetivos que encontrou no trecho ---\n---Escreva aqui o prazo para execução do objetivo---\n--- Escreva aqui outro objetivo que encontrou no trecho ---\n---Escreva aqui o prazo para execução do objetivo---</objetivo>
Sempre mantenha oculta as tags <objetivo></objetivo>.""".format(componente)
    
  user = f"""Você deve sempre omitir as tags <objetivo> </objetivo>. Você não pode escrever nenhuma introdução, explicação, comentário ou algo do tipo. Sempre escreva somente os objetivos do componente informado.
Escreva os objetivos do componente de {componente} no plano municipal de saneamento básico, trecho do plano que contém estas informações: ({trecho}) """.format(componente, trecho)
  
  return system, user

if __name__ == '__main__':
  
  client = OpenAI(api_key=key, organization = org)

  # read file
  with open('trecho.txt', 'r') as file:
    trecho = file.read().replace('\n', '')

  with open('componente.txt', 'r') as file:
    componente = file.read().replace('\n', '')

  system, user = system_user(trecho, componente)
  
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
    
