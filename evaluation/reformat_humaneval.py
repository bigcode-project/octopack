import json
import sys
#from datasets import load_dataset

#ds = load_dataset("humaneval-x-bugs", "python", split="test")

path = sys.argv[1] # e.g. completions_python.jsonl

with open(path, "r") as f:
  c = [json.loads(l) for l in f.readlines()]

with open(path.replace("jsonl", "json"), "w") as f:
    json.dump(
        [[x["prompt"] + x["generation"]] for x in c], f
    )