#!/bin/bash
#SBATCH --job-name=eval
#SBATCH --ntasks=1                   # number of MP tasks
#SBATCH --nodes=1
#SBATCH --cpus-per-task=10           # number of cores per tasks
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --time=10:00:00             # maximum execution time (HH:MM:SS)
#SBATCH --output=%x-%j.out          # output file name
#SBATCH --account=ajs@v100
#SBATCH --gres=gpu:1                # number of gpus

source $six_ALL_CCFRWORK/start-tr13f-6B3-ml-t0

cd ~/prod-worksf/code/bigcode/bigcode-evaluation-harness

accelerate launch --config_file config_1a100.yaml main.py \
--model codegen-2B-mono \
--tasks quixbugs \
--do_sample False \
--n_samples 1 \
--batch_size 1 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method prompt \
--generations_path generations_quixbugs_codegen2b_greedy.json \
--output_path evaluation_results_quixbugs_codegen2b_greedy.json \
--max_length_generation 1024


accelerate launch --config_file config_1a100.yaml main.py \
--model codegen-2B-mono \
--tasks parity \
--temperature 0.7 \
--do_sample True \
--n_samples 3200 \
--batch_size 160 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method prompt \
--generations_path generations_parity_codegen2b_prompt_temp07.json \
--output_path evaluation_results_parity_codegen2b_prompt_temp07.json

accelerate launch --config_file config_1a100.yaml main.py \
--model codegen-2B-mono \
--tasks parity \
--temperature 0.7 \
--do_sample True \
--n_samples 3200 \
--batch_size 160 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method prompt \
--generations_path generations_parity_codegen2b_prompt_temp07.json \
--output_path evaluation_results_parity_codegen2b_prompt_temp07.json

