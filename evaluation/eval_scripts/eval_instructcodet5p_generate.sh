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

accelerate launch --config_file config_8gpus_fp16.yaml main.py \
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
--mutate_method prompt \
--save_generations_path generations_humanevalxgeneratepy_instructcodet5p_temp02.json \
--metric_output_path evaluation_humanevalxgeneratepy_instructcodet5p_temp02.json \
--modeltype seq2seq \
--max_length_generation 2048 \
--precision fp16
