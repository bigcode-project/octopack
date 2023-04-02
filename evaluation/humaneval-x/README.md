---
annotations_creators: []
language_creators:
- crowdsourced
- expert-generated
language:
- code
license:
- apache-2.0
multilinguality:
- multilingual
size_categories:
- unknown
source_datasets: []
task_categories:
- text-generation
task_ids:
- language-modeling
pretty_name: HumanEval-X
---


### Modifications (@Muennighoff):

- JS Line 33: Added `testfindZero()\n`, as the test was never called
- JS Line 113: Changed the scope of the brackets in the `test` to actually test the solution; Previously all tests pass reagardless of the solution; Also rewrote the solution, which was incorrect; Likely the solution was written for the incorrect tests, which passed regardless of the solution
- JS Line 120: Added `testMatchParens()\n`, as the test was never called
- JS Line 154: Added `testDoubleTheDifference()\n`, as the test was never called
- Rust Line 33: Removed the comments that were deactivating the tests (Tests were commented out with `/* */` (See https://github.com/THUDM/CodeGeeX/pull/76#issue-1601406062))

# HumanEval-X

## Dataset Description
[HumanEval-X](https://github.com/THUDM/CodeGeeX) is a benchmark for evaluating the multilingual ability of code generative models. It consists of 820 high-quality human-crafted data samples (each with test cases) in Python, C++, Java, JavaScript, and Go, and can be used for various tasks, such as code generation and translation.

## Languages

The dataset contains coding problems in 5 programming languages: Python, C++, Java, JavaScript, and Go.

## Dataset Structure
To load the dataset you need to specify a subset among the 5 exiting languages  `[python, cpp, go, java, js]`. By default `python` is loaded. 

```python
from datasets import load_dataset
load_dataset("THUDM/humaneval-x", "js")

DatasetDict({
    test: Dataset({
        features: ['task_id', 'prompt', 'declaration', 'canonical_solution', 'test', 'example_test'],
        num_rows: 164
    })
})
```

```python
next(iter(data["test"]))
{'task_id': 'JavaScript/0',
 'prompt': '/* Check if in given list of numbers, are any two numbers closer to each other than\n  given threshold.\n  >>> hasCloseElements([1.0, 2.0, 3.0], 0.5)\n  false\n  >>> hasCloseElements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n  true\n  */\nconst hasCloseElements = (numbers, threshold) => {\n',
 'declaration': '\nconst hasCloseElements = (numbers, threshold) => {\n',
 'canonical_solution': '  for (let i = 0; i < numbers.length; i++) {\n    for (let j = 0; j < numbers.length; j++) {\n      if (i != j) {\n        let distance = Math.abs(numbers[i] - numbers[j]);\n        if (distance < threshold) {\n          return true;\n        }\n      }\n    }\n  }\n  return false;\n}\n\n',
 'test': 'const testHasCloseElements = () => {\n  console.assert(hasCloseElements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) === true)\n  console.assert(\n    hasCloseElements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) === false\n  )\n  console.assert(hasCloseElements([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) === true)\n  console.assert(hasCloseElements([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) === false)\n  console.assert(hasCloseElements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) === true)\n  console.assert(hasCloseElements([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) === true)\n  console.assert(hasCloseElements([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) === false)\n}\n\ntestHasCloseElements()\n',
 'example_test': 'const testHasCloseElements = () => {\n  console.assert(hasCloseElements([1.0, 2.0, 3.0], 0.5) === false)\n  console.assert(\n    hasCloseElements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) === true\n  )\n}\ntestHasCloseElements()\n'}
 ```


## Data Fields

*   ``task_id``: indicates the target language and ID of the problem. Language is one of ["Python", "Java", "JavaScript", "CPP", "Go"].
*   ``prompt``: the function declaration and docstring, used for code generation.
*   ``declaration``: only the function declaration, used for code translation. 
*   ``canonical_solution``: human-crafted example solutions.
*   ``test``: hidden test samples, used for evaluation.
*   ``example_test``: public test samples (appeared in prompt), used for evaluation. 

## Data Splits

Each subset has one split: test.

## Citation Information

Refer to https://github.com/THUDM/CodeGeeX.