import random
import re
from collections import Counter
from difflib import SequenceMatcher
from multiprocessing import Pool, Value

import ghdiff
import numpy as np
from datasets import load_dataset, concatenate_datasets
from huggingface_hub import hf_hub_download

opt_out_github_login_the_stack_12 = '''INSERT OPT OUT HERE'''.splitlines()
opt_out_github_login_the_stack_12 = [el.lower() for el in opt_out_github_login_the_stack_12]
CACHE_DIR = "YOU_CACHE_DIR"
DATASET_NAME = "bigcode/instruction-commits"
PUSH_DATASET_NAME = "bigcode/instruction-commits-filter"

# 1.0 mean keep all short commit messages
SHORT_SAMPLING = 1.0
LONG_SAMPLING = 0.1
MD_SAMPLING = 1.0
DATA_SAMPLING = 1.0

# the ratio to control how many examples are fully shown in the model input, 0.2 means 20% examples will have
# the full code context such as the whole code file as the input
FULL_RANGE_FRAC = 0.2
# the minimum range and the maximum range represent the minimum context lines and the maximum context lines as the code context
MIN_RANGE = 0
MAX_RANGE = 32

# the

DATA_EXT = {"json", "yml", "xml", "html"}

BAD_SUB_MESSAGE = [
    "auto commit",
    "update contributing",
    "<?xml",
    "merge branch",
    "merge pull request"
]

BAD_MESSAGE = [
    "readme",
    "update",
    "dummy",
    "updated",
    # "debug",
    "test",
    "update readme",
    "update readme.md",
    "updated readme.md",
    "updated readme",

]


def gh_diff(example):
    example["gh_diff"] = ghdiff.diff(example["old_contents"], example["new_contents"])
    return example


def get_line_diff_range(example):
    old_file_start = 0
    old_file_end = 0

    new_file_start = 0
    new_file_end = 0

    n_inserts = 0
    n_deletes = 0

    for group in SequenceMatcher(None, example["old_contents"].splitlines(),
                                 example["new_contents"].splitlines()).get_grouped_opcodes():
        group = [g for g in group if g[0] != "equal"]

        for element in group:
            if element[0] == "insert":
                n_inserts += element[4] - element[3]
            if element[0] == "delete":
                n_deletes += element[2] - element[1]
            if element[0] == "replace":
                n_deletes += element[2] - element[1]
                n_inserts += element[4] - element[3]

        first, last = group[0], group[-1]
        file1_range = (first[1], last[2])
        file2_range = (first[3], last[4])

        old_file_start = min(file1_range[0], old_file_start)
        old_file_end = max(file1_range[1], old_file_end)

        new_file_start = min(file2_range[0], new_file_start)
        new_file_end = max(file2_range[1], new_file_end)

    # -2 for compatibility with gh_diff
    example["old_change_start"] = old_file_start
    example["old_change_end"] = old_file_end
    example["old_change_range"] = old_file_end - old_file_start

    example["new_change_start"] = new_file_start
    example["new_change_end"] = new_file_end
    example["new_change_range"] = new_file_end - new_file_start

    example["n_inserts"] = n_inserts
    example["n_deletes"] = n_deletes
    example["n_changes"] = n_inserts + n_deletes

    return example


counter = Value('i', 0)


def init(args):
    ''' store the counter for later use '''
    global counter
    counter = args


def prepare_download_files():
    downloaded_files = []
    for i in range(1, 459):
        downloaded_files.append("data/python/python-{:04d}.jsonl".format(i))

    for i in range(1, 517):
        downloaded_files.append("data/javascript/javascript-{:04d}.jsonl".format(i))

    for i in range(1, 250):
        downloaded_files.append("data/java/java-{:04d}.jsonl".format(i))
    return downloaded_files


data_files = prepare_download_files()


def download_file(file):
    global counter
    print("start")
    file = hf_hub_download(DATASET_NAME, file, repo_type="dataset",
                           cache_dir=CACHE_DIR)
    with counter.get_lock():
        counter.value += 1
    print(counter.value)
    return file


# download files using multi-thread
with Pool(16, initializer=init, initargs=(counter,)) as p:
    _ = p.map(download_file, data_files[::2])

# obtain the file path
files = [hf_hub_download(DATASET_NAME, file, repo_type="dataset",
                         cache_dir=CACHE_DIR) for file in data_files]

counter = Value('i', 0)


def load_file(file):
    global counter
    print("start")
    file = load_dataset("/".join(file.split("/")[:-1]), data_files=file,
                        split="train", cache_dir=CACHE_DIR)
    with counter.get_lock():
        counter.value += 1
    print(counter.value)
    return file


with Pool(8, initializer=init, initargs=(counter,)) as p:
    ds_list = p.map(load_file, files)

ds = concatenate_datasets(ds_list)

print("The dataset size is: {}".format(len(ds)))

ds = ds.filter(lambda x: x["proba"] >= 0.9, num_proc=30)

