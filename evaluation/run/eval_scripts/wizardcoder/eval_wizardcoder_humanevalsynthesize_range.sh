#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -p small-g
#SBATCH -t 2:00:00
#SBATCH --gpus-per-node=mi250:1
#SBATCH --exclusive=user
#SBATCH --hint=nomultithread
#SBATCH --account=project_462000241
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err

source /pfs/lustrep2/scratch/project_462000241/muennighoff/venv/bin/activate
cd /pfs/lustrep2/scratch/project_462000185/muennighoff/bigcode-evaluation-harness
LANG=python

# Iterate through all possible combinations of config and run the jobs
for ((i=0; i<164; i++)); do
    eval_script="./eval_humanevalsynthesize$LANG\_$i.slurm"
    SAVE_GEN_PATH=generations_humanevalsynthesize$LANG\_wizardcoder_$i.json
    METRIC_OUTPUT_PATH=evaluation_humanevalsynthesize$LANG\_wizardcoder_$i.json
    # Skip if exists
    if [ -f $SAVE_GEN_PATH ]; then
        echo "Skipping $i"
        continue
    fi
    PORT=$((40740 + $i))
    cat <<EOT > $eval_script
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -p small-g
#SBATCH -t 4:00:00
#SBATCH --gpus-per-node=mi250:1
#SBATCH --exclusive=user
#SBATCH --hint=nomultithread
#SBATCH --account=project_462000241
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err

source /pfs/lustrep2/scratch/project_462000241/muennighoff/venv/bin/activate
cd /pfs/lustrep2/scratch/project_462000185/muennighoff/bigcode-evaluation-harness

accelerate launch --config_file config_1gpus_bf16.yaml --main_process_port $PORT main.py \
--model WizardCoder-15B-V1.0 \
--tasks humanevalsynthesize-$LANG \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--limit 1 \
--limit_start $i \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--prompt wizardcoder \
--save_generations_path $SAVE_GEN_PATH \
--metric_output_path $METRIC_OUTPUT_PATH \
--max_length_generation 2048 \
--generation_only \
--precision bf16
EOT
    # Submit the job
    sbatch $eval_script
    # Sleep for a bit to avoid hitting the job submission limit
    sleep 1
done
