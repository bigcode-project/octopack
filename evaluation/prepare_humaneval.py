import json

paths = [
    "humaneval-x/data/cpp/data/humaneval.jsonl",
    "humaneval-x/data/go/data/humaneval.jsonl",
    "humaneval-x/data/java/data/humaneval.jsonl",
    "humaneval-x/data/js/data/humaneval.jsonl",
    "humaneval-x/data/python/data/humaneval.jsonl",
]

for p in paths:
    with open(p, "r") as f:
        data = [json.loads(line) for line in f]

    with open(p.replace(".", "bugs."), "w") as f:
        for line in data:
            line["buggy_solution"] = line["canonical_solution"]
            line["bug_type"] = "variable misuse"
            line["failure_symptoms"] = "incorrect output"
            f.write(json.dumps(line) + "\n")

    with open(p.replace(".jsonl", "bugs.json"), "w") as f:
        out = []
        for line in data:
            line = {"buggy_solution": line["canonical_solution"]}
            if "python" in p:
                line["bug_type"] = "variable misuse"
                line["failure_symptoms"] = "incorrect output"
            out.append(line)
        f.write(json.dumps(out))

