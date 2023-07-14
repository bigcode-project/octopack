
from datasets import load_dataset
import os
import glob

paths = list(glob.glob("*.jsonl"))
ds = load_dataset("json", data_files=paths)["train"]

#dsf = ds.filter(lambda x: "Fix" in x["subject"])
ds = ds.filter(lambda x: any([y in x["new_contents"] for y in ["torch", "numpy", "tensorflow", "chainer"]])) #  "tensorflow", "jax"
ds = ds.filter(lambda x: len(x["old_contents"]) > 0) #  "tensorflow", "jax"
ds = ds.filter(lambda x: len(x["subject"]) < 50) #  "tensorflow", "jax"
ds = ds.filter(lambda x: "version" not in x["subject"]) #  "tensorflow", "jax"
ds = ds.filter(lambda x: 20 < (len(x["old_contents"]) + len(x["new_contents"])) < 1000)
