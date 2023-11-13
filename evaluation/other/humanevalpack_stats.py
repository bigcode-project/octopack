from datasets import load_dataset



for lang in ['python', 'js', 'cpp', 'java', 'go', 'rust']:
    print(f'Language: {lang}')
    ds = load_dataset('bigcode/humanevalpack', lang, split="test")
    # Average docstring length
    print(f'Average docstring length: {sum([len(d) for d in ds["docstring"]]) / len(ds["docstring"])}')
    # Min docstring length
    print(f'Min docstring length: {min([len(d) for d in ds["docstring"]])}')
    # Max docstring length
    print(f'Max docstring length: {max([len(d) for d in ds["docstring"]])}')
    # Average solution length
    print(f'Average solution length: {sum([len(d) for d in ds["canonical_solution"]]) / len(ds["canonical_solution"])}')
    # Min solution length
    print(f'Min solution length: {min([len(d) for d in ds["canonical_solution"]])}')
    # Max solution length
    print(f'Max solution length: {max([len(d) for d in ds["canonical_solution"]])}')