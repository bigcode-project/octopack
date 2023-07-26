#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -p small-g
#SBATCH -t 48:00:00
#SBATCH --gpus-per-node=mi250:8
#SBATCH --exclusive=user
#SBATCH --hint=nomultithread
#SBATCH --account=project_462000241
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.er

source $ajs_ALL_CCFRWORK/start-tr13f-6B3-ml-t0
conda activate bigcode

cd /gpfswork/rech/ajs/commun/code/bigcode/bigcode-evaluation-harness

accelerate launch --config_file config_8gpus_bf16.yaml main.py \
--model bloomz \
--tasks humanevalfixtests-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 2 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--prompt instruct \
--save_generations_path generations_humanevalfixpython_bloomz.json \
--metric_output_path evaluation_humanevalfixpython_bloomz.json \
--max_length_generation 2048 \
--precision bf16 \
--max_memory_per_gpu 50GB
