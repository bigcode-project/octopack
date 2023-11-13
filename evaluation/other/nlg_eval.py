import json
import nlgeval
from tqdm import tqdm
from nlgeval import NLGEval

def get_ref(file_path):
    ref = []
    with open(file_path) as f:
        for line in f:
            ref.append(json.loads(line)['docstring'])
    return ref

def get_hyp(file_path):
    with open(file_path) as f:
        hyp = json.load(f)
    return hyp


n = NLGEval(no_skipthoughts=True, no_glove=True, metrics_to_omit=['SPICE', 'CIDEr', 'ROUGE_L'])

for lang in ['cpp', 'java', 'go', 'js', 'python', 'rust']:
    metrics_dicts = []
    print(f'Language: {lang}')
    ref = get_ref(f'data/{lang}/data/humanevalpack.jsonl')
    hyp = get_hyp(f'octocoder/humanevalexplain/generations_humanevalexplaindescribe{lang}_starcoderguanacocommits.json')
    for i in tqdm(range(len(hyp))):
        metrics_dicts.append({})
        for j in range(len(hyp[i])):
            metrics_dict = n.compute_individual_metrics(ref[i], hyp[i][j])
            for k in metrics_dict:
                metrics_dicts[i][k] = max(metrics_dicts[i].get(k, 0), metrics_dict[k])
    with open(f'octocoder/humanevalexplain/metrics_humanevalexplaindescribe{lang}_starcoderguanacocommits.json', 'w') as f:
        json.dump(metrics_dicts, f, indent=4)