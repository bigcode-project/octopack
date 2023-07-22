import glob
import json
import random
import math
import os

random.seed(42)

files = {
    "xp3_Fraser_python_state_changes_None_train_needcode.jsonl": 50,
    "xp3_Fraser_python_state_changes_None_train_newval.jsonl": 70,
    "xp3_Fraser_python_state_changes_None_train_startend.jsonl": 50,
    "xp3_Fraser_python_state_changes_None_train_varbeg.jsonl": 50,
    "xp3_Muennighoff_mbpp_sanitized_test_function_solution.jsonl": 100,
    "xp3_Muennighoff_mbpp_sanitized_test_function_solved.jsonl": 100,
    "xp3_codeparrot_apps_all_test_abovesol.jsonl": 140,
    "xp3_codeparrot_apps_all_test_qsol.jsonl": 140,
    "xp3_codeparrot_apps_all_train_abovesol.jsonl": 140,
    "xp3_codeparrot_apps_all_train_qsol.jsonl": 140,
    "xp3_codeparrot_codecomplex_codeparrot__codecomplex_train_identifycomplexity.jsonl": 40,
    "xp3_codeparrot_codecomplex_codeparrot__codecomplex_train_whatcomplexity.jsonl": 90,
    "xp3_codeparrot_codecomplex_codeparrot__codecomplex_train_whichcomplexity.jsonl": 90,
    "xp3_codeparrot_github_jupyter_text_code_pairs_None_train_code.jsonl": 10,
    "xp3_codeparrot_github_jupyter_text_code_pairs_None_train_genmarkdown.jsonl": 10,
    "xp3_codeparrot_github_jupyter_text_code_pairs_None_train_markdowncode.jsonl": 10,
    "xp3_codeparrot_github_jupyter_text_code_pairs_None_train_taskcode.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_C++_program_level_test_abovecpp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_C++_program_level_test_solcpp.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_C++_program_level_train_abovecpp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_C++_program_level_train_solcpp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_C++_program_level_validation_abovecpp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_C++_program_level_validation_solcpp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_C_program_level_test_abovec.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_C_program_level_test_solc.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_C_program_level_train_abovec.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_C_program_level_train_solc.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_C_program_level_validation_abovec.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_C_program_level_validation_solc.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Csharp_program_level_test_abovecsharp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Csharp_program_level_test_solcsharp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Csharp_program_level_train_abovecsharp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Csharp_program_level_train_solcsharp.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_Csharp_program_level_validation_abovecsharp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Csharp_program_level_validation_solcsharp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Java_program_level_test_abovejava.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Java_program_level_test_soljava.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_Java_program_level_train_abovejava.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Java_program_level_train_soljava.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_Java_program_level_validation_abovejava.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Java_program_level_validation_soljava.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_Javascript_program_level_test_abovejs.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Javascript_program_level_test_soljs.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_Javascript_program_level_train_abovejs.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Javascript_program_level_train_soljs.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_Javascript_program_level_validation_abovejs.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Javascript_program_level_validation_soljs.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_PHP_program_level_test_abovephp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_PHP_program_level_test_solphp.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_PHP_program_level_train_abovephp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_PHP_program_level_train_solphp.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_PHP_program_level_validation_abovephp.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_PHP_program_level_validation_solphp.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_Python_program_level_test_abovepy.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Python_program_level_test_solpy.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_Python_program_level_train_abovepy.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Python_program_level_train_solpy.jsonl": 10,
    "xp3_codeparrot_xlcost_text_to_code_Python_program_level_validation_abovepy.jsonl": 50,
    "xp3_codeparrot_xlcost_text_to_code_Python_program_level_validation_solpy.jsonl": 10,
    "xp3_great_code_None_test_bug_detection.jsonl": 50,
    "xp3_great_code_None_test_fix_buggy_line.jsonl": 50,
    "xp3_great_code_None_test_identifier_prediction_no_choices.jsonl": 50,
    "xp3_great_code_None_test_identifier_prediction_with_choices.jsonl": 50,
    "xp3_great_code_None_train_bug_detection.jsonl": 50,
    "xp3_great_code_None_train_fix_buggy_line.jsonl": 50,
    "xp3_great_code_None_train_identifier_prediction_no_choices.jsonl": 50,
    "xp3_great_code_None_train_identifier_prediction_with_choices.jsonl": 50,
    "xp3_great_code_None_validation_bug_detection.jsonl": 50,
    "xp3_great_code_None_validation_fix_buggy_line.jsonl": 50,
    "xp3_great_code_None_validation_identifier_prediction_no_choices.jsonl": 50,
    "xp3_great_code_None_validation_identifier_prediction_with_choices.jsonl": 50,
#    "xp3_neural_code_search_evaluation_dataset_train_generate_a_description_given_code.jsonl": 50,
#    "xp3_neural_code_search_evaluation_dataset_train_generate_code_given_a_description.jsonl": 80,
    "xp3_teven_code_contests_None_test_abovesol.jsonl": 90,
    "xp3_teven_code_contests_None_test_contsol.jsonl": 30,
    "xp3_teven_code_contests_None_test_descsol.jsonl": 60,
    "xp3_teven_code_contests_None_test_langsol.jsonl": 90,
    "xp3_teven_code_contests_None_test_priortask.jsonl": 90,
    "xp3_teven_code_contests_None_test_solfor.jsonl": 50,
    "xp3_teven_code_contests_None_test_soltask.jsonl": 90,
    "xp3_teven_code_contests_None_train_abovesol.jsonl": 90,
    "xp3_teven_code_contests_None_train_contsol.jsonl": 30,
    "xp3_teven_code_contests_None_train_descsol.jsonl": 60,
    "xp3_teven_code_contests_None_train_langsol.jsonl": 90,
    "xp3_teven_code_contests_None_train_priortask.jsonl": 90,
    "xp3_teven_code_contests_None_train_solfor.jsonl": 50,
    "xp3_teven_code_contests_None_train_soltask.jsonl": 90,
    "xp3_teven_code_contests_None_valid_abovesol.jsonl": 90,
    "xp3_teven_code_contests_None_valid_contsol.jsonl": 30,
    "xp3_teven_code_contests_None_valid_descsol.jsonl": 60,
    "xp3_teven_code_contests_None_valid_langsol.jsonl": 90,
    "xp3_teven_code_contests_None_valid_priortask.jsonl": 50,
    "xp3_teven_code_contests_None_valid_solfor.jsonl": 50,
    "xp3_teven_code_contests_None_valid_soltask.jsonl": 90,
    "xp3_teven_code_docstring_corpus_top_level_top_level_complete.jsonl": 50,
    "xp3_teven_code_docstring_corpus_top_level_top_level_funccont.jsonl": 50,
    "xp3_teven_code_docstring_corpus_top_level_top_level_funcname.jsonl": 100,
}

samples = []
for f_name, c in files.items():
    print(f_name)
    with open(f_name, "r") as f:
        lines = [json.loads(x) for x in f.readlines()]
        if "mbpp" in f_name:
            for l in lines:
                l['inputs'] = l['inputs'].replace("Here is a solution in Python:", "Write a solution in Python.").replace("This can be solved in Python with the following code:", "How to solve it in Python?")
        elif "neuralcode" in f_name:
            for l in lines:
                l['inputs'] = l['inputs'].replace("Describe it:", "Describe it.")
        samples += random.sample(lines, c)

assert len(samples) == sum(files.values())
random.shuffle(samples)
with open(f"xp3x_code_5k.jsonl", "w") as f:
    for s in samples:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")

