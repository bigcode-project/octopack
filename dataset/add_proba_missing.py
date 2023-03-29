import json
import random
import os
import datasets

NUM_PROC = 16
if __name__ == "__main__":
    for lang in ["python", "java", "javascript"]:
        
        paths = os.listdir(f"tasky-commits/{lang}_add")
        paths = [f"tasky-commits/{lang}_add/{path}" for path in paths]
        ds = datasets.load_dataset("json", data_files=paths)["train"]

        COMMIT_TO_PROBA = {}
        for i in range(len(ds)):
            COMMIT_TO_PROBA[ds[i]["commit"]] = ds[i]["proba"]

        def map_col(example):
            example["proba"] = COMMIT_TO_PROBA.get(example["commit"], -1)
            return example

        paths = os.listdir(f"data/{lang}")
        for i in range(len(paths)):
            ds = datasets.load_dataset("json", data_files=[f"data/{lang}/{paths[i]}"])["train"]
            # -1 are the ones that were previously skipped & need to be added
            ds.filter(lambda x: x["proba"] == -1).map(map_col).to_json(f"data/{lang}/{paths[i]}", num_proc=NUM_PROC)