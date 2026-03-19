import json

from llm import LiteLLMBackend


# from reactxen.utils.model_inference import (
#     count_tokens,
#     get_context_length,
#     watsonx_llm,
# )

from evalagent import EvaluationAgent
from functools import partial
# from reactxen.utils.model_inference import watsonx_llm
from dotenv import load_dotenv
from huggingface_hub import login
from datasets import load_dataset
import os

TEMP = 0.3
print(f'temperature = {TEMP}')

NUM_ITER = 5
print(f'NUM_ITER = {NUM_ITER}')

# fp = open('src/metaagent/demo/end2end_utterance.json', 'r')
# utterances = json.load(fp)

# fp = open('log250322_granite_res.txt', 'r')
# fp = open('logmistral.txt', 'r')
# fp = open('log250323_granite.txt', 'r')
# fp = open('granite_noreflect.txt', 'r')
# infile = 'log250324_mistral-norefl.txt'
# infile = 'log250324_fmsr-mistral-granite-norefl.txt'
# infile = 'log250325_fmsr-mistral.txt'
# infile = 'log250325_dhaval'
# infile = 'log250324_fmsr.txt'
# infile = 'log250325_gran32_llama8.txt'
# infile = 'log250326granite-tsfm.txt'
# infile = 'log250326llama8.txt'
# infile = 'log250326granite-mistral.txt'
# infile = 'logmistral.txt'
# infile = 'log250325_fmsr-mistral.txt'
# infile = 'log250323_granite.txt'
# infile = 'log250325_gran32_llama8.txt'
# infile = 'log250326llama8.txt'
# infile = 'log250325_gran32_llama8.txt'

# infile = 'log250501-iot3.txt'
# infile = 'log250501-wo3.txt'
# infile = 'log250506_iot.txt'
# infile = 'log250508_48.txt'
infile = 'log250512_big11.txt'
# infile = 'log250506_fmsr.txt'
infile = 'log251120-1.txt'
infile = 'log251120-mav.txt'
infile = 'log251121-gpt.txt'
infile = 'log260110-20.txt'
infile = 'log260108-29.txt'
infile = 'log260113-36.txt'

MIN_UTTERANCE = 1
MAX_UTTERANCE = 622

# print(f'****** input log file: {infile}')
# fp = open(infile, 'r')

# MODEL_NAME = 'mistralai/mistral-large' # 6
# MODEL_NAME = 'meta-llama/llama-3-405b-instruct' # 7
# MODEL_NAME = 'meta-llama/llama-3-3-70b-instruct' # 12
# MODEL_NAME = 'meta-llama/llama-4-maverick-17b-128e-instruct-fp8' # 16
# MODEL_NAME = 'meta-llama/llama-4-scout-17b-16e-instruct' # 17
# MODEL_NAME = 'openai-azure/gpt-4.1-2025-04-14' # 18
# MODEL_NAME = 'ibm/granite-3-3-8b-instruct' # 19

MODEL_NAME = 'ibm/granite-3-2-8b-instruct'
# MODEL_NAME = 'llama-3-1-8b-instruct'
# MODEL_NAME = 'mistral-large'
MODEL_NAME = 'granite-3-2-8b-instruct'
MODEL_NAME = 'llama-4-maverick-17b-128e-instruct-fp8'
MODEL_NAME = 'openai/gpt-oss-120b'
MODEL_NAME = 'litellm/Azure/gpt-5-2025-08-07'
MODEL_NAME = 'litellm/GCP/claude-4-sonnet'

print(f'model = {MODEL_NAME}')

utterfileIoT = 'src/meta_agent/scenarios/single_agent/iot_utterance_meta.json'
utterfileFMSR = 'src/meta_agent/scenarios/single_agent/fmsr_utterance.jsonold'
utterfileTSFM = 'src/meta_agent/scenarios/single_agent/tsfm_utterance.json'
utterfileWO = 'src/meta_agent/scenarios/single_agent/wo_utterance.json'
utterfileE2E = 'src/meta_agent/scenarios/multi_agent/end2end_utterance.json'

def load_scenarios(utterance_ids):
    ds = load_dataset("ibm-research/AssetOpsBench", "scenarios")
    train_ds = ds["train"]
    df = train_ds.to_pandas()
    filtered_df = df[df["id"].isin(utterance_ids)]
    return filtered_df.to_dict(orient="records")

savedUtter = {}
# for utterfile in [ utterfileIoT, utterfileFMSR, utterfileTSFM, utterfileWO, utterfileE2E ]:
#     print(f'utterfile = {utterfile}')

#     fp3 = open(utterfile, 'r')
#     char1 = json.load(fp3)
#     fp3.close()

load_dotenv()
login(os.getenv("HF_APIKEY", None))

utterances = load_scenarios([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 41, 42, 43, 44, 45, 46, 47, 48, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622])


for ut in utterances:
    assert ut['id'] not in savedUtter

    savedUtter[ut['id']] = ut


savedTS = None
# successfulCompletions = 0
#     "task_completion": true/false,
#     "data_retrieval_accuracy": true/false,
#     "generalized_result_verification": true/false,
#     "agent_sequence_correct": true/false,
#     "clarity_and_justification": true/false,
#     "hallucinations": true/false,
#     "suggestions": "Optional. Actions or improvements for rectifying the response if applicable."

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

prefix = 'src/evaluation/'
suffix = '.json' 

