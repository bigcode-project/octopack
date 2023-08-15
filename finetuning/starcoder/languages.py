import argparse
from datasets import load_dataset
import matplotlib.pyplot as plt
import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name_or_path", type=str, default="bigcode/large-model")
    parser.add_argument("--split", type=str)
    parser.add_argument("--data_dir", type=str)
    parser.add_argument("--dataset_text_field", type=str)
    parser.add_argument("--in_backticks", action="store_true") # default=False
    parser.add_argument("--method", type=str, default="guesslang")
    parser.add_argument("--batch_size", type=int, default=8)
    return parser.parse_args()

def get_code(text):
    first_backticks = text.find("```") # First backticks
    if first_backticks == -1 :
        # There is no backticks in text, return the whole text.
        output = text
    else :
        second_backticks = text[first_backticks+3:].find("```") # Closing backticks
        if second_backticks == -1 : 
            # No closing backticks
            # Hence, the formatting is not perfect
            # Return everything after the first_backticks
            end_index = len(text[first_backticks+3:])
        else :
            end_index = first_backticks + 3 + second_backticks
        # Now we want to get everything after first_backticks and end_index, there are two cases to handle
        # ```\n{code}
        # ```{language}\n{code}
        # We just have to find the first return after backticks
        index_return = text[first_backticks+3:].find("\n")
        if index_return == -1 :
            start_index = first_backticks + 3
        else :
            start_index = first_backticks + 3 + index_return + 1
        output = text[start_index:end_index]
    return  output

def main(args):
    dataset = load_dataset(
        args.dataset_name_or_path,
        split=args.split,
        data_dir=args.data_dir
    )
    code_snippets = [
        example[args.dataset_text_field] for example in dataset
    ]
    if args.in_backticks :
        print("We'll look at the code in backticks.")
        code_snippets = [get_code(snippet) for snippet in code_snippets]
    
    code_snippets = [code for code in code_snippets if len(code) > 0]
    
    languages = {}
    if args.method == "guesslang" :
        print("You are using Guesslang.")
        from guesslang import guess
        g = guess.Guess()
        for code in code_snippets :
            try : 
                lan = g.language_name(code)
                if lan in languages :
                    languages[lan] += 1
                else :
                    languages[lan] = 1
            except :
                pass
    elif args.method == "whats-that-code" :
        print("You are using whats-that-code")
        from whats_that_code.election import guess_language_all_methods
        for code in code_snippets :
            try : 
                lan = guess_language_all_methods(code)
                if lan in languages :
                    languages[lan] += 1
                else :
                    languages[lan] = 1
            except :
                pass
    elif args.method == "CodeBERTa" :
        print("You are using CodeBERTa, it may take a certain amount of time. Feel free to try another method.")
        from transformers import RobertaTokenizer, RobertaForSequenceClassification
        from tqdm import tqdm
        CODEBERTA_LANGUAGE_ID = "huggingface/CodeBERTa-language-id"

        tokenizer = RobertaTokenizer.from_pretrained(CODEBERTA_LANGUAGE_ID)
        model = RobertaForSequenceClassification.from_pretrained(CODEBERTA_LANGUAGE_ID)

        id2label = {
            0 : "go",
            1 : "java",
            2 : "javascript",
            3 : "php",
            4 : "python",
            5 : "ruby"
        }
        
        inputs = tokenizer(code_snippets, return_tensors="pt", truncation=True, padding=True, max_length=512)
        batch_size = args.batch_size
        N = len(code_snippets)
        for i in tqdm(range(0, N, batch_size)):
            input_ids = inputs["input_ids"][i:i+batch_size]
            attention_mask = inputs["attention_mask"][i:i+batch_size]
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            predictions = outputs.logits.argmax(-1).tolist()
            predictions = [id2label[label] for label in predictions]
            for lan in predictions : 
                if lan in languages :
                    languages[lan] += 1
                else :
                    languages[lan] = 1
    else :
        ValueError("Unsupported method for programming language detection.")

    names = list(languages.keys())
    values = list(languages.values())
    indices = np.argsort(-np.array(values))
    names = [names[i] for i in indices]
    values = [values[i] for i in indices]
    plt.figure(figsize = (15, 9))
    plt.bar(range(len(names)), values, tick_label=names)
    plt.xticks(rotation=90)
    plt.title(f"Programming language repartition in {args.dataset_name_or_path.split('/')[-1]}")
    plt.show()

if __name__ == "__main__" :
    args = get_args()
    main(args)