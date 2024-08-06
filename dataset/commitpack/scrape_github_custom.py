from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import os
import logging
import random
import subprocess
import timeit
import json
from pathlib import Path
import time
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

MAX_COMMITS = 20
MAX_FILES_CHANGED = 1

# DEBUG_SIZE = 1024
CWD = os.getcwd()
repos_success =  0 #Successfully cloned
repos_failed  =   0 #Failed to clone
total_commits =  0 #Total number of commits

# file path to store the results
commits_file_path = "dataset/methods2test/commits.jsonl"

# file path to store the results
diffs_file_path = "dataset/methods2test/data/java/methods2test.jsonl"

def save_file(file_path, content , file_name):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path+file_name, 'w') as file:
        file.write(content)

# Shell utils
def run_in_shell(cmd: str, cwd=None, timeout=60):
    return subprocess.run([cmd], capture_output=True, shell=True, cwd=cwd, timeout=timeout)

def get_file_contents(repo_name, commit, old_file, new_file,  repo, random_dir, cwd=None):
    
    completed = run_in_shell("git init", cwd=random_dir)
    completed = run_in_shell("git remote add origin " + repo, cwd=random_dir)
    completed = run_in_shell("git fetch --depth 2 origin " + commit, cwd=cwd)
     # If it requires authentication
    if completed.returncode != 0:
        #print("ERRORC1", completed)
        return ("", "", completed.returncode, completed.stderr.decode(errors='ignore'))
    # Optionally do git diff at the same time (Saving code needs to be added)
    git_diff = run_in_shell(f"git diff {commit}^ {commit}" + " --name-only", cwd=cwd).stdout.decode(errors='ignore')
  
    completed = run_in_shell("git checkout FETCH_HEAD -- " + new_file, cwd=cwd)
    new_contents = run_in_shell("cat " + new_file, cwd=cwd).stdout.decode(errors='ignore')
    new_file_name  = "new_" + new_file.split("/")[-1]+ ".java"
    

    completed = run_in_shell("git checkout FETCH_HEAD^ -- " + old_file, cwd=cwd)
    # If there's only a new file, but no old file
    if completed.returncode != 0:
        #print("ERRORC2", completed)
        return (new_contents, "", completed.returncode, completed.stderr.decode(errors='ignore'))
    old_contents = run_in_shell("cat " + old_file, cwd=cwd).stdout.decode(errors='ignore')
    old_file_name  = "old_" + old_file.split("/")[-1]+ ".java"

    #if len(git_diff.split("\n")) <=2:
    # save_file(str(random_dir) + "/" + repo_name + "/", new_contents, new_file_name)
    # save_file(str(random_dir) + "/" + repo_name + "/", old_contents, old_file_name)
    # patch = run_in_shell("git diff "+ str(random_dir) + "/" + repo_name + "/" + new_file_name + " " + str(random_dir) + "/" + repo_name + "/" + old_file_name + ">" + str(random_dir) + "/" + repo_name + "/" + "diff.patch", cwd=cwd)
    patch = run_in_shell(f"git diff  {commit}^   {commit}  --  {new_file}  >  {str(random_dir)}/{repo_name}/diff.patch", cwd=cwd)
    #logging.info(f'patch: {patch}')
    logging.info(f'patch contents: {patch.stdout.decode(errors="ignore")}')
    return (new_contents, old_contents, completed.returncode, completed.stderr.decode(errors='ignore'))
   

def get_commit_diff(ex):
   
    repo = ex["url"]
    logging.info(f'repos----------: {repo}')
    # Create a random directory to store the repo
    random_dir = CWD + "/" + str(random.randint(0, 1000000))
    # Can take very long when running many processes
    run_in_shell("mkdir " + random_dir, timeout=300)

    with open(f'{commits_file_path}', 'a') as file:  # Open the file in append mode
        try:
            logging.info(f'processing {repo}..........................................................')
            completed = run_in_shell("git init", cwd=random_dir)
            completed = run_in_shell("git remote add origin " + repo, cwd=random_dir)
            completed = run_in_shell("git clone " + repo, cwd=random_dir)
 
            if completed.returncode != 0:
                logging.error(f'ERROR: Could not clone {repo}')
                logging.info(f'removing {random_dir}')
                run_in_shell("rm -rf " + random_dir + "/" + repo.split("/")[-1])
            #get all commits hash
            logging.info(f'getting all commits at ' + str(random_dir) + "...\n")
            completed = run_in_shell("git ls-remote " + repo, cwd=random_dir + "/" + repo.split("/")[-1])
            commits = completed.stdout.decode(errors='ignore').split("\n")
            commits = [c.split("\t")[0] for c in commits]

            if completed.returncode != 0:
                print(f'ERRORC2: {completed}')
            logging.info(f'checking if commits are less than 50')
            last_commit = False
            if len (commits) >  20:
                for i , commit_id in enumerate(commits[0:10]):
                    if i == len(commits[0:10]) - 1:
                        ex['is_last_commit'] = True
                        ex['commit'] = commit_id
                        last_commit = True
                        file.write(json.dumps(ex) + "\n")
                        logging.info(f'last commit reached:  i is: {i}\n')
                        break
                    else:
                        logging.info(f'last commit not reached')
                        ex['commit'] = commit_id
                        file.write(json.dumps(ex) + "\n")
             
            if last_commit:
                 logging.info(f'last commit reached: Removing {random_dir}...')
                 run_in_shell("rm -rf " + str(Path(random_dir)))  # clean up again
            if len(commits) < 20 :
                logging.info(f'Repo has less than 20 commits: Removing {random_dir}...')
                run_in_shell("rm -rf " + str(Path(random_dir)))  # clean up again

        except Exception as e:
            logging.error(f'ERROR: {e} : removing {random_dir} ...')
            run_in_shell("rm -rf " + str(Path(random_dir)))
    return ex


