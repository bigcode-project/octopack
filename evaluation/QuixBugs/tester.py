# make classes for extra classes and then just parse them in
# make version for proper programs

import copy
import json
import sys
import subprocess
import types

def py_try(algo, *args, correct=False):
    if not correct:
        module = __import__("python_programs."+algo)
    else:
        module = __import__("correct_python_programs."+algo)

    fx = getattr(module, algo)

    try:
        return getattr(fx,algo)(*args)
    except:
        return sys.exc_info()


def prettyprint(o):
    if isinstance(o, types.GeneratorType):
        return("(generator) " + str(list(o)))
    else:
        return(str(o))

graph_based = ["breadth_first_search",
               "depth_first_search",
               "detect_cycle",
               "minimum_spanning_tree",
               "reverse_linked_list",
               "shortest_path_length",
               "shortest_path_lengths",
               "shortest_paths",
               "topological_ordering"
              ]

if __name__ == "__main__":
    algo = sys.argv[1]

    if algo in graph_based:
        print("Correct Python:")
        correct_module = __import__("correct_python_programs."+algo+"_test")
        correct_fx = getattr(correct_module, algo+"_test")
        getattr(correct_fx,"main")()
        print()

        print("Bad Python:")
        test_module = __import__("python_programs."+algo+"_test")
        test_fx = getattr(test_module, algo+"_test")
        try:
            getattr(test_fx,"main")()
        except:
            print(sys.exc_info())
        print()

        print("Bad Java:")
        try:
            p1 = subprocess.Popen(["/usr/bin/java", "java_programs/"+algo.upper()+"_TEST"], stdout=subprocess.PIPE,
                    universal_newlines=True)
            java_out = p1.stdout.read()
            print(type(java_out))
            print(prettyprint(java_out))
        except:
            print(prettyprint(sys.exc_info()))


    else:
        working_file = open("json_testcases/"+algo+".json", 'r')

        for line in working_file:
            py_testcase = json.loads(line)
            print(py_testcase)
            test_in, test_out = py_testcase
            if not isinstance(test_in, list):
                # input is required to be a list, as multiparameter algos need to deconstruct a list of parameters
                # should fix in testcases, force all inputs to be list of inputs
                test_in = [test_in]
                # unsure how to make immutable; previous versions just used copy.deepcopy

            # check good Python version
            py_out_good = py_try(algo, *copy.deepcopy(test_in), correct=True)
            print("Correct Python: " + prettyprint(py_out_good))

            # check bad Python version
            py_out_test = py_try(algo, *copy.deepcopy(test_in))
            print("Bad Python: " + prettyprint(py_out_test))

            # check bad Java version
            try:
                p1 = subprocess.Popen(["/usr/bin/java", "JavaDeserialization", algo]+ \
                                    [json.dumps(arg) for arg in copy.deepcopy(test_in)], stdout=subprocess.PIPE,
                                    universal_newlines=True)
                java_out = p1.stdout.read()
                print("Bad Java:   " + prettyprint(java_out))
            except:
                print("Bad Java:   " + prettyprint(sys.exc_info()))

            print()
