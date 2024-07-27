
import datasets

NUM_PROC = 4
git_prefix = "https://github.com/"

commitpackft_java_jsonl_path_from_ibmcloud = "dataset/commitpackft_from_ibmcloud/bigcode_commitpackft_java.jsonl"
methods2test_path = "dataset/methods2test/repos.jsonl"

methods2test_ds = datasets.load_dataset("json", data_files=methods2test_path, num_proc=NUM_PROC)["train"]
ds_ibmcloud = datasets.load_dataset("json", data_files=commitpackft_java_jsonl_path_from_ibmcloud, num_proc=NUM_PROC)["train"]

commitpackft_repos = list(map(lambda x: x["repos"], ds_ibmcloud))
methods2test_repos = list(map(lambda x: x["url"], methods2test_ds))
commitpackft_repos_list = list(map(lambda x: x.split(","), commitpackft_repos))

match_repos = set()
for repo in  commitpackft_repos_list:
    for repo_name in list(set(repo)):
        if f'{git_prefix}{repo_name}' in methods2test_repos:
            print(f'{git_prefix}{repo_name} is in methods2test_repos')
            match_repos.add(f'{git_prefix}{repo_name}')
        else:
            continue

print(f'totat match repos: {len(match_repos)}')
print(f'we need to scrape {len(methods2test_ds) - len(match_repos)} repos')
