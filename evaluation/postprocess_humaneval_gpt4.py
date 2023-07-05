import json
import sys
#from datasets import load_dataset

#ds = load_dataset("humaneval-x-bugs", "python", split="test")

process = True
LANGUAGE = "python"

path = sys.argv[1] # e.g. completions_python.jsonl

with open(path, "r") as f:
  c = [json.loads(l) for l in f.readlines()]

with open(path.replace("jsonl", "json"), "w") as f:
    if process is False:
      if isinstance(c[0]["generation"], str):
        json.dump(
            [[x["prompt"] + x["generation"]] for x in c], f
        )
      else:
        json.dump(
            [[x["prompt"] + z for z in x["generation"]] for x in c], f
        )
    else:
      # From https://github.com/nlpxucan/WizardLM/blob/main/WizardCoder/src/process_humaneval.py
      a = 0
      output = []
      for samples in c:
        sub_output = []
        for completion in samples["raw_generation"]:
            completion = completion.replace("\r", "")       
            if '```' + LANGUAGE in completion: 
                def_line = completion.index('```' + LANGUAGE)
                completion = completion[def_line:].strip()
                completion = completion.replace('```' + LANGUAGE, '')
                # print(completion)
                try:
                    next_line = completion.index('```')
                    completion = completion[:next_line].strip()
                except:
                    a += 1
                    print(completion)
                    print("================\n")
                # print(completion)
            
            if LANGUAGE == "python":            
              if "__name__ == \"__main__\"" in completion:
                  next_line = completion.index('if __name__ == "__main__":')
                  completion = completion[:next_line].strip()
                  # print(completion)
            elif LANGUAGE == "cpp":
              if "int main()" in completion:
                  next_line = completion.index('int main()')
                  completion = completion[:next_line].strip()
                  # print(completion)
            elif LANGUAGE == "java":
              # Add class Solution before signature
              if "public class Main {\n" in completion:
                  completion = completion.replace("public class Main {\n", "class Solution {\n")
                  completion = completion.replace("public static void main(String[] args)", "")
              if "class Solution" not in completion:
                  for line in completion.split("\n"):
                    if samples["entry_point"] in line:
                      completion = completion.replace(line, "class Solution {\n" + line)
                      completion += "\n}"
                      break
              # Add import statements
              for line in samples["declaration"].split("\n"):
                  if "import" in line:
                      completion = line + "\n" + completion
            elif LANGUAGE == "go":
               # Remove package main
               completion = completion.replace("package main", "")
               
              
            if "# Example usage" in completion:
                # print(completion)
                next_line = completion.index('# Example usage')
                completion = completion[:next_line].strip()
            
            sub_output.append(completion)
        output.append(sub_output)
      json.dump(output, f)