#!/bin/bash
#SBATCH --job-name=eval
#SBATCH --ntasks=1                   # number of MP tasks
#SBATCH --nodes=1
#SBATCH --cpus-per-task=10           # number of cores per tasks
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --time=20:00:00             # maximum execution time (HH:MM:SS)
#SBATCH --output=%x-%j.out          # output file name
#SBATCH --account=ajs@a100
#SBATCH --constraint=a100
#SBATCH --gres=gpu:1                # number of gpus

source $ajs_ALL_CCFRWORK/start-tr13f-6B3-ml-t0
conda activate bigcode

cd /gpfswork/rech/ajs/commun/code/bigcode/bigcode-evaluation-harness

accelerate launch --config_file config_1a100_fp16.yaml main.py \
--model codegen-16B-multi \
--tasks humaneval-x-bugs-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method prompt \
--save_generations_path generations_humanevalxbugspy_codegen16b_temp02.json \
--metric_output_path evaluation_humanevalxbugspy_codegen16b_temp02.json \
--max_length_generation 2048 \
--precision fp16

accelerate launch --config_file config_1a100_fp16.yaml main.py \
--model codegen-16B-multi \
--tasks humaneval-x-bugs-js \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method prompt \
--save_generations_path generations_humanevalxbugsjs_codegen16b_temp02.json \
--metric_output_path evaluation_humanevalxbugsjs_codegen16b_temp02.json \
--generation_only \
--max_length_generation 2048 \
--precision fp16

accelerate launch --config_file config_1a100_fp16.yaml main.py \
--model codegen-16B-multi \
--tasks humaneval-x-bugs-java \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method prompt \
--save_generations_path generations_humanevalxbugsjava_codegen16b_temp02.json \
--metric_output_path evaluation_humanevalxbugsjava_codegen16b_temp02.json \
--generation_only \
--max_length_generation 2048 \
--precision fp16

accelerate launch --config_file config_1a100_fp16.yaml main.py \
--model codegen-16B-multi \
--tasks humaneval-x-bugs-go \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method prompt \
--save_generations_path generations_humanevalxbugsgo_codegen16b_temp02.json \
--metric_output_path evaluation_humanevalxbugsgo_codegen16b_temp02.json \
--generation_only \
--max_length_generation 2048 \
--precision fp16

accelerate launch --config_file config_1a100_fp16.yaml main.py \
--model codegen-16B-multi \
--tasks humaneval-x-bugs-cpp \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method prompt \
--save_generations_path generations_humanevalxbugscpp_codegen16b_temp02.json \
--metric_output_path evaluation_humanevalxbugscpp_codegen16b_temp02.json \
--generation_only \
--max_length_generation 2048 \
--precision fp16

accelerate launch --config_file config_1a100_fp16.yaml main.py \
--model codegen-16B-multi \
--tasks humaneval-x-bugs-rust \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method prompt \
--save_generations_path generations_humanevalxbugsrust_codegen16b_temp02.json \
--metric_output_path evaluation_humanevalxbugsrust_codegen16b_temp02.json \
--generation_only \
--max_length_generation 2048 \
--precision fp16