def get_diff(ex):
    
    repo = ex["url"]
    # Can take very long when running many processes
    repo_name = repo.split("/")[-1]
    repo_exists = False
    working_dir = ""

    for path in Path(CWD).rglob('*'): # get all the repos
        if path.is_dir() and path.name == repo_name:
            print(f'repo exists: {path}')
            print(f'path name: {path.name}')
            repo_exists = True
            random_dir = path.parent
            working_dir = path
            break
   
    with open('dataset/methods2test/methods2test.jsonl', 'a') as methods2test_file:  # Open the file in append mode

        if not repo_exists:
            random_dir = CWD + "/" + str(random.randint(0, 1000000))
            run_in_shell("mkdir " + random_dir, timeout=300)
            completed = run_in_shell("git init", cwd=random_dir)
            completed = run_in_shell("git remote add origin " + repo, cwd=random_dir)
            completed = run_in_shell("git clone " + repo, cwd=random_dir)
            working_dir = random_dir + "/" + repo.split("/")[-1]
        commit_id = ex['commit']

       
        # Create a random directory to store the repo
        #check if the ramdom directory exists
        logging.info(f'Getting all files at ' + str(working_dir)  + "for commit " + commit_id + "...\n")
        completed = run_in_shell("git diff-tree --no-commit-id --name-only -r " + f'{commit_id}', cwd=working_dir)
        if completed.returncode != 0:
            print(f'ERRORC2: {completed}')
            print(f'no files found for commit {commit_id} , error: {completed.stderr}')

        else:
            files = completed.stdout.decode(errors='ignore').split("\n")
            files=[f for f in files if f.endswith(".java")]
            if len(files) == 1:
                logging.info(f'Single file found for commit {commit_id} , getting diff...')
                for file in files:
                    print(f'file: {file} \n')

                    if not os.path.exists(os.path.join(working_dir, file)):
                        logging.error(f'ERROR: Could not find file {file} in repo {repo}')
                        continue

                    new_file = file
                    old_file = file
                    new_contents, old_contents ,_ , _ =  get_file_contents(repo_name,commit_id, old_file, new_file, repo, random_dir,  working_dir)
                    #get commit message
                    completed = run_in_shell("git show --format=%B -s " + commit_id, cwd=working_dir)
                    message = completed.stdout.decode(errors='ignore')
                    logging.info(f'message: {message} \n')
                    ex["new_contents"] = new_contents
                    ex["old_contents"] = old_contents
                    ex["new_file"] = new_file
                    ex["old_file"] = old_file
                    ex["commit"] =  commit_id
                    ex["message"] = message
                    methods2test_file.write(json.dumps(ex) + "\n")
                    logging.info(f'ex  written  to file {methods2test_file}')
        if ex['is_last_commit'] == True:
            logging.info(f'last commit reached: Removing {working_dir}')
            logging.info(f'cleaning up {random_dir}')
            run_in_shell("rm -rf " + str(Path(random_dir)))  # clean up again
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


   
    # Add basic logging to the root logger , and save it to a log file 
    logging.basicConfig(filename='runs.log', level=logging.INFO)

    methods2test_path = "dataset/methods2test/repos.jsonl"
    ds = datasets.load_dataset("json", data_files=methods2test_path, num_proc=NUM_PROC)["train"]
     # Cleanup cache files
    ds.cleanup_cache_files()
    
   
    
    # set all "test_cases" from the dataset to None,    
    ds = ds.map(lambda x: {"test_cases": {}})
    ds = ds.map(lambda x: ({"commit": "commit_id", "old_file": " ", "new_file": " ", "old_contents": "", "new_contents": " ", "subject": "", "message": "", "lang": "Java", "license": "", "repos": "","is_last_commit": False}))
    # # save the dataset
    # ds.to_json("dataset/methods2test/repos_testcases_none.jsonl", num_proc=NUM_PROC)
    

    START = 12 # Modify for each instance (0 - 7)
    samples_per_instance =  1 * 4 * 4 * 1   # 1 * 4 * 64 * 34 # 8_388_608
    select_start = START * samples_per_instance
    select_end = START * samples_per_instance + samples_per_instance
    ds = ds.select(range(select_start, select_end))
    logging.info(f"Going from {select_start} till {select_end}")
    
    
    # Build commits
    logging.info("Building commits...")
    start = time.time()
    def build_commit_diff():
        ds.map(get_commits_multi_threaded_processed, num_proc=NUM_PROC, batch_size=NUM_THREADS, batched=True)
    build_commit_diff()

    #compute time in hours
    hours = int((time.time() - start) / 3600)
    minutes = int((time.time() - start) / 60) - hours * 60
    seconds = time.time() - start - hours * 3600 - minutes * 60
    logging.info(f"Time taken to build commits: {hours}h {minutes}m {seconds}s")


    # # Load ds after commits are processed
    ds  = datasets.load_dataset("json", data_files=commits_file_path, num_proc=NUM_PROC)["train"]
    
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
    start = time.time()
    run_multi_processing_threading()
     #compute time in hours
    hours = int((time.time() - start) / 3600)
    minutes = int((time.time() - start) / 60) - hours * 60
    seconds = time.time() - start - hours * 3600 - minutes * 60
    logging.info(f"Time taken to retrieve diffs: {hours}h {minutes}m {seconds}s")

  