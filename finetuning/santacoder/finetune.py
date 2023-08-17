"""
Fine-Tune SantaCoder on Github commits diff dataset
"""

import argparse
import os
from functools import partial
from datasets import concatenate_datasets
from datasets import load_dataset, Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    DataCollatorWithPadding,
    TrainingArguments,
    logging,
    set_seed
)
import difflib
import numpy as np


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="bigcode/santacoder")
    parser.add_argument("--dataset_name", type=str, default="bigcode/instruction-commits")
    # parser.add_argument("--subset", type=str, default="data")
    parser.add_argument("--split", type=str, default="train")
    parser.add_argument("--cache_dir", type=str, default="/tmp/santacoder-github-cleaned")
    parser.add_argument("--size_valid_set", type=int, default=5000)
    parser.add_argument("--streaming", action="store_true")
    parser.add_argument("--shuffle_buffer", type=int, default=25600)

    parser.add_argument("--max_input_length", type=int, default=2048)
    parser.add_argument("--max_steps", type=int, default=10000)
    parser.add_argument("--message_min_token", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=8)
    parser.add_argument("--eos_token_id", type=int, default=49152)

    parser.add_argument("--learning_rate", type=float, default=5e-5)
    parser.add_argument("--lr_scheduler_type", type=str, default="cosine")
    parser.add_argument("--num_warmup_steps", type=int, default=100)
    parser.add_argument("--weight_decay", type=float, default=0.05)

    parser.add_argument("--local_rank", type=int, default=0)
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--bf16", action="store_true")
    parser.add_argument("--output_diff", action="store_true")
    parser.add_argument("--gradient_checkpointing", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_workers", type=int, default=None)
    parser.add_argument("--output_dir", type=str, default="/tmp/checkpoints")
    parser.add_argument("--deepspeed", type=str, default=None)
    parser.add_argument("--log_freq", default=1, type=int)
    parser.add_argument("--eval_freq", default=1000, type=int)
    parser.add_argument("--save_freq", default=1000, type=int)
    parser.add_argument("--predict_with_generate", action="store_true")
    parser.add_argument("--compute_loss_on_input", default=False, action="store_true")
    parser.add_argument("--compute_loss_on_instruction", default=False, action="store_true")
    parser.add_argument("--data_packing", default=False, action="store_true")
    parser.add_argument("--add_file_name", default=False, action="store_true")
    parser.add_argument("--flan_file_path", type=str, default=None)
    parser.add_argument("--line_diff", default=False, action="store_true")

    return parser.parse_args()


tokenizer = AutoTokenizer.from_pretrained("bigcode/santacoder")
tokenizer.pad_token = tokenizer.eos_token
tokenizer.sep_token = tokenizer.eos_token


def preprocess_function(examples, args, is_train):
    inputs = examples["input"]
    targets = examples["output"]
    model_inputs = [inp + tar + tokenizer.eos_token for inp, tar in zip(inputs, targets)]

    # do not do packing for fair comparison with no packing
    if args.data_packing and is_train:
        model_inputs = tokenizer(model_inputs,
                                 max_length=args.max_input_length,
                                 # no padding to calculate the real length
                                 padding=False,
                                 truncation=True)
        # packing in the input_ids level
        max_window = args.max_input_length
        # packed_length maintains a list, each of which is a list of all packed sequence lengths in this sequence
        packed_lengths, packed_ids, = [], []
        temp_length, temp_ids = 0, []
        for input_ids in model_inputs["input_ids"]:
            if temp_length + len(input_ids) >= max_window:
                packed_lengths.append(temp_length)
                packed_ids.append(temp_ids.copy())
                # refresh for the next packed sequence
                temp_length = 0
                temp_ids.clear()
            temp_ids.extend(input_ids)
            temp_length += len(input_ids)
        # add the last one
        if temp_length > 0:
            packed_lengths.append(temp_length)
            packed_ids.append(temp_ids.copy())
        # pad the packed_ids into max_window
        padded_input_ids = np.zeros((len(packed_ids), max_window), dtype=np.int64)
        padded_attention_masks = np.zeros((len(packed_ids), max_window), dtype=np.int64)
        for i, example_input_ids in enumerate(packed_ids):
            padded_input_ids[i, :packed_lengths[i]] = example_input_ids
            # obtain the attention mask
            padded_attention_masks[i, :packed_lengths[i]] += 1
        model_inputs["input_ids"] = padded_input_ids
        model_inputs["attention_mask"] = padded_attention_masks
        # take the last valid eos token as the end of the sequence
        first_eos_indices = [packed_lengths[i] - 1 for i in range(len(packed_lengths))]
    else:
        assert tokenizer.eos_token_id == tokenizer.pad_token_id
        model_inputs = tokenizer(model_inputs,
                                 max_length=args.max_input_length,
                                 padding="max_length",
                                 truncation=True)
        # This relies on tokenizer.eos_token_id == tokenizer.pad_token_id
        first_eos_indices = [
            model_inputs["input_ids"][i].index(tokenizer.eos_token_id)
            if model_inputs["input_ids"][i][-1] == tokenizer.eos_token_id else args.max_input_length
            for i in range(len(model_inputs["input_ids"]))
        ]

    if args.compute_loss_on_input:
        assert args.compute_loss_on_instruction is False
        model_inputs["labels"] = [
            list(inp[:first_eos_indices[i] + 1]) + [-100] * (args.max_input_length - first_eos_indices[i] - 1)
            for i, inp in enumerate(model_inputs["input_ids"])
        ]
    else:
        inputs = tokenizer(
            inputs, max_length=args.max_input_length, padding=False, truncation=True
        )["input_ids"]
        # -100 means ignore in loss computation; Make sure only one final eos token is predicted
        model_inputs["labels"] = [
            [-100] * len(inp) + inp_target[len(inp):first_eos_indices[i] + 1] + [-100] * (
                    args.max_input_length - first_eos_indices[i] - 1)
            for i, (inp, inp_target) in enumerate(zip(inputs, model_inputs["input_ids"]))
        ]
    return model_inputs


def create_datasets(args):
    dataset = load_dataset(
        args.dataset_name,
        split=args.split,
        use_auth_token=True,
        num_proc=args.num_workers if not args.streaming else None,
        streaming=args.streaming,
        cache_dir=args.cache_dir
    )

    # if streaming, we only use a small portion of the dataset for debugging
    if args.streaming:
        sample_number = 100
        train_data = []
        for i in range(sample_number):
            train_data.append(next(iter(dataset)))
        dataset = Dataset.from_list(train_data)

    dataset = dataset.train_test_split(test_size=0.005, seed=args.seed)


    def generate_line_diff(original_code, modified_code):
        original_code = original_code.strip()
        modified_code = modified_code.strip()
        original_lines = original_code.splitlines(keepends=True)
        modified_lines = modified_code.splitlines(keepends=True)

        # Add line numbers to original and modified code
        original_code_with_line_numbers = ''.join(f"{i + 1:3d} {line}" for i, line in enumerate(original_lines))
        modified_code_with_line_numbers = ''.join(f"{i + 1:3d} {line}" for i, line in enumerate(modified_lines))

        diff = difflib.unified_diff(original_code_with_line_numbers.splitlines(),
                                    modified_code_with_line_numbers.splitlines(), 
                                    fromfile='Original', 
                                    tofile='Modified', 
                                    lineterm='')
        # remove the first line and second line
        # print(diff)
        try:
            next(diff)
            next(diff)
            diff_with_line_numbers = '\n'.join(f"{line}" for line in diff if line.startswith(('+', '-')))
            return original_code_with_line_numbers, diff_with_line_numbers
        except StopIteration:
            return original_code_with_line_numbers, ""

    def unify_format(examples):
        if args.flan_file_path is not None:
            input_template = "Instructions: {instruction}\nInput:\n{input}\nOutput:\n"
        elif args.compute_loss_on_instruction:
            input_template = "<commit_before>\n{input}\n<commit_msg>"
        else:
            input_template = "<commit_before>\n{input}\n<commit_msg>\n{instruction}\n<commit_after>\n"

        # the example is from our old dataset
        if "content" in examples:
            # 14 is the character length of "<commit_after>"
            inputs = [inp[:inp.index("<commit_after>") + 14] for inp in examples["content"]]
            targets = [inp[inp.index("<commit_after>") + 14:] for inp in examples["content"]]
        # the example if from the diff dataset
        elif "diff" in examples:
            if args.compute_loss_on_instruction:
                inputs = [
                    input_template.format(input=content.strip())
                    for content in examples["old_contents"]
                ]
                targets = [
                    sub_example + "\n<commit_after>\n" + diff_example
                    for sub_example, diff_example in zip(examples["subject"], examples["diff"])
                ]
            else:
                inputs = [
                    input_template.format(input=content.strip(), instruction=message.strip())
                    for content, message in zip(examples["old_contents"], examples["subject"])
                ]
                targets = examples["diff"]
        # the example is from our new dataset
        else:
            if args.compute_loss_on_instruction:
                inputs = [input_template.format(input=content.strip()) for content in examples["old_contents"]]
                targets = [
                    sub_example + "<commit_after>" + new_example
                    for sub_example, new_example in zip(examples["subject"], examples["new_contents"])
                ]
            else:
                # if apply diff
                if args.line_diff:
                    # compute the line-level diff
                    diff_results = [
                        generate_line_diff(content, new_content)
                        for content, new_content in zip(examples["old_contents"], examples["new_contents"])
                    ]
                    inputs, targets = [], []
                    for i, (content, diff_content) in enumerate(diff_results):
                        inputs.append(input_template.format(input=content.rstrip(), instruction=examples["subject"][i].strip()))
                        targets.append(diff_content)
                else:
                    inputs = [
                        input_template.format(input=content.strip(), instruction=message.strip())
                        for content, message in zip(examples["old_contents"], examples["subject"])
                    ]
                    targets = examples["new_contents"]

                    
        if args.add_file_name:
            file_names = [file_path.split("/")[-1] for file_path in examples["old_file"]]
            inputs = [f"<file_name>\n{file_name}\n{inp}" for file_name, inp in zip(file_names, inputs)]

        examples["input"] = inputs
        examples["output"] = targets
        return examples

    if not args.compute_loss_on_input:
        # TODO: currently we do not support data packing when not computing loss on input
        assert args.data_packing is False, "data packing can be used when computing loss on input"

    train_data = dataset["train"].map(unify_format, batched=True, num_proc=args.num_workers)
    valid_data = dataset["test"].map(unify_format, batched=True, num_proc=args.num_workers)
    # if the flan file path is not None, add them into the current train set
    if args.flan_file_path is not None:
        flan_dataset = load_dataset(
            "json",
            data_files=args.flan_file_path,
            use_auth_token=True,
            num_proc=args.num_workers if not args.streaming else None,
            streaming=args.streaming,
            cache_dir=args.cache_dir,
        )
        train_data = concatenate_datasets([train_data, flan_dataset["train"]])
    # shuffle dataset
    train_data = train_data.shuffle(seed=args.seed)
    print(
        f"Size of the train set: {len(train_data)}. Size of the validation set: {len(valid_data)}"
    )

    column_names = dataset.column_names["train"] + ["input", "output"]
    train_dataset = train_data.map(
        partial(preprocess_function, args=args, is_train=True),
        batched=True,
        num_proc=args.num_workers,
        remove_columns=column_names,
        load_from_cache_file=True,
        desc="Running tokenizer on train dataset",
    )
    valid_dataset = valid_data.map(
        partial(preprocess_function, args=args, is_train=False),
        batched=True,
        num_proc=args.num_workers,
        remove_columns=column_names,
        load_from_cache_file=True,
        desc="Running tokenizer on validation dataset",
    )

    return train_dataset, valid_dataset


def run_training(args, train_data, val_data):
    print("Loading the model")
    # disable caching mechanism when using gradient checkpointing
    model = AutoModelForCausalLM.from_pretrained(
        args.model_path,
        trust_remote_code=True,
        use_cache=not args.gradient_checkpointing
    )

    print("Model loaded")
    train_data.start_iteration = 0

    print(f"Starting main loop")

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        dataloader_drop_last=True,
        evaluation_strategy="steps",
        max_steps=args.max_steps,
        eval_steps=args.eval_freq,
        save_steps=args.save_freq,
        logging_steps=args.log_freq,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        lr_scheduler_type=args.lr_scheduler_type,
        warmup_steps=args.num_warmup_steps,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        gradient_checkpointing=args.gradient_checkpointing,
        fp16=args.fp16,
        bf16=args.bf16,
        deepspeed=args.deepspeed,
        weight_decay=args.weight_decay,
        run_name=args.output_dir,
        report_to="wandb"
    )
    # Data collator
    data_collator = DataCollatorWithPadding(
        tokenizer,
        pad_to_multiple_of=8 if training_args.fp16 else None,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=val_data,
        tokenizer=tokenizer,
        data_collator=data_collator,
        # callbacks=[EvaluateDebugCallback()]
    )

    print("Training...")
    trainer.train()

    print("Saving last checkpoint of the model")
    model.save_pretrained(os.path.join(args.output_dir, "final_checkpoint/"))


def main(args):
    train_dataset, eval_dataset = create_datasets(args)
    run_training(args, train_dataset, eval_dataset)


if __name__ == "__main__":
    args = get_args()
    set_seed(args.seed)
    os.makedirs(args.output_dir, exist_ok=True)

    logging.set_verbosity_error()

    main(args)
