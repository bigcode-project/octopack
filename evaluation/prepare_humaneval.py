import json
import os
from create_instructions import python_instruct, cpp_instruct, java_instruct, javascript_instruct, rust_instruct, go_instruct

paths = [
    "humaneval-x/data/cpp/data/humaneval.jsonl",
    "humaneval-x/data/go/data/humaneval.jsonl",
    "humaneval-x/data/java/data/humaneval.jsonl",
    "humaneval-x/data/js/data/humaneval.jsonl",
    "humaneval-x/data/python/data/humaneval.jsonl",
    "humaneval-x/data/rust/data/humaneval.jsonl",    
]

### Prepare HumanEval data for manual adding bugs (Easiest in json format in VSCode with formatting) ###

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

MANUAL_ENTRY_NAMES = {
    "get_max_triples": "get_matrix_triples", # cpp & Rust

    "digitsum": "digitSum", # Java & JS
    "closestInteger": "closest_integer", # Java (It's accidentally not in camelCase in the original data)
    "wordsString": "words_string", # Java
    "minsubarraysum": "minSubarraySum", # Java & JS
    "minpath": "minPath", # Java & JS
    "fileNameCheck": "filenameCheck", # Java
    "specialfilter": "specialFilter", # Java
    "sortedListSum": "listSort", # Java (There's a mistake in Python where it's called listSort in the docstring)
    "strongestExtension": "StrongestExtension", # Java

    "max_element": "maximum", # Rust
    "minSubArraySum": "min_sub_array_sum", # Rust
    "minPath": "min_path", # Rust
    "specialFilter": "special_filter", # Rust
    "Strongest_Extension": "strongest_extension", # Rust
}

# It's okay if these are not in the docstring
NOT_IN_DOCSTRING = {
    "make_palindrome", # "is_palindrome_10" is in docstring instead
    "decode_shift",
}

for p, p_or in zip(paths_bugs, paths):
    with open(p, "r") as f:
        data = json.load(f)
    with open(p_or, "r") as f:
        data_or = [json.loads(line) for line in f]
    # Write in jsonl format
    with open(p_or.replace(".", "bugs."), "w") as f:
        for i, (line, line_bugs, line_bugs_py, line_original) in enumerate(zip(data_or, data, python_data, he_original)):
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
            # Remove metadata from Python
            elif "/python/" in p:
                line["test"] = line["test"].replace("METADATA = {\n    'author': 'jt',\n    'dataset': 'test'\n}", "").replace("METADATA = {}", "")
            # Special case
            if (line["entry_point"] == "iscube") and ("/rust/" in p or "/cpp/" in p):
                line["entry_point"] = "iscuber"
            # Check function name appears in prompt
            if line["entry_point"] not in line["declaration"] + line["prompt"]:
                if line["entry_point"] in MANUAL_ENTRY_NAMES:
                    line["entry_point"] = MANUAL_ENTRY_NAMES[line["entry_point"]]
                elif line["entry_point"] not in NOT_IN_DOCSTRING:
                    print("Not in docstring", i, p, line["entry_point"])

            # Add instructions
            if "/python/" in p:
                line = python_instruct(line)
            elif "/cpp/" in p:
                line = cpp_instruct(line)
            elif "/java/" in p:
                line = java_instruct(line)
            elif "/js/" in p:
                line = javascript_instruct(line)
            elif "/go/" in p:
                line = go_instruct(line)
            elif "/rust/" in p:
                line = rust_instruct(line)
            else:
                raise NotImplementedError
            
            f.write(json.dumps(line) + "\n")

