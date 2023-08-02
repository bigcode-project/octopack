import json
import sys
import random

# {"commit":"b4829b41402321a0a6f0f3c02766a5b25ebd09a1","old_file":"test\/clang-tidy\/hicpp-exception-baseclass.cpp","new_file":"test\/clang-tidy\/hicpp-exception-baseclass.cpp","old_contents":"\/\/ RUN: %check_clang_tidy %s hicpp-exception-baseclass %t\n\nnamespace std {\nclass exception {};\n} \/\/ namespace std\n\nclass derived_exception : public std::exception {};\nclass non_derived_exception {};\n\nvoid problematic() {\n  try {\n    throw int(42); \/\/ Built in is not allowed\n\/\/ CHECK-MESSAGES: [[@LINE-1]]:5: warning: throwing an exception whose type is not derived from 'std::exception'\n  } catch (int e) {\n  }\n  throw int(42); \/\/ Bad\n\/\/ CHECK-MESSAGES: [[@LINE-1]]:3: warning: throwing an exception whose type is not derived from 'std::exception'\n\n  try {\n    throw non_derived_exception(); \/\/ Some class is not allowed\n\/\/ CHECK-MESSAGES: [[@LINE-1]]:5: warning: throwing an exception whose type is not derived from 'std::exception'\n\/\/ CHECK-MESSAGES: 8:1: note: type defined here\n  } catch (non_derived_exception &e) { \n  }\n  throw non_derived_exception(); \/\/ Bad\n\/\/ CHECK-MESSAGES: [[@LINE-1]]:3: warning: throwing an exception whose type is not derived from 'std::exception'\n\/\/ CHECK-MESSAGES: 8:1: note: type defined here\n}\n\nvoid allowed_throws() {\n  try {\n    throw std::exception(); \/\/ Ok\n  } catch (std::exception &e) { \/\/ Ok\n  }\n  throw std::exception();\n\n  try {\n    throw derived_exception(); \/\/ Ok\n  } catch (derived_exception &e) { \/\/ Ok\n  }\n  throw derived_exception(); \/\/ Ok\n}\n","new_contents":"\/\/ RUN: %check_clang_tidy %s hicpp-exception-baseclass %t -- -- -fcxx-exceptions\n\nnamespace std {\nclass exception {};\n} \/\/ namespace std\n\nclass derived_exception : public std::exception {};\nclass non_derived_exception {};\n\nvoid problematic() {\n  try {\n    throw int(42); \/\/ Built in is not allowed\n\/\/ CHECK-MESSAGES: [[@LINE-1]]:5: warning: throwing an exception whose type is not derived from 'std::exception'\n  } catch (int e) {\n  }\n  throw int(42); \/\/ Bad\n\/\/ CHECK-MESSAGES: [[@LINE-1]]:3: warning: throwing an exception whose type is not derived from 'std::exception'\n\n  try {\n    throw non_derived_exception(); \/\/ Some class is not allowed\n\/\/ CHECK-MESSAGES: [[@LINE-1]]:5: warning: throwing an exception whose type is not derived from 'std::exception'\n\/\/ CHECK-MESSAGES: 8:1: note: type defined here\n  } catch (non_derived_exception &e) {\n  }\n  throw non_derived_exception(); \/\/ Bad\n\/\/ CHECK-MESSAGES: [[@LINE-1]]:3: warning: throwing an exception whose type is not derived from 'std::exception'\n\/\/ CHECK-MESSAGES: 8:1: note: type defined here\n}\n\nvoid allowed_throws() {\n  try {\n    throw std::exception(); \/\/ Ok\n  } catch (std::exception &e) { \/\/ Ok\n  }\n  throw std::exception();\n\n  try {\n    throw derived_exception(); \/\/ Ok\n  } catch (derived_exception &e) { \/\/ Ok\n  }\n  throw derived_exception(); \/\/ Ok\n}\n","subject":"Enable exceptions for this test case to speculatively fix the build bots.","message":"Enable exceptions for this test case to speculatively fix the build bots.\n\nHopefully corrects: http:\/\/lab.llvm.org:8011\/builders\/llvm-clang-lld-x86_64-scei-ps4-ubuntu-fast\/builds\/15666\n\ngit-svn-id: a34e9779ed74578ad5922b3306b3d80a0c825546@310732 91177308-0d34-0410-b5e6-96231b3b80d8\n","lang":"C++","license":"apache-2.0","repos":"llvm-mirror\/clang-tools-extra,llvm-mirror\/clang-tools-extra,llvm-mirror\/clang-tools-extra,llvm-mirror\/clang-tools-extra"}
path = sys.argv[1]
NUM_SELECT = 100

random.seed(42)

