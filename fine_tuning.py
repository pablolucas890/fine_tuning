import json
from openai import OpenAI
from aux import purple


if __name__ == "__main__":

    with open("cfg.json", encoding="utf-8") as f:
        key = json.load(f)["key"]
    with open("cfg.json", encoding="utf-8") as f:
        org = json.load(f)["org"]
    with open("cfg.json", encoding="utf-8") as f:
        suffix = json.load(f)["suffix"]
    with open("cfg.json", encoding="utf-8") as f:
        model = json.load(f)["model"]
    with open("data_training.jsonl", "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]

    client = OpenAI(api_key=key, organization=org)

    response_training = client.files.create(file=data, purpose="fine-tune")
    id_training = response_training.id
    fine_tuning = client.fine_tuning.jobs.create(
        training_file=id_training, model=model, suffix=suffix
    )
    print(purple("Modelo criado: ") + "\n")
    print(fine_tuning)
