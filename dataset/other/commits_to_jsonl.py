import datasets
import random

NUM_PROC = 32
ds = datasets.load_dataset("commits-8192")["train"]

def prepare(example):
    example["inputs"] = f"<commit_before>{example['old_contents']}<commit_msg>"
    example["targets"] = f"{example['subject']}<commit_after>{example['new_contents']}<|endoftext|>"
    return example

def prepare_code(example):
    example["inputs"] = f"```\n{example['old_contents']}\n```\n"
    example["targets"] = f"{example['subject']}\n```\n{example['new_contents']}\n```<|endoftext|>"
    return example

def prepare_bigcode(example):
    # With 50% probability add filename
    if random.random() < 0.5:
        example["inputs"] = f"<filename>{example['old_file'].split('/')[-1]}<commit_before>{example['old_contents']}<commit_msg>"
    else:
        example["inputs"] = f"<commit_before>{example['old_contents']}<commit_msg>"
    example["targets"] = f"{example['subject']}<commit_after>{example['new_contents']}<|endoftext|>"
    return example

ds = ds.map(prepare_bigcode, num_proc=NUM_PROC).select_columns(["inputs", "targets"])
ds.to_json("out.jsonl", orient="records", lines=True, force_ascii=False, num_proc=NUM_PROC)
