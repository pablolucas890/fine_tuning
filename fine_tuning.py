from openai import OpenAI
import json

key = json.load(open('cfg.json'))['key']
org = json.load(open('cfg.json'))['org']
suffix = json.load(open('cfg.json'))['suffix']
model=json.load(open('cfg.json'))['model']
client = OpenAI(api_key=key, organization = org)

#Passando o arquivo .jsonl criado para treinamento para a openAI processar e recebendo sua resposta
response_training = client.files.create(file=open("data_training.jsonl", "rb"), purpose="fine-tune")
#Salvando o id do arquivo de treinamento que foi carregado na openAI
id_training = response_training.id
#Criando o modelo: aqui,deve-se passar o id do objeto retornado ao passar o .jsonl de treinamento para a OpenAI
fine_tuning = client.fine_tuning.jobs.create(training_file=id_training, model=model, suffix=suffix)
print("\033[94m" + "Modelo criado:" + "\033[0m\n\n")
print(fine_tuning)