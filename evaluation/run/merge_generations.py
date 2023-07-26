"""
Merges generations when using the range eval scripts.
Usage: `python merge_generations.py "generations_humanevalfixpython_wizardcoder*.json"`
"""

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
