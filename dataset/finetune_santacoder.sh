#!/bin/bash
#SBATCH --job-name=santacoder
#SBATCH --partition=gpu_p5
#SBATCH --constraint=a100
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1          # crucial - only 1 task per dist per node!
#SBATCH --cpus-per-task=64           # number of cores per tasks
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --gres=gpu:8                 # number of gpus
#SBATCH --time 20:00:00             # maximum execution time (HH:MM:SS)
#SBATCH --output=%x-%j.out           # output file name
#SBATCH --account=cnw@a100

set -u # stop on unset variables

source $six_ALL_CCFRWORK/start-tr13f-6B3-ml-t0
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

echo "START TIME: $(date)"

# Runs the SantaCoder 1B model
GPUS_PER_NODE=8
MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
MASTER_PORT=6001
NNODES=$SLURM_NNODES
NODE_RANK=$SLURM_PROCID
WORLD_SIZE=$(($GPUS_PER_NODE*$NNODES))

DISTRIBUTED_ARGS="--nproc_per_node $GPUS_PER_NODE --nnodes $NNODES --node_rank $NODE_RANK --master_addr $MASTER_ADDR --master_port $MASTER_PORT"

CHECKPOINT_PATH=/gpfswork/rech/ajs/commun/code/bigcode/finetune/santacoder
WEIGHTS_TRAIN=/gpfswork/rech/ajs/commun/code/bigcode/finetune/train_data_paths.txt.tmp
# "train: 1.0 0:0.950 /gpfswork/rech/ajs/commun/code/bigcode/finetune/train"
WEIGHTS_VALID=/gpfswork/rech/ajs/commun/code/bigcode/finetune/valid_data_paths.txt.tmp
# "validation: 1.0 0.950:1 /gpfswork/rech/ajs/commun/code/bigcode/finetune/train"
TOKENIZER_FILE=/gpfswork/rech/ajs/commun/code/bigcode/bigcode-evaluation-harness/santacoder/tokenizer.json 

# Changes:
# Doubled LR
# Added min LR i.e. decay to 10%
# Changed warmup fraction to 1% (from 2%)
# Changed eval / save intervals
# Remove fim

GPT_ARGS="\
--tensor-model-parallel-size 1 \
--pipeline-model-parallel-size 1 \
--recompute-activations \
--num-layers 24 \
--hidden-size 2048 \
--num-attention-heads 16 \
--attention-head-type multiquery \
--init-method-std 0.022 \
--seq-length 2048 \
--max-position-embeddings 2048 \
--attention-dropout 0.1 \
--hidden-dropout 0.1 \
--micro-batch-size 2 \
--global-batch-size 192 \
--lr 0.0004 \
--min-lr 0.00004 \
--train-iters 5000 \
--lr-decay-iters 5000 \
--lr-decay-style cosine \
--lr-warmup-fraction 0.01 \
--weight-decay .1 \
--adam-beta2 .95 \
--clip-grad 1.0 \
--fp16 \
--log-interval 10 \
--save-interval 2500 \
--eval-interval 500 \
--eval-iters 10 \
--initial-loss-scale 65536 \
"
#--fim-rate 0.5 \


TENSORBOARD_ARGS="--tensorboard-dir ${CHECKPOINT_PATH}/tensorboard"

CMD=" \
    finetune_mtf.py \
    $GPT_ARGS \
    --tokenizer-type TokenizerFromFile \
    --tokenizer-file $TOKENIZER_FILE \
    --save $CHECKPOINT_PATH \
    --load $CHECKPOINT_PATH \
    --train-weighted-split-paths-path $WEIGHTS_TRAIN \
    --valid-weighted-split-paths-path $WEIGHTS_VALID \
    --valid_num_workers 0 \
    --structured-logs \
    --structured-logs-dir $CHECKPOINT_PATH/logs \
    $TENSORBOARD_ARGS \
    "

export LAUNCHER="python -u -m torch.distributed.run \
    --nproc_per_node $GPUS_PER_NODE \
    --nnodes $NNODES \
    --rdzv_endpoint $MASTER_ADDR:$MASTER_PORT \
    --rdzv_backend c10d \
    --max_restarts 0 \
    --tee 3 \
    "

echo $CMD

SRUN_ARGS=" \
    --wait=60 \
    --kill-on-bad-exit=1 \
    "

# py-spy top -s -i -n -- $LAUNCHER --node_rank $SLURM_PROCID --role $SLURMD_NODENAME: $CMD
clear; srun $SRUN_ARGS --jobid $SLURM_JOB_ID bash -c "$LAUNCHER --node_rank \$SLURM_PROCID --role \$SLURMD_NODENAME: $CMD" 2>&1 | tee $LOG_PATH

rm -rf $CHECKPOINT_PATH

echo "END TIME: $(date)"