print("After proba filtering, the dataset size is: {}".format(len(ds)))

ds = ds.filter(lambda x: len(x["old_contents"]) < 100_000, num_proc=30)

print("After content length filtering, the dataset size is: {}".format(len(ds)))

ds = ds.map(get_line_diff_range, num_proc=30)


def commit_filter(example):
    if len(example["new_contents"]) == 0:
        return False

    if example["old_change_range"] <= 2:
        if random.random() > SHORT_SAMPLING:
            return False

    if example["old_change_range"] >= 200:
        if random.random() > LONG_SAMPLING:
            return False

    if example["old_file"].split(".")[-1] == "md":
        if random.random() > MD_SAMPLING:
            return False

    if example["old_file"].split(".")[-1] in DATA_EXT:
        if random.random() > DATA_SAMPLING:
            return False

    if len(example["subject"]) == 0 or len(example["subject"].split()) == 0:
        return False

    # remove samples with bad subwords
    lower_subject = example["subject"].lower()
    for bad_msg in BAD_SUB_MESSAGE:
        if bad_msg in lower_subject:
            return False

    # remove samples with bad messages
    for bad_msg in BAD_MESSAGE:
        if bad_msg == lower_subject:
            return False

    # version updates (e.g. v1.1.0)
    if re.match(r"(?:v)?\d+\.\d+\.\d+(?=$|\S)", lower_subject):
        return False

    # high character/token ratio (e.g. hashes)
    if len(example["subject"]) / len(example["subject"].split()) > 20:
        return False

    # weird messages that started with a whitespace and only contained one word
    if lower_subject.startswith(" ") and len(lower_subject.strip().split()) == 1:
        return False

    return True


def check_uniques(example, uniques):
    """Check if current hash is still in set of unique hashes and remove if true."""
    if example["repos"] + "/" + example["old_file"] in uniques:
        uniques.remove(example["repos"] + "/" + example["old_file"])
        return True
    else:
        return False


uniques = set([r + "/" + filename for filename, r in zip(ds["old_file"], ds["repos"])])
print(len(uniques))

ds = ds.filter(check_uniques, fn_kwargs={"uniques": uniques}, num_proc=1)

ds_clean = ds.filter(commit_filter, num_proc=30)

print("After commit filtering, the dataset size is {}".format(len(ds_clean)))


def prepare_code(example):
    if np.random.random() < FULL_RANGE_FRAC:
        example["content"] = f"<commit_before>{example['old_contents']}<commit_msg>{example['subject']}<commit_after>{example['new_contents']}"
        example["size"] = len(example["content"])
    else:
        start_offset = np.random.randint(MIN_RANGE, MAX_RANGE)
        end_offset = np.random.randint(MIN_RANGE, MAX_RANGE)

        old_lines = example["old_contents"].splitlines()
        new_lines = example["new_contents"].splitlines()

        old_start = max(0, example["old_change_start"] - start_offset)
        new_start = max(0, example["new_change_start"] - start_offset)

        old_end = min(len(old_lines), example["old_change_end"] + end_offset)
        new_end = min(len(new_lines), example["new_change_end"] + end_offset)

        code_before = "\n".join(old_lines[old_start:old_end])
        code_after = "\n".join(new_lines[new_start:new_end])
        example["content"] = f"<commit_before>{code_before}<commit_msg>{example['subject']}<commit_after>{code_after}"
        example["size"] = len(example["content"])
    return example


ds_clean = ds_clean.map(prepare_code, num_proc=30)
opt_out_github_login_the_stack_12 = set([el.lower() for el in opt_out_github_login_the_stack_12])


def filter_opt_out(example):
    repo_names = example["repos"].split(",")
    try:
        repo_owners = [repo_name.split("/")[0].lower() for repo_name in repo_names]
    except:
        print(example["repos"])
    filtered_repo_names = [repo_name for repo_name, repo_owner in zip(repo_names,
                                                                      repo_owners) if
                           repo_owner not in opt_out_github_login_the_stack_12]

    if len(filtered_repo_names) > 0:
        example["repos"] = ",".join(filtered_repo_names)
        example["drop_opt_out"] = False
    else:
        example["repos"] = ""
        example["drop_opt_out"] = True
    return example


ds_opt_out = ds_clean.map(filter_opt_out, num_proc=30)
ds_opt_out = ds_opt_out.filter(lambda x: not x["drop_opt_out"], num_proc=30)

ds_final = ds_opt_out.remove_columns(
    ["subject", "message", "new_contents", "old_contents", "returncode", "stderr", "old_change_start", "old_change_end",
     "old_change_range", "new_change_start", 'new_change_end', 'new_change_range', 'n_inserts', 'n_deletes',
     'n_changes', 'drop_opt_out'])

print("Finish the data cleaning, the final dataset size is {}".format(len(ds_final)))
ds_final.push_to_hub(PUSH_DATASET_NAME, private=True)
