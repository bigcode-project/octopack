# Fine-tuning

## Fine-tuning StarCoder with PEFT

Here is provided the code we used in order to fine-tune StarCoder on different data mixtures. It is significantly similar to the [official repository](https://github.com/bigcode-project/starcoder). The installation requirements and the usage are the same, please refer the [documentation](https://github.com/bigcode-project/starcoder#quickstart) for the details. We performed minor changes:
- The new argument `--targets_only` allows to compute the loss for the instruction fine-tuning only on the targets.
- The argument `output_column_name` can be `None`. In such case, the column `input_column_name` is going to be the object of the training and the loss will be computed on its whole content.

## Programming Language distribution
We provide a way to get the programming language distribution in a given dataset. Currently we support three methods.

**DISCLAIMER** : We do not guarantee the effectiveness of any of them.

### Guesslang
[Guesslang](https://github.com/yoeo/guesslang/) is an open source software that help to detect the programming language to which a given text corresponds to. It supports more than 50 programming languages and has an accuracy above 90%.

It can be installed as follows
```bash
pip3 install guesslang
```
However, we recommend to install it directly from the source like this
```bash
git clone https://github.com/yoeo/guesslang/
cd guesslang 
pip3 install .
```
For those who are use tensorflow > 2.5.0 and/or python 3.10+, you may run into a tensorflow error. Make sure to remove `tensorflow==2.5.0` from the file `guesslang/requirements.txt` before running `pip3 install .`.

### Whats-that-code
[Whats-that-code](https://github.com/matthewdeanmartin/whats_that_code) is another alternative for programming language. The installation command is the following
```
pip install whats-that-code
```

### CodeBERTa
This method makes use of [CodeBERTa-language-id](https://huggingface.co/huggingface/CodeBERTa-language-id), a Language Model fine-tuned on a programming language identification task. However, it supports only 6 programming languages, python, go, java, javascript, ruby and php.

### Usage
The code is designed to a load a dataset from [HuggingFace's datasets Hub](https://huggingface.co/datasets?sort=trending) and check the programming languages distribution in a column of interest (`dataset_text_field`). You can decide which method to use (argument `method`) and if you just want to examine the text between backticks(```).

```bash
python languages.py \
    --dataset_name_or_path "codeparrot/self-instruct-starcoder" \
    --split "train" \
    --dataset_text_field \
    --in_backticks \
    --method "guesslang" \
```
