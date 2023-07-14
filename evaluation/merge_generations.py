import json
import os
import glob
import sys

pattern = sys.argv[1]
out_name = pattern.replace("_*", "")

if not ".json" in out_name:
    out_name += ".json"

print("Saving to ", out_name)

assert "0" not in pattern


files = sorted(glob.glob(pattern), key=lambda x: int(x.split("_")[-1].split(".")[0]))

all_data = []
for fname in files:
    with open(fname, "r") as f:
      data = json.load(f)
      # It's of form [[x], [y]..]
      if (len(data) > 1) and (len(data[0]) == 1):
        all_data.extend([[x[0] for x in data]])
      # It's of form [[x, y..]]
      else:
        all_data.extend(data)

with open(out_name, "w") as f:
    json.dump(all_data, f)

"""
python main.py \
--model starcoder \
--tasks humaneval-x-generate-cpp \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method starcodercommit \
--load_generations_path generations_hexexplaingencpp_starcoder.json \
--metric_output_path evaluation_hexexplaingencpp_starcoder.json \
--max_length_generation 2048 \
--precision bf16

python main.py \
--model bloomz \
--tasks humaneval-x-generate-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method instruct \
--load_generations_path generations_humanevalxexpgenpy_bloomz_temp02.json \
--metric_output_path evaluation_humanevalxexpgenpy_bloomz_temp02.json \
--max_length_generation 2048 \
--precision bf16

python main.py \
--model starcoder-guanaco-instruct-500 \
--tasks humaneval-x-generate-python \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method instruct-qa \
--load_generations_path generations_hexexplaingenpython_starcoderguanacosj.json \
--metric_output_path evaluation_hexexplaingenpython_starcoderguanacosi.json \
--max_length_generation 2048 \
--precision bf16


python main.py \
--model starcoder-guanaco-xp3x-45 \
--tasks humaneval-x-bugs-python-tests \
--do_sample True \
--temperature 0.2 \
--n_samples 20 \
--batch_size 5 \
--allow_code_execution \
--save_generations \
--trust_remote_code \
--mutate_method instruct-qa \
--load_generations_path generations_hexbugspython_starcoderguanacoxp3x.json \
--metric_output_path evaluation_hexbugspython_starcoderguanacoxp3x.json \
--max_length_generation 2048 \
--precision bf16
"""
