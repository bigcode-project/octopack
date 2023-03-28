import datasets
path = "javascript_new.jsonl"
ds = datasets.load_dataset("json", data_files=[path])["train"]
# Remove all columns that are not "commit" or "message"
ds = ds.filter(lambda x: x["returncode"] == 0).select_columns(["commit", "message"]).to_json("javascript_messages.jsonl", num_proc=8)