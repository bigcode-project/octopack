#! /bin/bash

# set -u # stop on unset variables

export WANDB_API_KEY= # your wandb key
export WANDB_PROJECT= # your wandb project name

NNODES=$WORLD_SIZE  # Adjust
GPUS_PER_NODE=8

GPU_NUM=$(($GPUS_PER_NODE*$NNODES))
WORLD_SIZE=$(($GPUS_PER_NODE*$NNODES))

echo "================================================"
echo "GPU_NUM: $GPU_NUM"
echo "================================================"

DISTRIBUTED_ARGS="\
              --nproc_per_node $GPUS_PER_NODE \
              --nnodes $NNODES \
              --node_rank $RANK \
              --master_addr $MASTER_ADDR \
              --master_port $MASTER_PORT \
"

echo $DISTRIBUTED_ARGS

CHECKPOINT_PATH=  # Adjust: Directory to store the checkpoints 
DATA_PATH=  # Adjust: Prefix of the preprocessed dataset.
TOKENIZER_FILE=  # Adjust: starcoder-tokenizer/tokenizer.json

GPT_ARGS="\
       --tensor-model-parallel-size 1 \
       --pipeline-model-parallel-size 1 \
       --recompute-activations \
       --num-layers 24 \
       --hidden-size 2048 \
       --num-attention-heads 16 \
       --attention-head-type multiquery \
       --init-method-std 0.022 \
       --seq-length 8192 \
       --max-position-embeddings 8192 \
       --attention-dropout 0.1 \
       --hidden-dropout 0.1 \
       --micro-batch-size 2 \
       --global-batch-size 64 \
       --lr 0.0002 \
       --train-iters 250000 \
       --lr-decay-iters 600000 \
       --lr-decay-style cosine \
       --lr-warmup-fraction 0.02 \
       --weight-decay .1 \
       --adam-beta2 .95 \
       --clip-grad 1.0 \
       --bf16 \
       --log-interval 10 \
       --save-interval 1000 \
       --eval-interval 500 \
       --eval-iters 10 \
       --initial-loss-scale 65536 \
"

TENSORBOARD_ARGS="--tensorboard-dir ${CHECKPOINT_PATH}/tensorboard"

torchrun $DISTRIBUTED_ARGS \
       pretrain_gpt.py \
       $GPT_ARGS \
       --tokenizer-type TokenizerFromFile \
       --tokenizer-file $TOKENIZER_FILE \
       --save $CHECKPOINT_PATH \
       --load $CHECKPOINT_PATH \
       --data-path $DATA_PATH \
       $TENSORBOARD_ARGS \
       --wandb-project-name # project name \
       --wandb-entity-name # entity name \