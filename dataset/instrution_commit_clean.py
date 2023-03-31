import random
import re
from collections import Counter
from difflib import SequenceMatcher
from multiprocessing import Pool, Value

import numpy as np
from datasets import load_dataset, concatenate_datasets
from huggingface_hub import hf_hub_download

CACHE_DIR = "YOU_CACHE_DIR"
DATASET_NAME = "bigcode/instruction-commits"
PUSH_DATASET_NAME = "bigcode/instruction-commits-filter"

# 1.0 mean keep all short commit messages
SHORT_SAMPLING = 0.2
LONG_SAMPLING_THRESHOLD = 500
LONG_SAMPLING = 0.1
MD_SAMPLING = 1.0

DATA_SAMPLING = 1.0

PROBA_STRICT_FILTERING = True
STRICT_PROBA_THRESHOLD = 0.01

# if enable resampling, it means you want to resample the dataset according to the probability of the
# commit message being instructions
PROBA_SOFT_RESAMPLING = False
SAMPLE_REPEAT_TIMES = 1
SOFT_PROBA_THRESHOLD = 0.1
LOW_QUALITY_SAMPLING_PROB = 0.1

assert not (PROBA_STRICT_FILTERING and PROBA_SOFT_RESAMPLING), "You can only enable one of the two options: ENABLE_PROBA_FILTERING and ENABLE_RESAMPLING"


# the ratio to control how many examples are fully shown in the model input, 0.2 means 20% examples will have
# the full code context such as the whole code file as the input
FULL_RANGE_FRAC = 0.2
# the minimum range and the maximum range represent the minimum context lines and the maximum context lines as the code context
MIN_RANGE = 0
MAX_RANGE = 32

dataset_description = "This dataset is built with the following parameters: \n" \
                        f"The sampling parameters to balance the code modification range as:\n" \
                        f"  SHORT_SAMPLING: {SHORT_SAMPLING}\n" \
                        f"  LONG_SAMPLING: {LONG_SAMPLING}\n" \
                        f"  LONG_SAMPLING_THRESHOLD: {LONG_SAMPLING_THRESHOLD}\n" \
                        f"  MD_SAMPLING: {MD_SAMPLING}\n" \
                        f"The sampling parameters to balance the programming language as:\n" \
                        f"  DATA_SAMPLING: {DATA_SAMPLING}\n" \
                        f"The sampling parameters to strictly filter the dataset using it's proba of being a good instruction as:\n" \
                        f"  PROBA_STRICT_FILTERING: {PROBA_STRICT_FILTERING}\n" \
                        f"  STRICT_PROBA_THRESHOLD: {STRICT_PROBA_THRESHOLD}\n" \
                        f"The sampling parameters to resample the dataset using it's proba of being a good instruction as:\n" \
                        f"  PROBA_SOFT_RESAMPLING: {PROBA_SOFT_RESAMPLING}\n" \
                        f"  SOFT_PROBA_THRESHOLD: {SOFT_PROBA_THRESHOLD}\n" \
                        f"  SAMPLE_REPEAT_TIMES: {SAMPLE_REPEAT_TIMES}\n" \
                        f"  LOW_QUALITY_SAMPLING_PROB: {LOW_QUALITY_SAMPLING_PROB}\n" \
                        f"The sampling parameters to control the code context range as:\n" \
                        f"  FULL_RANGE_FRAC: {FULL_RANGE_FRAC}\n" \
                        f"  MIN_RANGE: {MIN_RANGE}\n" \
                        f"  MAX_RANGE: {MAX_RANGE}\n"

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
    _ = p.map(download_file, data_files)

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

if PROBA_STRICT_FILTERING:
    ds = ds.filter(lambda x: x["proba"] >= STRICT_PROBA_THRESHOLD, num_proc=30)
    print("After proba strict filtering, the dataset size is {}".format(len(ds)))


ds = ds.filter(lambda x: len(x["old_contents"]) < 100_000, num_proc=30)

print("After content length filtering, the dataset size is: {}".format(len(ds)))

ds = ds.map(get_line_diff_range, num_proc=30)


def commit_filter(example):
    if len(example["new_contents"]) == 0:
        return False

    if example["old_change_range"] <= 2:
        if random.random() > SHORT_SAMPLING:
            return False

    if example["old_change_range"] >= LONG_SAMPLING_THRESHOLD:
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

    lower_subject = example["subject"].lower()

    # remove samples with bad messages
    if lower_subject in BAD_MESSAGE:
        return False

    # remove samples with bad subwords
    for bad_msg in BAD_SUB_MESSAGE:
        if bad_msg in lower_subject:
            return False

    # version updates (e.g. v1.1.0)
    if re.match(r"(?:v)?\d+\.\d+\.\d+(?=$|\S)", lower_subject):
        return False

    # commit message are hashes like 0239-2a41, but we do not want to remove english words like "debug"
    if re.match(r"^[a-f0-9]+(?:-[a-f0-9]+)*$", lower_subject):
        return False

    # weird messages that started with a whitespace and only contained one word
    if lower_subject.startswith(" ") and len(lower_subject.strip().split()) == 1:
        return False

    return True


ds_clean = ds.filter(commit_filter, num_proc=30)

print("After commit filtering, the dataset size is {}".format(len(ds_clean)))

if PROBA_SOFT_RESAMPLING:
    # repeat the dataset to make it larger
    ds_clean = concatenate_datasets([ds_clean] * SAMPLE_REPEAT_TIMES)

    def sub_sampling_based_on_proba(example):
        proba = example["proba"]
        if proba > SOFT_PROBA_THRESHOLD:
            return True
        elif random.random() < LOW_QUALITY_SAMPLING_PROB:
            return True
        return False


    ds_clean = ds_clean.filter(sub_sampling_based_on_proba, num_proc=30)
    print("After high proba filtering, the dataset size is {}".format(len(ds_clean)))


def prepare_code(example):
    if np.random.random() < FULL_RANGE_FRAC:
        example["size"] = len(f"<commit_before>{example['old_contents']}<commit_msg>{example['subject']}<commit_after>{example['new_contents']}")
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

        # rewrite the old and new contents
        example["old_contents"] = code_before
        example["new_contents"] = code_after
        example["size"] = len(f"<commit_before>{code_before}<commit_msg>{example['subject']}<commit_after>{code_after}")
    return example


ds_clean = ds_clean.map(prepare_code, num_proc=30)

# remove the samples that are too long
ds_clean = ds_clean.filter(lambda x: x["size"] < 4.0 * 2048, num_proc=30)

ds_final = ds_clean.remove_columns(
    ["message", "returncode", "stderr", "old_change_start", "old_change_end",
     "old_change_range", "new_change_start", 'new_change_end', 'new_change_range', 'n_inserts', 'n_deletes',
     'n_changes'])

print("Finish the data cleaning, the final dataset size is {}".format(len(ds_final)))

# add metadata
ds_final.info.description = dataset_description
ds_final.push_to_hub(PUSH_DATASET_NAME, private=True)
