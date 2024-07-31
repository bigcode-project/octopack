from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import os
import random
import subprocess
import timeit
import json
from pathlib import Path

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
  
    completed = run_in_shell("git fetch --depth 2 origin " + commit, cwd=cwd)
     # If it requires authentication
    if completed.returncode != 0:
        #print("ERRORC1", completed)
        return ("", "", completed.returncode, completed.stderr.decode(errors='ignore'))
    # Optionally do git diff at the same time (Saving code needs to be added)
    # git_diff = run_in_shell(f"git diff {commit}^ {commit}", cwd=cwd).stdout.decode(errors='ignore')
    completed = run_in_shell("git checkout FETCH_HEAD -- " + new_file, cwd=cwd)
    new_contents = run_in_shell("cat " + new_file, cwd=cwd).stdout.decode(errors='ignore')
    completed = run_in_shell("git checkout FETCH_HEAD^ -- " + old_file, cwd=cwd)
    # If there's only a new file, but no old file
    if completed.returncode != 0:
        return (new_contents, "", completed.returncode, completed.stderr.decode(errors='ignore'))
    old_contents = run_in_shell("cat " + old_file, cwd=cwd).stdout.decode(errors='ignore')
    return (new_contents, old_contents, completed.returncode, completed.stderr.decode(errors='ignore'))

def get_commit_diff(ex):
   
    repo = ex["url"]
    print(f'repos----------: {repo}')
    # Create a random directory to store the repo
    random_dir = CWD + "/" + str(random.randint(0, 1000000))
    # Can take very long when running many processes
    run_in_shell("mkdir " + random_dir, timeout=300)

    with open('dataset/methods2test/methods2test_commits.jsonl', 'a') as file:  # Open the file in append mode
        try:
            print(f'processing {repo}..........................................................')
            completed = run_in_shell("git init", cwd=random_dir)
            completed = run_in_shell("git remote add origin " + repo, cwd=random_dir)
            completed = run_in_shell("git clone " + repo, cwd=random_dir)

            #get all commits hash
            completed = run_in_shell("git ls-remote " + repo, cwd=random_dir + "/" + repo.split("/")[-1])
            commits = completed.stdout.decode(errors='ignore').split("\n")
            commits = [c.split("\t")[0] for c in commits]

            if completed.returncode != 0:
                print(f'ERRORC2: {completed}')
            if len(commits) > 50:
                for i , commit_id in enumerate(commits[0:30]):
                    if i == len(commits[0:30]) - 1:
                        ex['is_last_commit'] = True 
                    ex['commit'] = commit_id
                    file.write(json.dumps(ex) + "\n")
            
        except Exception as e:
            print(f'ERROR: {e}')
        run_in_shell("rm -rf " + random_dir) # clean up again
    return ex


