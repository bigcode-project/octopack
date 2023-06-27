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

accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port 20749 main.py \
--model WizardCoder-15B-V1.0 \
--tasks humaneval-x-generate-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method instruct \
--save_generations_path generations_humanevalxgeneratepy_wizardcoder_temp02.json \
--metric_output_path evaluation_humanevalxgeneratepy_wizardcoder_temp02.json \
--max_length_generation 2048 \
--precision bf16
