import json
import sys
from openai import OpenAI

sys.path.append("/".join(__file__.split("/")[0:-2]))
# pylint: disable-next=wrong-import-position
from lib.aux import purple


if __name__ == "__main__":

    with open("cfg.json", encoding="utf-8") as f:
        key = json.load(f)["key"]
    with open("cfg.json", encoding="utf-8") as f:
        org = json.load(f)["org"]
    with open("cfg.json", encoding="utf-8") as f:
        suffix = json.load(f)["suffix"]
    with open("cfg.json", encoding="utf-8") as f:
        base_model_to_fine_tune = json.load(f)["base_model_to_fine_tune"]
    with open("data/data_training.jsonl", "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]

    client = OpenAI(api_key=key, organization=org)

    response_training = client.files.create(file=data, purpose="fine-tune")
    id_training = response_training.id
    fine_tuning = client.fine_tuning.jobs.create(
        training_file=id_training, model=base_model_to_fine_tune, suffix=suffix
    )
    print(purple("Modelo criado: ") + "\n")
    print(fine_tuning)
