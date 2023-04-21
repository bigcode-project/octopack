#!/bin/bash
#SBATCH --job-name=jsonl # job name
#SBATCH --ntasks=1                   # number of MP tasks
#SBATCH --nodes=1
#SBATCH --cpus-per-task=40           # number of cores per tasks
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --time=5:00:00             # maximum execution time (HH:MM:SS)
#SBATCH --output=%x-%j.out          # output file name
#SBATCH --account=cnw@cpu
#SBATCH --partition=cpu_p1

#sort -u out.jsonl | shuf > dedup.jsonl
### Santacoder
OUTPUT=/gpfswork/rech/ajs/commun/code/bigcode/finetune/train
TOKENIZER_FILE=/gpfswork/rech/ajs/commun/code/bigcode/bigcode-evaluation-harness/santacoder/tokenizer.json
### Bigcode
OUTPUT=/gpfswork/rech/ajs/commun/code/bigcode/finetune/train_bigcode
TOKENIZER_FILE=/gpfsscratch/rech/ajs/commun/large-model/tokenizer.json


cd /gpfswork/rech/ajs/commun/code/bigcode/finetune/Megatron-LM
python tools/preprocess_data.py \
    --input ../dedup.jsonl \
    --output-prefix $OUTPUT \
    --dataset-impl mmap \
    --json-key inputs \
    --tokenizer-type TokenizerFromFile \
    --tokenizer-file $TOKENIZER_FILE \
    --workers 24 \
    --chunk-size 1000
python tools/preprocess_data.py \
    --input ../dedup.jsonl \
    --output-prefix $OUTPUT \
    --dataset-impl mmap \
    --json-key targets \
    --tokenizer-type TokenizerFromFile \
    --tokenizer-file $TOKENIZER_FILE \
    --workers 24 \
    --chunk-size 1000
