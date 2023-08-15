import os
import json

RENAME_MAP = {
    "humanevalxexpgen": "humanevalexplainsynthesize",
    "hexexpgenerate": "humanevalexplainsynthesize",
    "hexexplaingen": "humanevalexplainsynthesize",
    "hexexpdesc": "humanevalexplaindescribe",
    "humanevalxexpdescribe": "humanevalexplaindescribe",
    "humanevalxexpdesc": "humanevalexplaindescribe",
    "hexexplaindesc": "humanevalexplaindescribe",
    "hexexpdescribe": "humanevalexplaindescribe",
    "hexexplaindescribe": "humanevalexplaindescribe",
    "hexbugs": "humanevalfix",
    "humanevalxbugs": "humanevalfix",
    "humanevalxgenerate": "humanevalsynthesize",
    "hexgenerate": "humanevalsynthesize",
}

DIR = "evaluation"

# Rename all file paths in the directory & subdirectories
for root, dirs, files in os.walk(DIR):
    for file in files:
        if file.endswith(".json") and any(x in file for x in RENAME_MAP):
            # Rename file
            for k, v in RENAME_MAP.items():
                if k in file:
                    new_file_name = file.replace(k, v)
                    os.rename(os.path.join(root, file), os.path.join(root, new_file_name))
                    print(f"Renamed {file} to {new_file_name}")
                    break
