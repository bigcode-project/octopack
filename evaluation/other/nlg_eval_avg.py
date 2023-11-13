import json

for lang in ['cpp', 'java', 'go', 'js', 'python', 'rust']:
    print(f'Language: {lang}')
    with open(f'evaluation/octocoder/humanevalexplain/metrics_humanevalexplaindescribe{lang}_starcoderguanacocommits.json', 'r') as f:
        data = json.load(f)

    bleu1 = [d['Bleu_1'] * 100 for d in data]
    bleu2 = [d['Bleu_2'] * 100 for d in data]
    bleu3 = [d['Bleu_3'] * 100 for d in data]
    bleu4 = [d['Bleu_4'] * 100 for d in data]
    meteor = [d['METEOR'] * 100 for d in data]

    # Average
    print(f'BLEU-1: {sum(bleu1) / len(bleu1)}')
    print(f'BLEU-2: {sum(bleu2) / len(bleu2)}')
    print(f'BLEU-3: {sum(bleu3) / len(bleu3)}')
    print(f'BLEU-4: {sum(bleu4) / len(bleu4)}')
    print(f'METEOR: {sum(meteor) / len(meteor)}')