# Manually chosen lines
### CPP ### # 70 samples
INDICES = [3, 10, 17, 19, 21, 23, 26, 27, 28, 35, 36, 38, 41, 912, 1791, 4139, 4597, 4598, 4647, 4791, 876, 4868, 2231, 2308, 2162, 4140, 4594, 1221, 1213, 3520, 326, 2044, 842, 2897, 1822, 3264, 2689, 3274, 226, 4189, 947, 1557, 4410, 2983, 573, 1020, 2460, 3105, 1425, 4488, 2350, 3892, 3730, 3395, 1592, 3145, 4049, 1208, 1792, 2025, 4270, 2249, 2225, 526, 3398, 3339, 4445, 3816, 1694, 3432]
IDX_OFFSET = 493
#"""
### PYTHON ### # 89 samples
#INDICES = [7296, 48598, 16049, 9144, 48540, 35741, 5697, 27651, 1739, 36781, 13031, 35713, 27493, 38618, 53046, 425, 49729, 14110, 50036, 22059, 24898, 17335, 30108, 35142, 24807, 41198, 37837, 43336, 50663, 5229, 18217, 23909, 13730, 44796, 39920, 41613, 16043, 14392, 44866, 21252, 32717, 25928, 9363, 9150, 48823, 36789, 17219, 48956, 38242, 27666, 39086, 39052, 30674, 22293, 10365, 33271, 24504, 34757, 32021, 5613, 47966, 49497, 26148, 29588, 14725, 1378, 38564, 47780, 44129, 42824, 42348, 3972, 26386, 22236, 16295, 27648, 18254, 16371, 4940, 29041, 52954, 15491, 26282, 10789, 141, 14267, 35533, 49019, 4453]
#IDX_OFFSET = 394

### RUST ### # 75 samples
INDICES = [2619, 456, 1003, 419, 2771, 2233, 2418, 130, 952, 2069, 108, 2298, 1718, 1839, 1139, 418, 1470, 322, 2533, 1093, 2495, 1002, 669, 899, 2804, 938, 1643, 1620, 2989, 1010, 1076, 1729, 1576, 1917, 2167, 2994, 1858, 1078, 435, 1222, 2617, 2973, 1486, 237, 986, 2941, 350, 1990, 525, 2702, 2251, 676, 2484, 823, 1276, 1634, 2751, 1849, 495, 1015, 942, 937, 1140, 397, 1765, 1912, 221, 2676, 248, 1018, 2944, 2983, 2755, 1023, 2276]
IDX_OFFSET = 306

### GO ### # 72 samples
#INDICES = [204, 2253, 2006, 1828, 4467, 3456, 1791, 1905, 4931, 3436, 3679, 2278, 53, 1307, 3462, 1763, 2757, 2817, 4945, 3763, 1022, 3100, 2401, 2962, 1575, 375, 653, 3113, 2277, 3108, 2211, 4562, 1876, 2584, 542, 4646, 2577, 4998, 2020, 4598, 2020, 4780, 3271, 744, 898, 26, 871, 2444, 1629, 4889, 3063, 1323, 4418, 4344, 159, 2519, 4503, 552, 580, 1949, 1083, 1990, 2902, 3469, 4393, 3675, 4993, 3789, 3630, 3329, 2172, 4552]
#IDX_OFFSET = 263

#"""
### JAVA ### # 86 samples
#INDICES = [204, 2253, 2006, 1828, 4467, 3456, 1791, 1905, 4931, 3436, 3679, 2278, 53, 1307, 3462, 1763, 2757, 2817, 4945, 3763, 1022, 3100, 2401, 2962, 1575, 375, 653, 3113, 2277, 3108, 2211, 4562, 1876, 2584, 542, 4646, 2577, 4998, 2020, 4598, 2020, 4780, 3271, 744, 898, 26, 871, 2444, 1629, 4889, 3063, 1323, 4418, 4344, 159, 2519, 4503, 552, 580, 1949, 1083, 1990, 2902, 3469, 4393, 3675, 4993, 3789, 3630, 3329, 2172, 4552, 12418, 9347, 13861, 10276, 17403, 5158, 2245, 1302, 10366, 12969, 10360, 15017, 20368, 9912]
#IDX_OFFSET = 341
#"""
### JAVASCRIPT ### # 61 samples
#INDICES = [14628, 6717, 44348, 35741, 27651, 6140, 14328, 33118, 1739, 46925, 45962, 35713, 14446, 52810, 45753, 22298, 14110, 50036, 24898, 17335, 2847, 24807, 36178, 19213, 23700, 4558, 3003, 29714, 24260, 17496, 16043, 2103, 4337, 37170, 13934, 42954, 42129, 30071, 9363, 9150, 48823, 36789, 38311, 28077, 23723, 10484, 51909, 44596, 25009, 30674, 34676, 44583, 7507, 35190, 49209, 50370, 42006, 7310, 10365, 212, 47323,]
#IDX_OFFSET = 187
#"""
ADD = True

if ADD:
    with open(path, "r") as f:
        lines = f.readlines()
        lines_chosen = [lines[i] for i in INDICES]
    with open(f"oasstcommitpackftmanual.jsonl", "a") as f:
        for l in lines_chosen:
            l = json.loads(l)
            data = {
                "prompt": l["subject"] + "\n" + l["old_contents"],
                "completion": l["new_contents"],
            }
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    exit()


with open(path, "r") as f:
    # c = [json.loads(l) for l in f.readlines()]
    # Collect indices that are OK
    lines = f.readlines()
    lines_shuffled = random.sample(lines, len(lines))
    for j, l in enumerate(lines_shuffled):
        if j < IDX_OFFSET: continue
        i = lines.index(l)
        data = json.loads(l)
        print(data["subject"])
        is_ok = input("Is this OK? [y/n]") # n to break out; just enter for no
        if is_ok == "y":
            INDICES.append(i)
        elif is_ok == "n":
            print("Breaking at index {}".format(j))
            break

print(INDICES)
print("Samples: ", len(INDICES))


