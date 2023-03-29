### Prepare HumanEval data for manual adding bugs (Easiest in json format in VSCode with formatting) ###

import json
import os

if False:
    paths = [
        "humaneval-x/data/cpp/data/humaneval.jsonl",
        "humaneval-x/data/go/data/humaneval.jsonl",
        "humaneval-x/data/java/data/humaneval.jsonl",
        "humaneval-x/data/js/data/humaneval.jsonl",
        "humaneval-x/data/python/data/humaneval.jsonl",
        "humaneval-x/data/rust/data/humaneval.jsonl",    
    ]

    for p in paths:
        with open(p, "r") as f:
            data = [json.loads(line) for line in f]

        with open(p.replace(".jsonl", "bugs.json"), "w") as f:
            out = []
            for line in data:
                line = {"buggy_solution": line["canonical_solution"]}
                if "python" in p:
                    line["bug_type"] = "variable misuse"
                    line["failure_symptoms"] = "incorrect output"
                out.append(line)
            f.write(json.dumps(out))

### Load prepared HumanEval & format for usage ###

paths_bugs = [
    "humaneval-x/data/cpp/data/humanevalbugs.json",
    "humaneval-x/data/go/data/humanevalbugs.json",
    "humaneval-x/data/java/data/humanevalbugs.json",
    "humaneval-x/data/js/data/humanevalbugs.json",
    "humaneval-x/data/python/data/humanevalbugs.json",
]

with open("humaneval-x/data/python/data/humanevalbugs.json", "r") as f:
    python_data = json.load(f)

for p, p_or in zip(paths_bugs, paths):
    with open(p, "r") as f:
        data = json.load(f)
    with open(p_or, "r") as f:
        data_or = [json.loads(line) for line in f]
    # Write in jsonl format
    with open(p_or.replace(".", "bugs."), "w") as f:
        for line, line_bugs, line_bugs_py in zip(data_or, data, python_data):
            line["buggy_solution"] = line_bugs["buggy_solution"]
            line["bug_type"] = line_bugs_py["bug_type"]
            line["failure_symptoms"] = line_bugs_py["failure_symptoms"]
            f.write(json.dumps(line) + "\n")

