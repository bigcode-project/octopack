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

accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port 50749 main.py \
--model starcoder-guanaco-commits-50 \
--tasks humaneval-x-generate-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method starcodercommit \
--save_generations_path generations_humanevalxgeneratepy_starcoderguanacocommits2_temp02.json \
--metric_output_path evaluation_humanevalxgeneratepy_starcoderguanacocommits2_temp02.json \
--max_length_generation 2048 \
--precision bf16


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

accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port 50749 main.py \
--model starcoder-guanaco-commits-50 \
--tasks humaneval-x-generate-cpp \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method starcodercommit \
--save_generations_path generations_humanevalxgeneratecpp_starcoderguanacocommits2_temp02.json \
--metric_output_path evaluation_humanevalxgeneratecpp_starcoderguanacocommits2_temp02.json \
--max_length_generation 2048 \
--precision bf16


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

accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port 60749 main.py \
--model starcoder-guanaco-commits-50 \
--tasks humaneval-x-bugs-python-tests \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method starcodercommit \
--save_generations_path generations_humanevalxbugspy_starcoderguanacocommits2_temp02.json \
--metric_output_path evaluation_humanevalxbugspy_starcoderguanacocommits2_temp02.json \
--max_length_generation 2048 \
--precision bf16





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

accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port 50749 main.py \
--model starcoder-guanaco-commits-50 \
--tasks humaneval-x-explain-describe-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method starcodercommit \
--save_generations_path generations_humanevalxexplaindescribepy_starcoderguanacocommits2_temp02.json \
--metric_output_path evaluation_humanevalxexplaindescribepy_starcoderguanacocommits2_temp02.json \
--max_length_generation 2048 \
--generation_only \
--precision bf16



CUDA_VISIBLE_DEVICES=3 accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port 50749 main.py \
--model gc-80-nofc \
--tasks humaneval-x-generate-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method instruct-qa \
--save_generations_path generations_humanevalxgeneratepy_starcodergc_temp02.json \
--metric_output_path evaluation_humanevalxgeneratepy_starcodergc_temp02.json \
--max_length_generation 2048 \
--precision bf16
