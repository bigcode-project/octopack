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

def get_file_contents(commit, old_file, new_file, repo, cwd=None):
    completed = run_in_shell("git fetch --depth 2 origin " + commit, cwd=cwd) # fetch curerent commit up to its parent (depth 2)
     # If it requires authentication
    if completed.returncode != 0:
        #print("ERRORC1", completed)
        return ("", "", completed.returncode, completed.stderr.decode(errors='ignore'))
    # Optionally do git diff at the same time (Saving code needs to be added)
    # git_diff = run_in_shell(f"git diff {commit}^ {commit}", cwd=cwd).stdout.decode(errors='ignore')
    completed = run_in_shell("git checkout FETCH_HEAD -- " + new_file, cwd=cwd) #pointer to the current commit
    new_contents = run_in_shell("cat " + new_file, cwd=cwd).stdout.decode(errors='ignore')
    completed = run_in_shell("git checkout FETCH_HEAD^ -- " + old_file, cwd=cwd)  #parent of the commit
    # If there's only a new file, but no old file
    if completed.returncode != 0:
        #print("ERRORC2", completed)
        return (new_contents, "", completed.returncode, completed.stderr.decode(errors='ignore'))
    old_contents = run_in_shell("cat " + old_file, cwd=cwd).stdout.decode(errors='ignore')
    return (new_contents, old_contents, completed.returncode, completed.stderr.decode(errors='ignore'))

def get_diff(ex):
    repos = list(set(ex["url"].split(",")))
   
    for i, repo in enumerate(repos):
        # Create a random directory to store the repo
        random_dir = CWD + "/" + str(random.randint(0, 1000000))
        # Can take very long when running many processes
        run_in_shell("mkdir " + random_dir, timeout=300)
        try:
            print(f'repo: {repo}')
            completed = run_in_shell("git init", cwd=random_dir)
            completed = run_in_shell("git remote add origin " + repo, cwd=random_dir)
            completed = run_in_shell("git clone " + repo, cwd=random_dir)

            #get all commits hash
            completed = run_in_shell("git ls-remote " + repo, cwd=random_dir + "/" + repo.split("/")[-1])
            commits = completed.stdout.decode(errors='ignore').split("\n")
            commits = [c.split("\t")[0] for c in commits]
            # Get latest commit hash
            commit_id = commits[0]
            print(f'commit_id: {commit_id}')
            if completed.returncode != 0:
                print(f'ERRORC2: {completed}')
                continue
            #get files modified in this commit
            completed = run_in_shell("git diff-tree --no-commit-id --name-only -r " + f'{commit_id}', cwd=random_dir + "/" + repo.split("/")[-1])
            if completed.returncode != 0:
                print(f'ERRORC3: {completed}')
                continue
            files = completed.stdout.decode(errors='ignore').split("\n") # list of files
            # show all files
            print(f'files: {files}')
            #Assuminng that file names has not changed between commits
            old_file = files[0]
            new_file = old_file
            print(f'new_file: {new_file} --> old_file: {old_file}')
            new_contents, old_contents, returncode, stderr = get_file_contents(commit_id, old_file, new_file, repo, cwd=random_dir)
        
        except Exception as e:
            #print("ERROR", commit_id, old_file, new_file, repo, str(random_dir), e)
            # Break in case of many repos that all lead us nowhere
            if i > 10:
                break
            continue
        finally:
            run_in_shell("rm -rf " + random_dir) # clean up again
        # ex["new_contents"] = new_contents
        # ex["old_contents"] = old_contents
        # ex["returncode"] = returncode
        # ex["stderr"] = stderr
        return ex
    # If no repo worked
    # ex["new_contents"] = ""
    # ex["old_contents"] = ""
    # ex["returncode"] = returncode
    # ex["stderr"] = stderr
    return ex

def get_diff_multi_threaded_processed(batch):
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        # Convert dict of lists to list of dicts then map to threads
        results = list(executor.map(get_diff, [dict(zip(batch,t)) for t in zip(*batch.values())]))
        # Convert list of dicts to dict of lists
        return {k: [dic[k] for dic in results] for k in results[0]}

if __name__ == "__main__":
    # git clone https://huggingface.co/datasets/bigcode/commitpackmeta
    # ds = datasets.load_dataset("./commitpackmeta", use_auth_token=True)["train"]
    methods2test_path = "dataset/methods2test/repos.jsonl"
    ds = datasets.load_dataset("json", data_files=methods2test_path, num_proc=NUM_PROC)["train"]

    # set all "test_cases" from the dataset to None,    
    ds = ds.map(lambda x: {"test_cases": {}})
    # add the following    {"commit": "commit_id", "old_file": " ", "new_file": " ", "old_contents": "", "new_contents": " ", "subject": "", "message": "R", "lang": "Java", "license": "", "repos": ""}    
    ds = ds.map(lambda x: ({"commit": "commit_id", "old_file": " ", "new_file": " ", "old_contents": "", "new_contents": " ", "subject": "", "message": "R", "lang": "Java", "license": "", "repos": ""}))

    # save the dataset
    ds.to_json("dataset/methods2test/repos_testcases_none.jsonl", num_proc=NUM_PROC)


    exit()

    START = 8 # Modify for each instance (0 - 7)
    samples_per_instance =  1 * 4 * 5 * 1    # 1 * 4 * 64 * 34 # 8_388_608
    select_start = START * samples_per_instance
    select_end = START * samples_per_instance + samples_per_instance
    ds = ds.select(range(select_start, select_end))
    print(f"Going from {select_start} till {select_end}")

    ### ALTERNATIVELY LOAD EXISTING SPLIT ###
    """
    path = "github-commits-diff/data/diffs_50331648_58720256.jsonl"
    ds = datasets.load_dataset("json", data_files=path)
    sub_ds = ds.filter(lambda x: x['stderr'].startswith("fatal: unable to acces"))
    skipped_ds = ds.filter(lambda x: not(x['stderr'].startswith("fatal")))
    
    datasets.concatenate_datasets((
        skipped_ds,
        sub_ds.map(get_diff_multi_threaded_processed, num_proc=NUM_PROC, batch_size=NUM_THREADS, batched=True),
    )).to_json(path.replace(".", "_new."), num_proc=NUM_PROC)
    exit()
    """
    ### END LOAD EXISTING ###

    def run_multi_processing_threading():
        ds.map(get_diff_multi_threaded_processed, num_proc=NUM_PROC, batch_size=NUM_THREADS, batched=True).to_json(f"diffs_{select_start}_{select_end}.jsonl", num_proc=NUM_PROC)

    # Benchmarking
    #NUM_TRIALS = 1
    #print(f"Timing multithreading + multiprocessing using {NUM_THREADS} threads and {NUM_PROC} processes")
    #time = timeit.timeit(stmt=run_multi_processing_threading, number=NUM_TRIALS)
    #print("Time:", time)
    #with open("mpt.txt", "w") as f:
    #    f.write(str(time))

    # Running
    run_multi_processing_threading()