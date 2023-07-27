CMD=" \
    finetune.py \
    --model_path="bigcode/starcoder" \
    --dataset_name="ArmelR/guanaco-commits" \
    --seq_length 2048 \
    --max_steps 1000 \
    --batch_size 1 \
    --input_column_name="prompt" \
    --output_column_name="completion" \
    --gradient_accumulation_steps 4 \
    --learning_rate 5e-4 \
    --lr_scheduler_type="cosine"\
    --log_freq 1 \
    --eval_freq 1 \
    --num_warmup_steps 5 \
    --save_freq 5 \
    --weight_decay 0.05 \
    --output_dir="./checkpoints-guanaco-commits" \
"


export LAUNCHER="python3 -u -m torch.distributed.run \
    --nproc_per_node $GPUS_PER_NODE \
    --nnodes $NNODES \
    --rdzv_endpoint $MASTER_ADDR:$MASTER_PORT \
    --rdzv_backend c10d \
    --max_restarts 0 \
    --tee 3 \
    "