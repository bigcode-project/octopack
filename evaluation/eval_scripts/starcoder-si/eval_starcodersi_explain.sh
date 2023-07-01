#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -p small-g
#SBATCH -t 48:00:00
#SBATCH --gpus-per-node=mi250:1
#SBATCH --exclusive=user
#SBATCH --hint=nomultithread
#SBATCH --account=project_462000241
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err

source /pfs/lustrep2/scratch/project_462000241/muennighoff/venv/bin/activate
cd /pfs/lustrep2/scratch/project_462000185/muennighoff/bigcode-evaluation-harness

accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port 25902 main.py \
--model starcoder-si-10 \
--tasks humaneval-x-explain-generate-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method instruct-qa \
--load_data_path generations_humanevalxexplaindescpy_starcodersi_temp02.json \
--save_generations_path generations_humanevalxexplaingenpy_starcodersi_temp02.json \
--max_length_generation 2048 \
--precision bf16


accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port 25901 main.py \
--model starcoder-si-10 \
--tasks humaneval-x-explain-desc-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method instruct-qa \
--save_generations_path generations_humanevalxexplaindescpy_starcodersi_temp02.json \
--generation_only \
--max_length_generation 1500 \
--precision bf16

accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port 25902 main.py \
--model starcoder-si-10 \
--tasks humaneval-x-explain-generate-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method instruct-qa \
--load_data_path generations_humanevalxexplaindescpy_starcodersi_temp02.json \
--save_generations_path generations_humanevalxexplaingenpy_starcodersi_temp02.json \
--generation_only \
--max_length_generation 1500 \
--precision bf16
