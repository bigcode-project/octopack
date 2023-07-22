import datasets
import glob
import os
NUM_PROC = 4

LANGUAGES = os.listdir("data")

for L in LANGUAGES:

    if os.path.exists(f"data/{L}/data.jsonl"):
        continue

    PATHS = glob.glob(f"data/{L}/*.jsonl")
    print(PATHS)
    ds = datasets.load_dataset("json", data_files=PATHS, num_proc=NUM_PROC)["train"]

    print("Dataset size is: {}".format(len(ds)))

    ds = ds.filter(lambda x: "cherry picked from commit" not in x["subject"], num_proc=NUM_PROC)
    print("After hashtag filtering, the dataset size is: {}".format(len(ds)))

    # Check for any commit messages in the subject e.g. `Revert commit f514fe31f0c6efd4a18cfdfe8871aab65138afa3` or `See af25135c753845b3611c765c5baca1daac52c582` etc. using regex
    import re
    commit_regex = re.compile(r"([a-f0-9]{40})")
    ds = ds.filter(lambda x: not commit_regex.search(x["subject"]), num_proc=NUM_PROC)
    print("After commit filtering, the dataset size is: {}".format(len(ds)))

    # Remove [ci skip] from commit messages
    def remove_ci_skip(example):
        example["subject"] = example["subject"].replace("[ci skip]", "").strip()
        return example

    ds = ds.map(remove_ci_skip, num_proc=NUM_PROC)

    # Remove subject that starts with `Bump` with 90% probability
    import random
    def remove_bump(example):
        if example["subject"].startswith(("Bump", "Set version", "Update version")) and random.random() < 0.9:
            return False
        return True

    ds = ds.filter(remove_bump, num_proc=NUM_PROC)
    print("After rmv bump filtering, the dataset size is: {}".format(len(ds)))

    # Check if " I " is present in the commit subject
    def check_i(example):
        if " i " in example["subject"].lower() or "i've" in example["subject"].lower() or "i'm" in example["subject"].lower():
            return False
        return True

    ds = ds.filter(check_i, num_proc=NUM_PROC)
    print("After I filtering, the dataset size is: {}".format(len(ds)))


    # Check if `Thanks to` and `for` is present in the commit subject
    def check_thanks(example):
        if "thanks to" in example["subject"].lower() and "for" in example["subject"]:
            return False
        return True

    ds = ds.filter(check_thanks, num_proc=NUM_PROC)
    print("After thanks filtering, the dataset size is: {}".format(len(ds)))

    # Check if `code review` is present in the commit subject
    def check_code_review(example):
        if "code review" in example["subject"].lower():
            return False
        return True

    ds = ds.filter(check_code_review, num_proc=NUM_PROC)
    print("After code review filtering, the dataset size is: {}".format(len(ds)))


    # Remove some specific messages
    def rmv_specific(example):
        messages = [
            "fix that bug where things didn't work but now they should",
            "put the thingie in the thingie",
            'add a beter commit message',
        ]
        if example["subject"].lower() in messages:
            return False
        return True

    ds = ds.filter(rmv_specific, num_proc=NUM_PROC)
    print("After specific filtering, the dataset size is: {}".format(len(ds)))

    # Use regex to check for `...issue 159...` & `...bug 182...`
    import re
    issue_regex = re.compile(r"issue\s*\d+", re.IGNORECASE)
    bug_regex = re.compile(r"bug\s*\d+", re.IGNORECASE)
    feature_regex = re.compile(r"feature\s*\d+", re.IGNORECASE)
    def check_issue(example):
        if issue_regex.search(example["subject"].lower()) or bug_regex.search(example["subject"].lower()) or feature_regex.search(example["subject"].lower()):
            return False
        return True

    ds = ds.filter(check_issue, num_proc=NUM_PROC)
    print("After issue filtering, the dataset size is: {}".format(len(ds)))


    # Filter out anything with CDPCP in it
    def check_cdpcp(example):
        if "cdpcp" in example["subject"].lower():
            return False
        return True

    ds = ds.filter(check_cdpcp, num_proc=NUM_PROC)
    print("After cdpcp filtering, the dataset size is: {}".format(len(ds)))

    # Filter out anything with //codereview in it
    def check_codereview(example):
        if "//codereview" in example["subject"].lower():
            return False
        return True

    ds = ds.filter(check_codereview, num_proc=NUM_PROC)
    print("After codereview filtering, the dataset size is: {}".format(len(ds)))

    # Filter anything with Work in Progress or WIP
    def check_wip(example):
        if "work in progress" in example["subject"].lower() or "wip" in example["subject"].lower():
            return False
        return True

    ds = ds.filter(check_wip, num_proc=NUM_PROC)
    print("After wip filtering, the dataset size is: {}".format(len(ds)))

    # Filter anything with `https://` or `http://` in it
    def check_http(example):
        if "https://" in example["subject"].lower() or "http://" in example["subject"].lower():
            return False
        return True

    ds = ds.filter(check_http, num_proc=NUM_PROC)
    print("After http filtering, the dataset size is: {}".format(len(ds)))

    # Filter anything with `| LeetCode` in it
    def check_leetcode(example):
        if "| leetcode" in example["subject"].lower():
            return False
        return True

    ds = ds.filter(check_leetcode, num_proc=NUM_PROC)
    print("After leetcode filtering, the dataset size is: {}".format(len(ds)))

    # Filter for anything with <5 words
    def check_words(example):
        if len(example["subject"].split()) < 4:
            return False
        return True

    ds = ds.filter(check_words, num_proc=NUM_PROC)
    print("After words filtering, the dataset size is: {}".format(len(ds)))

    ds.to_json(f"data/{L}/data.jsonl", num_proc=NUM_PROC, force_ascii=False)
    """
    langs = ds.unique('lang')
    for lang in langs:
        ds.filter(lambda x: x['lang'] == lang).to_json(f"commits-ft/data/{lang}.jsonl", num_proc=NUM_PROC, force_ascii=False)
        cols_to_select = ["old_contents", "new_contents", "subject"]
        ds.filter(lambda x: x['lang'] == lang).select_columns(cols_to_select).to_json(f"commits-ft/short/{lang}.jsonl", num_proc=NUM_PROC, force_ascii=False)
    """