def get_diff(ex):
    
    repo = ex["url"]
    # Can take very long when running many processes
    repo_name = repo.split("/")[-1]
    repo_exists = False
    working_dir = ""
    for path in Path(CWD).rglob('*'):
        if path.is_dir() and path.name == repo_name:
            print(f'repo exists: {path}')
            repo_exists = True
            working_dir = path
            break
    with open('dataset/methods2test/methods2test.jsonl', 'a') as methods2test_file:  # Open the file in append mode
        try:
            # Create a random directory to store the repo
            #check if the ramdom directory exists
            
            if not repo_exists:
                random_dir = CWD + "/" + str(random.randint(0, 1000000))
                run_in_shell("mkdir " + random_dir, timeout=300)
                completed = run_in_shell("git init", cwd=random_dir)
                completed = run_in_shell("git remote add origin " + repo, cwd=random_dir)
                completed = run_in_shell("git clone " + repo, cwd=random_dir)
                working_dir = random_dir + "/" + repo.split("/")[-1]
        
            
            commit_id = ex['commit']
            #get files modified in this commit
            print(f'getting all files at ' + str(working_dir) + "/" + repo.split("/")[-1] +"for commit " + commit_id + "...\n")
            completed = run_in_shell("git diff-tree --no-commit-id --name-only -r " + f'{commit_id}', cwd=working_dir)
            if completed.returncode != 0:
                print(f'ERRORC3: {completed}')
            
            files = completed.stdout.decode(errors='ignore').split("\n") 
            # show all files
            print(f'files: {files}')
            if len(files) < 25:
                for file in files:
                    if file.endswith(".java"):
                        #Assuminng that file names has not changed between commits
                        new_file = file
                        old_file = file
                        print(f'new_file: {new_file} --> old_file: {old_file}')
                        print(f'getting file contents for {new_file} at ' + str(working_dir) + "for commit " + commit_id + "...\n")
                        new_contents, old_contents ,_ ,_ = get_file_contents(commit_id, old_file, new_file, repo, cwd=working_dir)

                        #get commit message
                        completed = run_in_shell("git show --format=%B -s " + commit_id, cwd=working_dir)
                        message = completed.stdout.decode(errors='ignore')
                        print(f'message: {message} \n')
                        ex["new_contents"] = new_contents
                        ex["old_contents"] = old_contents
                        ex["new_file"] = new_file
                        ex["old_file"] = old_file
                        ex["commit"] =  commit_id
                        ex["message"] = message
                        methods2test_file.write(json.dumps(ex) + "\n")

        except Exception as e:
            #print("ERROR", commit_id, old_file, new_file, repo, str(random_dir), e)
            # Break in case of many repos that all lead us nowhere
            print(f'ERROR: {e}')
            print(f'Working dir causing this error: {working_dir}')

        
        finally:
            if ex['is_last_commit'] == True:
                print(f'cleaning up {working_dir}')
                run_in_shell("rm -rf " + str(Path(working_dir)))  # clean up again
        return ex
      

def get_commits_multi_threaded_processed(batch):
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        # Convert dict of lists to list of dicts then map to threads
        results = list(executor.map(get_commit_diff, [dict(zip(batch,t)) for t in zip(*batch.values())]))
        # Convert list of dicts to dict of lists
        return {k: [dic[k] for dic in results] for k in results[0]}

def get_diff_multi_threaded_processed(batch):
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        # Convert dict of lists to list of dicts then map to threads
        results = list(executor.map(get_diff, [dict(zip(batch,t)) for t in zip(*batch.values())]))
        # Convert list of dicts to dict of lists
        return {k: [dic[k] for dic in results] for k in results[0]}

if __name__ == "__main__":
    methods2test_path = "dataset/methods2test/repos.jsonl"
    ds = datasets.load_dataset("json", data_files=methods2test_path, num_proc=NUM_PROC)["train"]
    
    # Cleanup cache files
    ds.cleanup_cache_files()
    
    # set all "test_cases" from the dataset to None,    
    ds = ds.map(lambda x: {"test_cases": {}})
    ds = ds.map(lambda x: ({"commit": "commit_id", "old_file": " ", "new_file": " ", "old_contents": "", "new_contents": " ", "subject": "", "message": "", "lang": "Java", "license": "", "repos": "","is_last_commit": False}))
    # # save the dataset
    # ds.to_json("dataset/methods2test/repos_testcases_none.jsonl", num_proc=NUM_PROC)

    START = 15 # Modify for each instance (0 - 7)
    samples_per_instance =  1 * 4 * 5 * 1    # 1 * 4 * 64 * 34 # 8_388_608
    select_start = START * samples_per_instance
    select_end = START * samples_per_instance + samples_per_instance
    ds = ds.select(range(select_start, select_end))
    print(f"Going from {select_start} till {select_end}")
    
    
    # Build commits
    def build_commit_diff():
        ds.map(get_commits_multi_threaded_processed, num_proc=NUM_PROC, batch_size=NUM_THREADS, batched=True)
    build_commit_diff()
    # Load ds after commits are processed
    ds  = datasets.load_dataset("json", data_files="dataset/methods2test/methods2test_commits.jsonl", num_proc=NUM_PROC)["train"]
    
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