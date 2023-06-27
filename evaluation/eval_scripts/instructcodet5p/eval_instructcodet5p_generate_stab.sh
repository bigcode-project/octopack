#!/bin/bash
#SBATCH -p g40x
#SBATCH -t 24:00:00
#SBATCH --gpus=1
#SBATCH --exclusive=user
#SBATCH --hint=nomultithread
#SBATCH --account=laion
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err

source /fsx/muennighoff/env/bin/activate
cd /fsx/muennighoff/bigcode-evaluation-harness

accelerate launch --config_file config_1gpus_fp16.yaml main.py \
--model instructcodet5p-16b \
--tasks humaneval-x-generate-python \
--do_sample True \
--temperature 0.2 \
--n_samples 1 \
--batch_size 1 \
--limit 1 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method instructcodet5p \
--save_generations_path generations_humanevalxgeneratepy_instructcodet5p_temp02.json \
--metric_output_path evaluation_humanevalxgeneratepy_instructcodet5p_temp02.json \
--modeltype seq2seq \
--max_length_generation 2048 \
--precision fp16
