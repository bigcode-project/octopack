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



def get_code_block( file_path: str, start_line: int , end_line:int ) -> dict:
    """_summary_

    Args:
        diff_patch_file (str): _description_

    Returns:
        dict: _description_
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    
    logging.info(f'retrieving code block from {file_path} from line {start_line} to {   start_line+ end_line}')
    code_block = ""
    for i , code in enumerate(lines):
        if i+1  ==  start_line + end_line:
            break
        elif i+1  >= start_line and i+1 < start_line + end_line:
            code_block += code
        else:
            continue
        
    return code_block



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
    file_path = str(cwd) + "/" + new_file
 
    completed = run_in_shell("git checkout FETCH_HEAD -- " + new_file, cwd=cwd)
    new_contents = run_in_shell("cat " + new_file, cwd=cwd).stdout.decode(errors='ignore')
   
    completed = run_in_shell("git checkout FETCH_HEAD^ -- " + old_file, cwd=cwd)
    # If there's only a new file, but no old file
    if completed.returncode != 0:
        #print("ERRORC2", completed)
        return (new_contents, "", completed.returncode, completed.stderr.decode(errors='ignore'))
    old_contents = run_in_shell("cat " + old_file, cwd=cwd).stdout.decode(errors='ignore')
   
    patch = run_in_shell(f"git diff  {commit}^   {commit}  --  {new_file} | grep -o '^@@.*@@'", cwd=cwd) #>  {str(random_dir)}/{repo_name}/diff.patch
    #logging.info(f'patch: {patch}')
    if patch.returncode != 0:
        logging.error(f'ERROR: Could not  get patch for {new_file}')
        return ("", "", patch.returncode, patch.stderr.decode(errors='ignore'))
    
    lines =patch.stdout.decode(errors="ignore")
    lines = lines.replace("@@",'').split("\n")
    line_pairs = []
    for line in lines:
        if line != "":
            line_pairs.append(line.strip())

    
    diff = defaultdict(list)
    
    #pairs = ['-3,9 +3,11', '-15,6 +17,7', '-132,12 +135,13', '-255,12 +259,11', '-271,30 +274,53']
    for idx, pair in enumerate(line_pairs):
        line_num = pair.split(" ")

        old_line = line_num[0].replace("-","") 
        completed = run_in_shell("git checkout FETCH_HEAD^ -- " + old_file, cwd=cwd)
        file_path =  str(cwd) + "/" + old_file
        # logging.info(f'old file path: {file_path}')
        # logging.info(f'get old line numbers: {old_line}')

        old_line_start = old_line.split(",")[0]
        offset = old_line.split(",")[1]
        # logging.info(f'old line start: {int(old_line_start)}')
        # logging.info(f'old line end: {int(old_line_start) + int(offset)}')

        old_contents_line= get_code_block(file_path, int(old_line_start), int(offset))
        logging.info(f'old file block: {old_contents_line}\n')

        new_line = line_num[1].replace("+","")   
        completed = run_in_shell("git checkout FETCH_HEAD -- " + new_file, cwd=cwd)

   
        new_line_start = new_line.split(",")[0]
        offset = new_line.split(",")[1]
        new_contents_line = get_code_block(file_path, int(new_line_start), int(offset))
        logging.info(f'new file block: {new_contents_line}\n')

        diff['diff_'+str(idx)] = [old_contents_line , new_contents_line]

    patch = run_in_shell(f'git diff {commit}^ {commit}' , cwd=cwd) #>  {str(random_dir)}/{repo_name}/diff.patch
    logging.info(f'diff dict: {diff}')
    logging.info(f'patch: {patch.stdout.decode(errors="ignore")}')
    logging.info(f'current commit: {commit}, current repo: {repo}')
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
    # logging.info("Building commits...")
    # start = time.time()
    # def build_commit_diff():
    #     ds.map(get_commits_multi_threaded_processed, num_proc=NUM_PROC, batch_size=NUM_THREADS, batched=True)
    # build_commit_diff()

    # #compute time in hours
    # hours = int((time.time() - start) / 3600)
    # minutes = int((time.time() - start) / 60) - hours * 60
    # seconds = time.time() - start - hours * 3600 - minutes * 60
    # logging.info(f"Time taken to build commits: {hours}h {minutes}m {seconds}s")


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

  