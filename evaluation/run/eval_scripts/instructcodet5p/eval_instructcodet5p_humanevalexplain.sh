#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -p small-g
#SBATCH -t 24:00:00
#SBATCH --cpus-per-task=31
#SBATCH --gpus-per-node=mi250:1
#SBATCH --exclusive=user
#SBATCH --hint=nomultithread
#SBATCH --account=project_462000241
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err

source /pfs/lustrep2/scratch/project_462000241/muennighoff/venv/bin/activate
cd /pfs/lustrep2/scratch/project_462000185/muennighoff/bigcode-evaluation-harness

accelerate launch --config_file config_1gpus_fp16.yaml main.py \
--model instructcodet5p-16b \
--tasks humanevalexplaindescribe-python \
--do_sample True \
--temperature 0.2 \
--n_samples 1 \
--batch_size 1 \
--limit 1 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--prompt instructcodet5p \
--save_generations_path generations_humanevalexplaindescribepython_instructcodet5p.json \
--modeltype seq2seq \
--max_length_generation 2048 \
--precision fp16 \
--generation_only

accelerate launch --config_file config_1gpus_fp16.yaml main.py \
--model instructcodet5p-16b \
--tasks humanevalexplainsynthesize-python \
--do_sample True \
--temperature 0.2 \
--n_samples 1 \
--batch_size 1 \
--limit 1 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--prompt instructcodet5p \
--load_data_path generations_humanevalexplaindescribepython_instructcodet5p.json \
--save_generations_path generations_humanevalexplainsynthesizepython_instructcodet5p.json \
--metric_output_path evaluation_humanevalexplainpython_instructcodet5p.json \
--modeltype seq2seq \
--max_length_generation 2048 \
--precision fp16
