# pip install -q transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "/gpfsscratch/rech/ajs/commun/Bigcode-large-megatron_conv/base3"
device = "cpu" # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint, trust_remote_code=True).to(device)

inputs = tokenizer.encode("def print_hello_world():", return_tensors="pt").to(device)
outputs = model.generate(inputs)
print(tokenizer.decode(outputs[0]))


from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "/gpfsscratch/rech/ajs/commun/starcoderbase"
#checkpoint = "/gpfsscratch/rech/ajs/commun/conv/starcoderbase/hf_checkpoints"
device = "cuda" # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint, trust_remote_code=True, torch_dtype="auto", device_map="auto", low_cpu_mem_usage=True)

inputs = tokenizer.encode("def print_hello_world():", return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=1)
print(tokenizer.decode(outputs[0]))