for fn in ['src/evaluation/0001.json']:
    print(f'{fn}')

    fp = open(fn, 'r')
    traj = json.load(fp)
    if not 'trajectory' in traj:
        print(f'********* {fn}: no trajectory saved, skipping....')
        continue

    fnlast = fn[(len(prefix)):]
    fnid = fnlast[:4]

    print(f'{fnid}')
    utteranceID = int(fnid)

    characteristic = savedUtter[utteranceID]

    print(json.dumps(characteristic, indent=2))

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
        evalAgent = EvaluationAgent(llm) 

        print(f"text = {characteristic['text']}")
        print(f"answer = {traj['final_answer']}")
        print(f"characteristic_answer= {characteristic['characteristic_form']}")
        print(f"think = {json.dumps(traj['trajectory'], indent=2)}")

        try:
            review_resultFull = evalAgent.evaluate_response(
                question=characteristic['text'], agent_think=json.dumps(traj['trajectory']),
                agent_response=traj['final_answer'], characteristic_answer=characteristic['characteristic_form'])
        except BaseException as e:
            print(f'EXCEPTION: {e}')
            raise e
            continue
        # evaluate_response(self, question, agent_think, agent_response, characteristic_answer):
    
        print('')
        print(review_resultFull)

        for key in stats:
            if key not in review_resultFull:
                print(f'cannnot find {key} in {review_resultFull}')
                continue

            if review_resultFull[key]:
                itemStats[key] += 1

    for key in stats:
        if itemStats[key] > (NUM_ITER / 2.0):
            stats[key] += 1
    print(itemStats)

    print('************************')


exit(1)


for line in fp:
    ismodel = line.find(MODEL_NAME)
    if ismodel == -1:
        continue

    startmeta = 'START-META: ISO '
    hasStart = line.find(startmeta)
    # print('***********', hasStart)
    isotyp = '2025-05-06T17:22:29' # just typical format

    if hasStart != -1:
        savedTS = line[hasStart+len(startmeta):hasStart+len(startmeta) + len(isotyp)]
        # print('saved ', savedTS)
        continue
        
    finish = 'FINISH-META: '
    hasfinal = line.find(finish)
    if hasfinal == -1:
        continue

    isostr = 'ISO '
    isoloc = line.find(isostr)
    if isoloc != -1:
        timestamp = line[isoloc+len(isostr):isoloc+len(isostr) + len(isotyp)]
    else:
        timestamp = savedTS

    # print (timestamp)

    # locmerge = line.index('METRIC')
    # jsonpart = line[locmerge + 6:]
    # # print(jsonpart)
    # baseinfo = json.loads(jsonpart)

    # print(json.dumps(baseinfo,indent=2))

    utterid = 'utteranceID:'
    utterloc = line.index(utterid)
    utterendloc = line.index(',', utterloc+len(utterid))
    utteranceID = int(line[utterloc+len(utterid):utterendloc])

    print(f'********* utteranceid = {utteranceID}')

    # if utteranceID < MIN_UTTERANCE or utteranceID > MAX_UTTERANCE:
    #     continue

    print(line)
    completions += 1

    # print(utteranceID)

    # file2 = 'trajs/' + timestamp + '/granite-3-8b-instruct/' + str(utteranceID).zfill(4)
    file2 = 'trajs/' + timestamp + '/' + MODEL_NAME + '/' + str(utteranceID).zfill(4)

    fp2 = open(file2, 'r')
    traj = json.load(fp2)
    if not 'trajectory' in traj:
        print(f'********* {file2}: no trajectory saved, skipping....')
        continue

    # print(json.dumps(traj['trajectory'], indent=2))

    if utteranceID not in savedUtter:
        print(f'cant find saved utterance {utteranceID}')
        continue

    characteristic = savedUtter[utteranceID]
    # for chr in chara:
    #     if chr['id'] == utteranceID:
    #         characteristic = chr
    #         break
    # assert characteristic is not None

    itemStats = {}
    for key in stats:
        itemStats[key] = 0

    for v in range(NUM_ITER):
        selected_llm_family = partial(
            watsonx_llm, max_tokens=8192, temperature=TEMP
        )
        evalAgent = EvaluationAgent(model_id=16, llm=selected_llm_family) # "openai-azure/gpt-4.1-2025-04-14", #18
        # "meta-llama/llama-4-maverick-17b-128e-instruct-fp8", #16

        print(f"text = {characteristic['text']}")
        print(f"answer = {traj['final_answer']}")
        print(f"characteristic_answer= {characteristic['characteristic_form']}")
        print(f"think = {json.dumps(traj['trajectory'], indent=2)}")

        try:
            review_resultFull = evalAgent.evaluate_response(
                question=characteristic['text'], agent_think=json.dumps(traj['trajectory']),
                agent_response=traj['final_answer'], characteristic_answer=characteristic['characteristic_form'])
        except BaseException as e:
            print(f'EXCEPTION: {e}')
            continue
        # evaluate_response(self, question, agent_think, agent_response, characteristic_answer):
    
        print('')
        print(review_resultFull)

        for key in stats:
            if key not in review_resultFull:
                print(f'cannnot find {key} in {review_resultFull}')
                continue

            if review_resultFull[key]:
                itemStats[key] += 1

    for key in stats:
        if itemStats[key] > (NUM_ITER / 2.0):
            stats[key] += 1
    print(itemStats)

    print('************************')

print(f'input file {infile}, {completions} total')
print(f'utterance range {MIN_UTTERANCE} - {MAX_UTTERANCE}')
print(f'model = {MODEL_NAME}')
print(stats)
