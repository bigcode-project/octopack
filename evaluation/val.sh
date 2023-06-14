#!/bin/bash
#SBATCH --job-name=ckpts
#SBATCH --ntasks=1                   # number of MP tasks
#SBATCH --nodes=1
#SBATCH --cpus-per-task=10           # number of cores per tasks
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --time=10:00:00             # maximum execution time (HH:MM:SS)
#SBATCH --output=%x-%j.out          # output file name
#SBATCH --account=cnw@cpu
#SBATCH --partition=cpu_p1

set -x -e

source $six_ALL_CCFRWORK/start-tr13f-6B3-ml-t0
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

#iter_0005000
#iter_0010000
#iter_0015000
#iter_0020000
#iter_0025000
#iter_0030000
CKPTS=(
iter_0035000
iter_0040000
iter_0045000
iter_0050000
)

EXAMPLE_CKPT=/gpfswork/rech/ajs/commun/code/bigcode/finetune/santacoderref
DUMP_PATH=/gpfswork/rech/ajs/commun/code/bigcode/finetune/santacoderlongconv
OUT_PREFIX=santacoderlong_

CKPT_PATH=/gpfswork/rech/ajs/commun/code/bigcode/finetune/santacoderlong

for i in {0..5}; do
CKPT=${CKPTS[$i]}
echo "$i"
echo "Running $CKPT"

OUTPUTCKPT=$DUMP_PATH/"$OUT_PREFIX$CKPT"

cd /gpfswork/rech/ajs/commun/code/bigcode/finetune/Megatron-LM
python -m tools.hf_transformers.convert_checkpoint --path_to_checkpoint $CKPT_PATH/$CKPT/mp_rank_00/model_optim_rng.pt --output-dir $OUTPUTCKPT

# Copy tokenizer.json etc
cp -r $EXAMPLE_CKPT/*.json $OUTPUTCKPT/
cp -r $EXAMPLE_CKPT/*.py $OUTPUTCKPT/

eval_script="./eval_$i.slurm"
cat <<EOT > $eval_script
#!/bin/bash
#SBATCH --job-name=eval
#SBATCH --ntasks=1                   # number of MP tasks
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8           # number of cores per tasks
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --time=10:00:00             # maximum execution time (HH:MM:SS)
#SBATCH --output=%x-%j.out          # output file name
#SBATCH --account=cnw@a100
#SBATCH --constraint=a100
#SBATCH --gres=gpu:1                # number of gpus

#source $six_ALL_CCFRWORK/start-tr13f-6B3-ml-t0
source $ajs_ALL_CCFRWORK/start-tr13f-6B3-ml-t0
conda activate bigcode

cd /gpfswork/rech/ajs/commun/code/bigcode/bigcode-evaluation-harness

accelerate launch --config_file config_1a100_fp16.yaml main.py \
--model $OUTPUTCKPT \
--tasks humaneval-x-bugs-python \
--do_sample False \
--n_samples 1 \
--batch_size 1 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method edit \
--generations_path generations_humanevalxbugs_$OUT_PREFIX$CKPT\_greedy.json \
--output_path evaluation_results_humanevalxbugs_$OUT_PREFIX$CKPT\_greedy.json \
--max_length_generation 2048
EOT

sbatch $eval_script

done