from concurrent.futures import ThreadPoolExecutor
import os
import random
import subprocess
import timeit

import datasets

"""Example
git init
git remote add origin https://github.com/huggingface/evaluate.git
git fetch --depth 2 origin 9b056cdd5eb95459ae80142014865263e7dd75b8
# Get file after change
git checkout FETCH_HEAD -- README.md
# Get file before change
git checkout FETCH_HEAD^ -- README.md
"""

# In the multiprocessing case, the below leads to each process creating the same directory
# random = random.Random(42)  # make it reproducible

NUM_THREADS = 1
NUM_PROC = 4
# DEBUG_SIZE = 1024

CWD = os.getcwd()

# Shell utils
def run_in_shell(cmd: str, cwd=None, timeout=60):
    return subprocess.run([cmd], capture_output=True, shell=True, cwd=cwd, timeout=timeout)

def get_file_contents(commit, repo ,old_file =None,     new_file =None, cwd=None):
    completed = run_in_shell("git init", cwd=cwd)
    completed = run_in_shell("git remote add origin " + repo, cwd=cwd)
    completed = run_in_shell("git fetch --depth 2 origin " + commit, cwd=cwd)
     # If it requires authentication
    if completed.returncode != 0:
        print("ERRORC1", completed)
        return ("", "", completed.returncode, completed.stderr.decode(errors='ignore'))
    # Optionally do git diff at the same time (Saving code needs to be added)
    # git_diff = run_in_shell(f"git diff {commit}^ {commit}", cwd=cwd).stdout.decode(errors='ignore')


    completed = run_in_shell("git checkout FETCH_HEAD -- " + new_file, cwd=cwd)
    new_contents = run_in_shell("cat " + new_file, cwd=cwd).stdout.decode(errors='ignore')
    completed = run_in_shell("git checkout FETCH_HEAD^ -- " + old_file, cwd=cwd)
    # If there's only a new file, but no old file
    if completed.returncode != 0:
        #print("ERRORC2", completed)
        return (new_contents, "", completed.returncode, completed.stderr.decode(errors='ignore'))
    old_contents = run_in_shell("cat " + old_file, cwd=cwd).stdout.decode(errors='ignore')
    return (new_contents, old_contents, completed.returncode, completed.stderr.decode(errors='ignore'))

def get_diff(ex):

    repos = [ex['repository']['url']]

    #exit()
    # commit_id = ex["commit"]
    # repos = list(set(ex["repos"].split(",")))
    # old_file = ex["old_file"]
    # new_file = ex["new_file"]
    # Initialize
    returncode = 0
    stderr = "unknown"

    for i, repo_url in enumerate(repos):
        #repo = "https://xxx:xxx@github.com/" + repo + ".git"
        repo =  repo_url #"https://github.com/linkedin/rest.li.git"
        # Create a random directory to store the repo

        random_dir = CWD + "/" + str(random.randint(0, 1000000))
        # Can take very long when running many processes
        run_in_shell("mkdir " + random_dir, timeout=300)
        run_in_shell("git clone " + repo + " " + random_dir, timeout=300)
        run_in_shell("cd " + random_dir, timeout=300)
        commit_history = run_in_shell('git log --pretty=format:"%H"', timeout=300)
        run_in_shell(CWD)

        #print(commit_history.stdout.decode(errors='ignore').split("\n"))
        
        try:
            new_contents, old_contents, returncode, stderr = get_file_contents(commit_history[2], repo, cwd=random_dir)
        except Exception as e:
            #print("ERROR", commit_id, old_file, new_file, repo, str(random_dir), e)
            # Break in case of many repos that all lead us nowhere
            if i > 10:
                break
            continue
        finally:
            run_in_shell("rm -rf " + random_dir) # clean up again
        ex["new_contents"] = new_contents
        ex["old_contents"] = old_contents
        ex["returncode"] = returncode
        ex["stderr"] = stderr

        print(f'new_contents: {new_contents}')
        print(f'old_contents: {old_contents}')
        print(f'returncode: {returncode}')
        print(f'stderr: {stderr}')
        return ex
    # If no repo worked
    ex["new_contents"] = ""
    ex["old_contents"] = ""
    ex["returncode"] = returncode
    ex["stderr"] = stderr


    return ex

def get_diff_multi_threaded_processed(batch):
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        # Convert dict of lists to list of dicts then map to threads
        results = list(executor.map(get_diff, [dict(zip(batch,t)) for t in zip(*batch.values())]))
        # Convert list of dicts to dict of lists
        return {k: [dic[k] for dic in results] for k in results[0]}

