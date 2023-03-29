# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""HumanEval-X dataset."""


import json
import datasets



_DESCRIPTION = """
HumanEval-X is a benchmark for the evaluation of the multilingual ability of code generative models. \
It consists of 820 high-quality human-crafted data samples (each with test cases) in Python, C++, Java, JavaScript, and Go, and can be used for various tasks.
"""

_HOMEPAGE = "https://github.com/THUDM/CodeGeeX"

def get_url(name):
    url = f"data/{name}/data/humaneval.jsonl"
    return url

def split_generator(dl_manager, name):
    downloaded_files = dl_manager.download(get_url(name))
    return [
        datasets.SplitGenerator(
            name=datasets.Split.TEST,
            gen_kwargs={
                "filepath": downloaded_files,
            },
        )
    ]

class HumanEvalXConfig(datasets.BuilderConfig):
    """BuilderConfig """

    def __init__(self, name, description, features, **kwargs):
        super(HumanEvalXConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.name = name
        self.description = description
        self.features = features


class HumanEvalX(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        HumanEvalXConfig(
            name="python",
            description="Python HumanEval",
            features=["task_id", "prompt", "declaration", "canonical_solution", "test", "example_test"]
        ),
        HumanEvalXConfig(
            name="cpp",
            description="C++ HumanEval",
            features=["task_id", "prompt", "declaration", "canonical_solution", "test", "example_test"]
        ),

        HumanEvalXConfig(
            name="go",
            description="Go HumanEval",
            features=["task_id", "prompt", "declaration", "canonical_solution", "test", "example_test"]
        ),
        HumanEvalXConfig(
            name="java",
            description="Java HumanEval",
            features=["task_id", "prompt", "declaration", "canonical_solution", "test", "example_test"]
        ),

        HumanEvalXConfig(
            name="js",
            description="JavaScript HumanEval",
            features=["task_id", "prompt", "declaration", "canonical_solution", "test", "example_test"]
        ),
        ]
    DEFAULT_CONFIG_NAME = "python"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"task_id": datasets.Value("string"),
                                        "prompt": datasets.Value("string"),
                                        "declaration": datasets.Value("string"),
                                        "canonical_solution": datasets.Value("string"),
                                        "test": datasets.Value("string"),
                                        "example_test": datasets.Value("string"),
                                        }),
            homepage=_HOMEPAGE,
        )

    def _split_generators(self, dl_manager):
        if self.config.name == "python":
            return split_generator(dl_manager, self.config.name)

        elif self.config.name == "cpp":
            return split_generator(dl_manager, self.config.name)

        elif self.config.name == "go":
            return split_generator(dl_manager, self.config.name)

        elif self.config.name == "java":
            return split_generator(dl_manager, self.config.name)

        elif self.config.name == "js":
            return split_generator(dl_manager, self.config.name)
           
    def _generate_examples(self, filepath):
        key = 0
        with open(filepath) as f:
            for line in f:
                row = json.loads(line)
                key += 1
                yield key, {
                    "task_id": row["task_id"],
                    "prompt": row["prompt"],
                    "declaration": row["declaration"],
                    "canonical_solution": row["canonical_solution"],
                    "test": row["test"],
                    "example_test": row["example_test"],

                }  
                key += 1