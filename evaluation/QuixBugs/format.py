import json
import os

PROGRAMS_PATH = "python_programs"




with open("quixbugs_python.jsonl", "w") as f_out:
    for program_file in sorted(os.listdir(PROGRAMS_PATH)):
        program_name = program_file.split(".")[0]

        if program_name.endswith("_test"):
            continue
        elif program_name == "node":
            continue

        with open(os.path.join(PROGRAMS_PATH, program_file)) as f:
            program = f.read()
        
        with open(os.path.join("correct_" + PROGRAMS_PATH, program_file)) as f:
            program_correct = f.read()

        # Find docstring
        docstring_start = program.find('"""')
        # Separate docstring from program
        docstring = program[docstring_start:].strip()
        program = program[:docstring_start].strip()

        # Some correct programs contain a docstring of the incorrect program
        docstring_start_correct = program_correct.find('"""') if '"""' in program_correct else len(program_correct)
        # Separate docstring from program
        program_correct = program_correct[:docstring_start_correct].strip()

        TEST_PATH = os.path.join(
            PROGRAMS_PATH.replace("programs", "testcases"),
            "test_" + program_file,
        )

        # Tests with input and output
        if os.path.exists("json_testcases/" + program_name + ".json"):
            with open("json_testcases/" + program_name + ".json") as f:
                test_data = [json.loads(line) for line in f]
                # Custom formatting for some programs
                if program_name == "hanoi":
                    test_data = [[inp, [tuple(x) for x in out]] for inp, out in test_data]
                if program_name == "levenshtein":
                    test_data = [[inp, out] for inp, out in test_data if inp != [
                        "amanaplanacanalpanama",
                        "docnoteidissentafastneverpreventsafatnessidietoncod",
                    ]]
                if program_name == "knapsack":
                    test_data = [[inp, out] for inp, out in test_data if inp[0] != 6404180]
            
            with open(TEST_PATH) as f:
                test_function = f.read()
            tests = []
            for test in test_data:
                target = "'" + test[1] + "'" if isinstance(test[1], str) else test[1]
                if program_name in ("flatten", "kheapsort"):
                    tests.append(
                        f"assert list({program_name}(*{test[0]})) == {target}"
                    )
                elif program_name == "sqrt":
                    # assert abs(sqrt(*input_data) - expected) <= input_data[-1]
                    tests.append(
                        f"assert abs({program_name}(*{test[0]}) - {target}) <= {test[0][-1]}"
                    )
                else:
                    tests.append(
                        f"assert {program_name}(*{test[0]}) == {target}"
                    )

            tests = "\n".join(tests)
        # Tests with only input
        elif os.path.exists(TEST_PATH):
            with open(TEST_PATH) as f:
                tests = f.read()

        f_out.write(json.dumps({
            "name": program_name,
            "buggy_program": program,
            "docstring": docstring,            
            "solution": program_correct,
            "tests": tests,
        }) + "\n")
