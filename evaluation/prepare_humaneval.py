### Prepare HumanEval data for manual adding bugs (Easiest in json format in VSCode with formatting) ###

import json
import os

paths = [
    "humaneval-x/data/cpp/data/humaneval.jsonl",
    "humaneval-x/data/go/data/humaneval.jsonl",
    "humaneval-x/data/java/data/humaneval.jsonl",
    "humaneval-x/data/js/data/humaneval.jsonl",
    "humaneval-x/data/python/data/humaneval.jsonl",
    "humaneval-x/data/rust/data/humaneval.jsonl",    
]

if False:

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
    "humaneval-x/data/rust/data/humanevalbugs.json",
]

with open("humaneval-x/data/python/data/humanevalbugs.json", "r") as f:
    python_data = json.load(f)

with open("humaneval-x/HumanEval_original.jsonl", "r") as f:
    he_original = [json.loads(line) for line in f]

for p, p_or in zip(paths_bugs, paths):
    with open(p, "r") as f:
        data = json.load(f)
    with open(p_or, "r") as f:
        data_or = [json.loads(line) for line in f]
    # Write in jsonl format
    with open(p_or.replace(".", "bugs."), "w") as f:
        for line, line_bugs, line_bugs_py, line_original in zip(data_or, data, python_data, he_original):
            line["buggy_solution"] = line_bugs["buggy_solution"]
            line["bug_type"] = line_bugs_py["bug_type"]
            line["failure_symptoms"] = line_bugs_py["failure_symptoms"]
            line["entry_point"] = line_original["entry_point"]
            # Go use camelCase hence need to remove _ & capitalize i.e. "hello_world" -> "HelloWorld"
            if "/go/" in p:
                line["entry_point"] = line["entry_point"].replace("_", " ").title().replace(" ", "")
            # Java / JS use camelCase but with first letter lowercase i.e. "hello_world" -> "helloWorld"
            elif "/java/" in p or "/js/" in p:
                line["entry_point"] = line["entry_point"].replace("_", " ").title().replace(" ", "")[0].lower() + line["entry_point"].replace("_", " ").title().replace(" ", "")[1:]
            f.write(json.dumps(line) + "\n")

