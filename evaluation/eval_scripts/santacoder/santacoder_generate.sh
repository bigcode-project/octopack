#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -p small-g
#SBATCH -t 24:00:00
#SBATCH --gpus-per-node=mi250:1
#SBATCH --exclusive=user
#SBATCH --hint=nomultithread
#SBATCH --account=project_462000241
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err

source /pfs/lustrep2/scratch/project_462000241/muennighoff/venv/bin/activate
cd /pfs/lustrep2/scratch/project_462000185/muennighoff/bigcode-evaluation-harness

accelerate launch --config_file config_1gpus_fp16.yaml main.py \
--model santacoder \
--tasks humaneval-x-generate-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 20 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method continue \
--save_generations_path generations_humanevalxgeneratepy_santacoder_temp02.json \
--metric_output_path evaluation_humanevalxgeneratepy_santacoder_temp02.json \
--max_length_generation 2048 \
--precision fp16
