"""
This code is now integrated into bigcode-evaluation-harness when evaluating humanevalexplain.
If you evaluate externally, you may use this code to remove overlap between solutions and explanations.
"""

import json
from datasets import load_dataset
import os

path = "generations_hexexplaindesccpp_wizardcoder.json"

def remove_code(text, canonical_solution):
    for line in canonical_solution.split("\n"):
        line = line.strip()
        if len(line) > 20 and line in text:
            text = text.replace(line, "")
    return text

ds = load_dataset("humaneval-x-bugs", "python", split="test")

with open(path, "r") as f:
    data = json.load(f)

for i, (sample, gen) in enumerate(zip(ds, data)):
    for j, g in enumerate(gen):
        g_clean = remove_code(g, sample["canonical_solution"])
        if g_clean != g:
            print(f"Fixed {i}: {j}")
            # if i == 0:
            #     print(sample["canonical_solution"])
            #     print(g)
            #     print(g_clean)
            #data[i][j] = g_clean
            #if os.path.exists(f"generations_hexexplaingenpython_starcoderguanacosi_{i}.json"):
            #    print("renaming")
            #    os.rename(f"generations_hexexplaingenpython_starcoderguanacosi_{i}.json", f"tormv/generations_hexexplaingenpython_starcoderguanacosi_{i}.json")

with open(path.replace(".json", "_fixed.json"), "w") as f:
    json.dump(data, f)