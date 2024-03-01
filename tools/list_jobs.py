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

    client = OpenAI(api_key=key, organization=org)
    model = client.fine_tuning.jobs.list()

    print(purple("Modelos criados: ") + "\n\n")
    model = client.fine_tuning.jobs.list()
    for i in model:
        last_model = i
        fine_tuned_model = last_model.fine_tuned_model
        print(fine_tuned_model)
