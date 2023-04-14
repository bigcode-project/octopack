import datasets

NUM_PROC = 64
ds = datasets.load_dataset("commits-pjj-2048")["train"]

def prepare(example):
    example["inputs"] = f"<commit_before>{example['old_contents']}<commit_msg>"
    example["targets"] = f"{example['subject']}<commit_after>{example['new_contents']}<|endoftext|>"
    return example

ds = ds.map(prepare, num_proc=NUM_PROC).select_columns(["inputs", "targets"])
ds.to_json("out.jsonl", orient="records", lines=True, force_ascii=False, num_proc=NUM_PROC)