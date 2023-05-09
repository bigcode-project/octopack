
### WIP



#### Checkpoint conversion

- Update the paths in `convert_large.sh` & download the marked repos & run it

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