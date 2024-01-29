from openai import OpenAI
import json

key = json.load(open('cfg.json'))['key']
org = json.load(open('cfg.json'))['org']

#Iniciando uma chamada com a API da OpenAI
client = OpenAI(api_key=key, organization = org)
model = client.fine_tuning.jobs.list()

# List up to 10 events from a fine-tuning job
print("\033[94m" + "Modelos criados:" + "\033[0m\n\n")
model = client.fine_tuning.jobs.list()
for i in model:
    last_model = i
    fine_tuned_model=last_model.fine_tuned_model
    print(fine_tuned_model)