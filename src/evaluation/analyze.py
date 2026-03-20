import json

from llm import LiteLLMBackend
from evalagent import EvaluationAgent
from functools import partial
from dotenv import load_dotenv
from huggingface_hub import login
from datasets import load_dataset
import os

TEMP = 0.3
print(f'temperature = {TEMP}')

NUM_ITER = 5
print(f'NUM_ITER = {NUM_ITER}')

def load_scenarios(utterance_ids):
    ds = load_dataset("ibm-research/AssetOpsBench", "scenarios")
    train_ds = ds["train"]
    df = train_ds.to_pandas()
    filtered_df = df[df["id"].isin(utterance_ids)]
    return filtered_df.to_dict(orient="records")

savedUtter = {}

load_dotenv()

login(os.getenv("HF_APIKEY", None))

utterances = load_scenarios([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 41, 42, 43, 44, 45, 46, 47, 48, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622])

for ut in utterances:
    assert ut['id'] not in savedUtter

    savedUtter[ut['id']] = ut

savedTS = None

completions = 0
stats = {
    "task_completion": 0,
    "data_retrieval_accuracy": 0,
    "generalized_result_verification": 0,
    "agent_sequence_correct": 0,
    "clarity_and_justification": 0,
    "hallucinations": 0,
}

llm = LiteLLMBackend('watsonx/meta-llama/llama-4-maverick-17b-128e-instruct-fp8')
evalAgent = EvaluationAgent(llm, temperature=TEMP) 

prefix = 'src/evaluation/'
suffix = '.json' 

for fn in ['src/evaluation/0001.json', 'src/evaluation/0002.json']:
    # print(f'{fn}')

    fp = open(fn, 'r')
    traj = json.load(fp)
    if not 'trajectory' in traj:
        print(f'********* {fn}: no trajectory saved, skipping....')
        continue

    fnlast = fn[(len(prefix)):]
    fnid = fnlast[:len(suffix)-1]

    utteranceID = int(fnid)

    characteristic = savedUtter[utteranceID]

    # print(json.dumps(characteristic, indent=2))

    # {
    #   "id": 1,
    #   "type": "IoT",
    #   "text": "What IoT sites are available?",
    #   "category": "Knowledge Query",
    #   "deterministic": true,
    #   "characteristic_form": "The expected response should be the return value of all sites, either as text or as a reference to a file",
    #   "group": "retrospective",
    #   "entity": "Site",
    #   "note": "Source: IoT data operations; Deterministic query with single correct answer; Category: Knowledge Query"
    # }

    assert characteristic['id'] == utteranceID

    assert characteristic['text'] == traj['task']

    itemStats = {}
    for key in stats:
        itemStats[key] = 0

    for v in range(NUM_ITER):

        # print(f"text = {characteristic['text']}")
        # print(f"answer = {traj['final_answer']}")
        # print(f"characteristic_answer= {characteristic['characteristic_form']}")
        # print(f"think = {json.dumps(traj['trajectory'], indent=2)}")

        try:
            review_resultFull = evalAgent.evaluate_response(
                question=characteristic['text'], agent_think=json.dumps(traj['trajectory']),
                agent_response=traj['final_answer'], characteristic_answer=characteristic['characteristic_form'])
        except BaseException as e:
            print(f'EXCEPTION: {e}')
            continue
    
        # print(review_resultFull)

        for key in stats:
            if key not in review_resultFull:
                print(f'cannnot find {key} in {review_resultFull}')
                continue

            if review_resultFull[key]:
                itemStats[key] += 1

    completions += 1
    
    for key in stats:
        if itemStats[key] > (NUM_ITER / 2.0):
            stats[key] += 1
    print(itemStats)

    print('************************')

print(f'{completions} total completions')
print(stats)
