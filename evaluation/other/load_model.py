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


from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

checkpoint = "instructcodet5p-16b"
#checkpoint = "/gpfsscratch/rech/ajs/commun/conv/starcoderbase/hf_checkpoints"
device = "cuda" # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint, trust_remote_code=True, torch_dtype="auto", device_map="auto", low_cpu_mem_usage=True)
func = '''from typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    for idx, elem in enumerate(numbers):\n        for idx2, elem2 in enumerate(numbers):\n            if idx != idx2:\n                distance = abs(elem - elem2)\n                if distance < threshold:\n                    return True\n\n    return False\n'''
inputs = tokenizer.encode(f"{func}\nProvide a concise natural language description of the above function using at most 100 characters.", return_tensors="pt").to(device)
outputs = model.generate(inputs, decoder_input_ids=inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))




from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "WizardCoder-15B-V1.0"
#checkpoint = "/gpfsscratch/rech/ajs/commun/conv/starcoderbase/hf_checkpoints"
device = "cuda" # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint, trust_remote_code=True, torch_dtype="auto", device_map="auto", low_cpu_mem_usage=True)

func = '''from typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    for idx, elem in enumerate(numbers):\n        for idx2, elem2 in enumerate(numbers):\n            if idx != idx2:\n                distance = abs(elem - elem2)\n                if distance < threshold:\n                    return True\n\n    return False\n'''
inputs = tokenizer.encode(f"{func}\nProvide a concise natural language description of the above function using at most 100 characters.", return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=20)
print(tokenizer.decode(outputs[0]))


inputs = tokenizer.encode(f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\nProvide a concise natural language description of the below function using at most 100 characters.\n{func}\n\n### Response:", return_tensors="pt").to(device)

inputs = tokenizer.encode(f"This function takes a list of numbers and a threshold value as input and returns True if there are any two elements in the list that are within a certain threshold distance of each other.\nWrite functional code in Python according to the description above.\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:", return_tensors="pt").to(device)



from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "starcoder-guanaco-45"
#checkpoint = "/gpfsscratch/rech/ajs/commun/conv/starcoderbase/hf_checkpoints"
device = "cuda" # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint, trust_remote_code=True, torch_dtype="auto", device_map="auto", low_cpu_mem_usage=True)

func = '''from typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    for idx, elem in enumerate(numbers):\n        for idx2, elem2 in enumerate(numbers):\n            if idx != idx2:\n                distance = abs(elem - elem2)\n                if distance < threshold:\n                    return True\n\n    return False\n'''
inst = "Provide a concise natural language description of the function using at most 100 characters."
inputs = tokenizer.encode(f"Question: {inst}\n{func}\n\nAnswer:", return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))


inputs = tokenizer.encode(f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\nProvide a concise natural language description of the below function using at most 100 characters.\n{func}\n\n### Response:", return_tensors="pt").to(device)

inputs = tokenizer.encode(f"This function takes a list of numbers and a threshold value as input and returns True if there are any two elements in the list that are within a certain threshold distance of each other.\nWrite functional code in Python according to the description above.\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:", return_tensors="pt").to(device)