#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -p small-g
#SBATCH -t 24:00:00
#SBATCH --gpus-per-node=mi250:8
#SBATCH --exclusive=user
#SBATCH --hint=nomultithread
#SBATCH --account=project_462000241
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err

source /pfs/lustrep2/scratch/project_462000241/muennighoff/venv/bin/activate
cd /pfs/lustrep2/scratch/project_462000185/muennighoff/bigcode-evaluation-harness

accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port 20699 main.py \
--model bloomz \
--tasks humaneval-x-explain-describe-python \
--do_sample True \
--temperature 0.2 \
--n_samples 1 \
--batch_size 1 \
--limit 1 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method instruct \
--save_generations_path generations_humanevalxexplaindesc_bloomz_temp02.json \
--max_length_generation 2048 \
--precision bf16 \
--generation_only \
--max_memory_per_gpu 40GB

accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port 20699 main.py \
--model bloomz \
--tasks humaneval-x-explain-generate-python \
--do_sample True \
--temperature 0.2 \
--n_samples 1 \
--batch_size 1 \
--limit 1 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method instruct \
--load_data_path generations_humanevalxexplaindesc_bloomz_temp02.json \
--save_generations_path generations_humanevalxexplaingen_bloomz_temp02.json \
--metric_output_path evaluation_humanevalxexplain_bloomz_temp02.json \
--max_length_generation 2048 \
--precision bf16 \
--max_memory_per_gpu 40GB
