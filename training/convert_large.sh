# example for iter_5000
source $six_ALL_CCFRWORK/start-tr13f-6B3-ml-t0

### MERGE ###

OUTPUT_PATH=/gpfsscratch/rech/ajs/commun/Bigcode-large-megatron_conv/base

cd /gpfsdswork/projects/rech/ajs/commun/code/bigcode/finetune

python Megatron-LM-ckpt/tools/checkpoint_util.py \
        --model-type GPT  \
        --load-dir /gpfsscratch/rech/ajs/commun/Bigcode-large-megatron \
        --save-dir $OUTPUT_PATH \
        --target-tensor-parallel-size 1 \
        --target-pipeline-parallel-size 1 \
        --use-distributed-optimizer | tee $OUTPUT_PATH/checkpoint_util.log

### CONVERT ###

# Megatron-LM should be this branch: https://github.com/bigcode-project/Megatron-LM/pull/40
export PYTHONPATH=/gpfsdswork/projects/rech/ajs/commun/code/bigcode/finetune/Megatron-LM-ckpt:${PYTHONPATH}
export PYTHONPATH=/gpfsdswork/projects/rech/ajs/commun/code/bigcode/finetune/transformers/src:${PYTHONPATH}
# transformers should be https://github.com/bigcode-project/transformers on branch `conv`
cd transformers/src/transformers/models

python -m megatron_gpt_bigcode.push_checkpoints \
    --exp_dir $OUTPUT_PATH \
    --repo_name Muennighoff/star \
    --branch_name base2 \
    --iter_interval 250000


python -m tools.hf_transformers.convert_checkpoint --path_to_checkpoint /gpfsscratch/rech/ajs/commun/Bigcode-large-megatron_conv/base/iter_0250000/mp_rank_00/model_optim_rng.pt --output-dir /gpfsscratch/rech/ajs/commun/Bigcode-large-megatron_conv/base3
