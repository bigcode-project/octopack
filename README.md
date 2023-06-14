
### Fine-tuning


1. Get the StarCoderBase Megatron-LM checkpoint: `git clone https://huggingface.co/bigcode/starcoderbase-megatron`
2. Get Megatron-LM: `git clone -b mtf https://github.com/bigcode-project/Megatron-LM`
3. Prepare a Python environment with PyTorch. (TODO: There may be some other packages needed that you will find out about when training fails)
4. Prepare dataset: Preapre a finetuning dataset in the form of a single jsonl file with two keys: `inputs` & `outputs`. `inputs` should contain the prompt and instruction while `outputs` contains the targets. Loss will only be computed over `outputs`. See `dataset/commits_to_jsonl.py` for an example of doing this. In that example we put the instruction (commit message) in the target, but it's better to put it in the input.
5. Tokenize the fine-tuning dataset by modifying `dataset/preprocess.sh` to point to your jsonl dataset. Also modify the path of the tokenizer, in our case point to the StarCoder's `tokenizer.json` (`wget https://huggingface.co/bigcode/starcoderbase/raw/main/tokenizer.json`). Finally specify an output prefix where the tokenized data will be stored. Then run it with `bash dataset/preprocess.sh`.
6. Create two files `train_data_paths.txt.tmp` and `valid_data_paths.txt.tmp` that contain the paths to the above created tokenized dataset. For example they could look like `"train: 1.0 0:0.95 output_prefix"` and `"valid: 1.0 0.95:1.0 output_prefix`. In this case the dataset is split into 95% training and 5% validation. The first number is the weight of the dataset, the second number is the start of the dataset and the third number is the end of the dataset.
7. Rename the checkpoint downloaded to `release` i.e. `mv starcoderbase-megatron/iter* starcoderbase-megatron/release` and create a file `starcoderbase-megatron/latest_checkpointed_iteration.txt` that contains simply `release` (`echo release > starcoderbase-megatron/latest_checkpointed_iteration.txt`).
8. Modify `training/finetune_starcoderbase.sh` to adapt `CHECKPOINT_PATH` to point to the downloaded Megatron-LM checkpoint, `WEIGHTS_TRAIN` & `WEIGHTS_VALID` to point to the above created txt files, `TOKENIZER_FILE` to StarCoder's `tokenizer.json`, point to your environment and cache locations, and modify the SBATCH settings to suit your setup. Then run it with `bash training/finetune_starcoderbase.sh`. You can interrupt and resume training, however, if you resume, you need to remove `--no_load_optim` and `--no_load_rng` from the command line arguments in the script to load the optimizer and random number generator state from the newly saved checkpoint (we only do not want to load them from starcoderbase).
9. Convert the saved checkpoint using the instructions below.


#### Checkpoint conversion

1. Update the paths in `convert_large.sh` & download the marked repos & run it

#### Other

for idx in ["00001", "00002", "00003", "00004", "00005", "00006", "00007"]:
    x = torch.load(f"/gpfsscratch/rech/ajs/commun/Bigcode-large-megatron_conv/base/shard2/pytorch_model-{idx}-of-00007.bin")
    y = torch.load(f"/gpfsscratch/rech/ajs/commun/starcoderbase/pytorch_model-{idx}-of-00007.bin")
    assert x.keys() == y.keys()
    for k in x.keys():
        if not((x[k] == y[k]).all()):
            print(k)
            print(x[k].shape)
            print(y[k].shape)
            break

# pip install -q transformers
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "/gpfsscratch/rech/ajs/commun/Bigcode-large-megatron_conv/base/shard"
checkpoint = "/gpfsscratch/rech/ajs/commun/Bigcode-large-megatron_conv/base3/"
device = "cuda" # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(
    checkpoint, 
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
).to(device)

inputs = tokenizer.encode("def print_hello_world():", return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=1)
print(tokenizer.decode(outputs[0]))
```