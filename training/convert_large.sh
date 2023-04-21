# example for iter_5000
source $six_ALL_CCFRWORK/start-tr13f-6B3-ml-t0

### MERGE ###

OUTPUT_PATH=/gpfsscratch/rech/ajs/commun/large-model-megatron-180k-conv/iter_5000

python Megatron-LM/tools/checkpoint_util.py \
        --model-type GPT  \
        --load-dir /gpfsscratch/rech/ajs/commun/large-model-megatron-180k/iter_5000 \
        --save-dir $OUTPUT_PATH \
        --target-tensor-parallel-size 1 \
        --target-pipeline-parallel-size 1 \
        --use-distributed-optimizer | tee $OUTPUT_PATH/checkpoint_util_200k.log

### CONVERT ###

export PYTHONPATH=/fsx/loubna/code/new/Megatron-LM
cd transformers/src/transformers/models

python -m megatron_gpt_bigcode.push_checkpoints \
    --exp_dir $OUTPUT_PATH \
    --repo_name bigcode/large-model-ft \
    --branch_name main \
    --iter_interval 5000