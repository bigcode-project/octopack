import json
import random
import os
import datasets

NUM_PROC = 16
if __name__ == "__main__":
    for lang in ["python", "java", "javascript"]:
        
        paths = os.listdir(f"tasky-commits/{lang}")
        paths = [f"tasky-commits/{lang}/{path}" for path in paths]
        ds = datasets.load_dataset("json", data_files=paths)["train"]

        COMMIT_TO_PROBA = {}
        for i in range(len(ds)):
            COMMIT_TO_PROBA[ds[i]["commit"]] = ds[i]["proba"]

        def map_col(example):
            example["proba"] = COMMIT_TO_PROBA[example["commit"]]
            return example

        paths = os.listdir(f"{lang}")
        for i in range(len(paths)):
            ds = datasets.load_dataset("json", data_files=[f"{lang}/{paths[i]}"])["train"]
            ds.map(map_col).to_json(f"{lang}/{paths[i]}")