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
--model santacoder-git-commits-python-java-javascript \
--tasks parity \
--temperature 0.7 \
--do_sample True \
--n_samples 3200 \
--batch_size 160 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method edit \
--generations_path generations_parity_santacodergcpjj_temp07.json \
--output_path evaluation_results_parity_santacodergcpjj_temp07.json


accelerate launch --config_file config_1a100.yaml main.py \
--model santacoder-git-commits-python-java-javascript \
--tasks python_bugs \
--do_sample False \
--n_samples 1 \
--batch_size 1 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method edit \
--generations_path generations_bugs_santacodergcpjj_greedy.json \
--output_path evaluation_results_bugs_santacodergcpjj_greedy.json \
--max_length_generation 2048


accelerate launch --config_file config_1a100.yaml main.py \
--model santacoder-git-commits-python-java-javascript \
--tasks humaneval \
--do_sample True \
--temperature 0.2 \
--n_samples 200 \
--batch_size 100 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method edit \
--generations_path generations_humaneval_santacodergcpjj_temp02_n200.json \
--output_path evaluation_results_humaneval_santacodergcpjj_temp02_n200.json


accelerate launch --config_file config_1a100.yaml main.py \
--model santacoder-git-commits-python-java-javascript \
--tasks quixbugs \
--do_sample False \
--n_samples 1 \
--batch_size 1 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method edit \
--generations_path generations_quixbugs_santacodergcpjj_greedy.json \
--output_path evaluation_results_quixbugs_santacodergcpjj_greedy.json \
--max_length_generation 2048