if __name__ == "__main__":
    # git clone https://huggingface.co/datasets/bigcode/commitpackmeta
    #ds = datasets.load_dataset("./commitpackmeta", use_auth_token=True)["train"]
    from datasets import load_dataset
    #ds = datasets.load_dataset("/Users/lambert/Downloads/method2test.tar.gz.partaa", use_auth_token=False) #["train"]

    


    ### OPTIONAL FILTERING ###
    #"""
    java = [".java"]
    javascript = [
        "._js",
        ".bones",
        ".es6",
        ".jake",
        ".jsb",
        ".jscad",
        ".jsfl",
        ".jsm",
        ".jss",
        ".njs",
        ".pac",
        ".sjs",
        ".ssjs",
        ".xsjs",
        ".xsjslib"
    ]
    python = [
        ".py",
        ".bzl",
        ".gyp",
        ".lmi",
        ".pyde",
        ".pyp",
        ".pyt",
        ".pyw",
        ".tac",
        ".wsgi",
        ".xpy"
    ]

    import json
    with open("dataset/commitpack/programming_languages.json", "r") as f:
        extensions = json.load(f)
    suffices = tuple([suffix for suffices in extensions.values() for suffix in suffices])
    # def filter_extension(ex):
    #     return ex["new_file"].endswith(suffices)

    # def filter_extension_python(ex):
    #     return ex["new_file"].endswith(python)

    # def filter_update(ex):
    #     return ex["message"] != "Update " + ex["old_file"]

    # filter_msg = ["initial commit", "please\n", "please", "lalala"]

    # def filter_misc(ex):
    #     return ex["message"] not in filter_msg

    # # Removes ~10M
    # ds = ds.filter(filter_extension, num_proc=NUM_PROC)
    # print("After Extension filter", len(ds))
    # # Removes ~1M
    # ds = ds.filter(filter_update, num_proc=NUM_PROC)
    # print("After Update filter", len(ds))
    # #ds = ds.filter(filter_extension_python, num_proc=NUM_PROC)
    # #print("After Python filter", len(ds))
    # ds = ds.filter(filter_misc, num_proc=NUM_PROC)
    # print("After Misc filter", len(ds))
    # #ds = ds.select(range(DEBUG_SIZE))
    START = 0 # Modify for each instance (0 - 7)
    samples_per_instance =   1  #   64 * 64 * 64 * 32 # 8_388_608
    select_start = START * samples_per_instance
    select_end = START * samples_per_instance + samples_per_instance
    # ds = ds.select(range(select_start, select_end))
    # print(f"Going from {select_start} till {select_end}")

    #"""
    ### END FILTERING ###

    

    ### ALTERNATIVELY LOAD EXISTING SPLIT ###
    
    path ="/Users/lambert/projects/Aster/zircon-finetuning-data/method2test-raw-data-parts/method2test/181194375/181194375_2.json"  # "github-commits-diff/data/diffs_50331648_58720256.jsonl"
    ds = datasets.load_dataset("json", data_files=path)
    #sub_ds = ds.filter(lambda x: x['stderr'].startswith("fatal: unable to acces"))
    #skipped_ds = ds.filter(lambda x: not(x['stderr'].startswith("fatal")))
    # print(dir(ds))
    # print((ds.keys()))
    print(ds["train"]['repository'][0]['url'])
    
    # datasets.concatenate_datasets((
    #     skipped_ds,
    #     sub_ds.map(get_diff_multi_threaded_processed, num_proc=NUM_PROC, batch_size=NUM_THREADS, batched=True),
    # )).to_json(path.replace(".", "_new."), num_proc=NUM_PROC)

    
    ### END LOAD EXISTING ###

    def run_multi_processing_threading():
        ds.map(get_diff_multi_threaded_processed, num_proc=NUM_PROC, batch_size=NUM_THREADS, batched=True).to_json(f"diffs_{select_start}_{select_end}.jsonl")
        print(ds.shape)
        print("Done")

    # Benchmarking
    #NUM_TRIALS = 1
    #print(f"Timing multithreading + multiprocessing using {NUM_THREADS} threads and {NUM_PROC} processes")
    #time = timeit.timeit(stmt=run_multi_processing_threading, number=NUM_TRIALS)
    #print("Time:", time)
    #with open("mpt.txt", "w") as f:
    #    f.write(str(time))

    # Running
    run_multi_processing_threading()