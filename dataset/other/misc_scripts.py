import json
import random
import os
import datasets

NUM_PROC = 16

opt_out_github_login_the_stack_12 = '''tomas
bermannoah
rtzoeller
sdatkinson
jtth
benui-dev
DrTimothyAldenDavis
pranftw
marcsances
sitmo
jucor
digantamisra98
przemb
jisakiel
kellycochran
AkashM398
MeSayan
SWinxy
zitterbewegung
fredster33
demangejeremy
PPPI
henilp105
tobymcclean
cynddl
spate141
plaaosert
woylie
alexkoster
satyrnidae
rclark
zakkolar
jimscard
marjoleinF
ghchinoy
jmfadeley
fuhrmanator
stephen-three
retro-ai
abolouri
matthewheath
jollypolly123
RJRauch
ivansche
'''.splitlines()

paths = '''diffs_10485761_11010048.jsonl
diffs_1048577_1572864.jsonl
diffs_11010049_11534336.jsonl
diffs_11534337_12058624.jsonl
diffs_12058625_12582912.jsonl
diffs_12582913_13107200.jsonl
diffs_13107201_13631488.jsonl
diffs_13631489_14155776.jsonl
diffs_14155777_14680064.jsonl
diffs_14680065_15204352.jsonl
diffs_15204353_15728640.jsonl
diffs_15728641_16252928.jsonl
diffs_1572865_2097152.jsonl
diffs_16252929_16777216.jsonl
diffs_1_524288.jsonl
diffs_2097153_2621440.jsonl
diffs_25165825_25690112.jsonl
diffs_25690113_26214400.jsonl
diffs_26214401_26738688.jsonl
diffs_2621441_3145728.jsonl
diffs_26738689_27262976.jsonl
diffs_27262977_27787264.jsonl
diffs_27787265_28311552.jsonl
diffs_28311553_28835840.jsonl
diffs_28835841_29360128.jsonl
diffs_29360129_29884416.jsonl
diffs_29884417_30408704.jsonl
diffs_30408705_30932992.jsonl
diffs_30932993_31457280.jsonl
diffs_31457281_31981568.jsonl
diffs_3145729_3670016.jsonl
diffs_31981569_32505856.jsonl
diffs_32505857_33030144.jsonl
diffs_33030145_33554432.jsonl
diffs_33554433_34078720.jsonl
diffs_34078721_34603008.jsonl
diffs_34603009_35127296.jsonl
diffs_35127297_35651584.jsonl
diffs_35651585_36175872.jsonl
diffs_36175873_36700160.jsonl
diffs_36700161_37224448.jsonl
diffs_3670017_4194304.jsonl
diffs_37224449_37748736.jsonl
diffs_37748737_38273024.jsonl
diffs_38273025_38797312.jsonl
diffs_38797313_39321600.jsonl
diffs_39321601_39845888.jsonl
diffs_39845889_40370176.jsonl
diffs_40370177_40894464.jsonl
diffs_40894465_41418752.jsonl
diffs_41418753_41943040.jsonl
diffs_41943041_42467328.jsonl
diffs_4194305_4718592.jsonl
diffs_42467329_42991616.jsonl
diffs_42991617_43515904.jsonl
diffs_43515905_44040192.jsonl
diffs_44040193_44564480.jsonl
diffs_44564481_45088768.jsonl
diffs_45088769_45613056.jsonl
diffs_45613057_46137344.jsonl
diffs_46137345_46661632.jsonl
diffs_46661633_47185920.jsonl
diffs_47185921_47710208.jsonl
diffs_4718593_5242880.jsonl
diffs_47710209_48234496.jsonl
diffs_48234497_48758784.jsonl
diffs_48758785_49283072.jsonl
diffs_49283073_49807360.jsonl
diffs_49807361_50331648.jsonl
diffs_50331649_50855936.jsonl
diffs_50855937_51380224.jsonl
diffs_51380225_51904512.jsonl
diffs_51904513_52428800.jsonl
diffs_52428801_52953088.jsonl
diffs_5242881_5767168.jsonl
diffs_524289_1048576.jsonl
diffs_52953089_53477376.jsonl
diffs_53477377_54001664.jsonl
diffs_54001665_54525952.jsonl
diffs_54525953_55050240.jsonl
diffs_55050241_55574528.jsonl
diffs_55574529_56098816.jsonl
diffs_56098817_56623104.jsonl
diffs_56623105_57147392.jsonl
diffs_57147393_57671680.jsonl
diffs_57671681_58195968.jsonl
diffs_5767169_6291456.jsonl
diffs_58195969_58720256.jsonl
diffs_49807361_50331648.jsonl
diffs_50331649_50855936.jsonl
diffs_50855937_51380224.jsonl
diffs_51380225_51904512.jsonl
diffs_51904513_52428800.jsonl
diffs_52428801_52953088.jsonl
diffs_5242881_5767168.jsonl
diffs_524289_1048576.jsonl
diffs_52953089_53477376.jsonl
diffs_53477377_54001664.jsonl
diffs_54001665_54525952.jsonl
diffs_54525953_55050240.jsonl
diffs_55050241_55574528.jsonl
diffs_55574529_56098816.jsonl
diffs_56098817_56623104.jsonl
diffs_56623105_57147392.jsonl
diffs_57147393_57671680.jsonl
diffs_57671681_58195968.jsonl
diffs_5767169_6291456.jsonl
diffs_58195969_58720256.jsonl
diffs_58720257_59244544.jsonl
diffs_59244545_59768832.jsonl
diffs_59768833_60293120.jsonl
diffs_60293121_60817408.jsonl
diffs_60817409_61341696.jsonl
diffs_61341697_61865984.jsonl
diffs_61865985_62390272.jsonl
diffs_62390273_62914560.jsonl
diffs_62914561_63438848.jsonl
diffs_6291457_6815744.jsonl
diffs_63438849_63963136.jsonl
diffs_63963137_64487424.jsonl
diffs_64487425_65011712.jsonl
diffs_65011713_65536000.jsonl
diffs_65536001_66060288.jsonl
diffs_66060289_66584576.jsonl
diffs_66584577_67108864.jsonl
diffs_6815745_7340032.jsonl
diffs_7340033_7864320.jsonl
diffs_7864321_8388608.jsonl
diffs_8388609_8912896.jsonl
diffs_8912897_9437184.jsonl
diffs_9437185_9961472.jsonl'''.splitlines()

paths="""diffs_1048577_1572864.jsonl
diffs_1572865_2097152.jsonl
diffs_1_524288.jsonl
diffs_2097153_2621440.jsonl
diffs_2621441_3145728.jsonl
diffs_3145729_3670016.jsonl
diffs_3670017_4194304.jsonl
diffs_4194305_4718592.jsonl
diffs_4718593_5242880.jsonl
diffs_5242881_5767168.jsonl
diffs_524289_1048576.jsonl
diffs_5767169_6291456.jsonl
diffs_6291457_6815744.jsonl
diffs_6815745_7340032.jsonl
diffs_7340033_7864320.jsonl
diffs_7864321_8388608.jsonl""".splitlines()

paths="""diffs_10485761_11010048.jsonl
diffs_1048577_1572864.jsonl
diffs_11010049_11534336.jsonl
diffs_11534337_12058624.jsonl
diffs_12058625_12582912.jsonl
diffs_12582913_13107200.jsonl
diffs_13107201_13631488.jsonl
diffs_13631489_14155776.jsonl
diffs_14155777_14680064.jsonl
diffs_14680065_15204352.jsonl
diffs_15204353_15728640.jsonl
diffs_15728641_16252928.jsonl
diffs_1572865_2097152.jsonl
diffs_16252929_16777216.jsonl
diffs_1_524288.jsonl
diffs_2097153_2621440.jsonl
diffs_25165825_25690112.jsonl
diffs_25690113_26214400.jsonl
diffs_26214401_26738688.jsonl
diffs_2621441_3145728.jsonl
diffs_26738689_27262976.jsonl
diffs_27262977_27787264.jsonl
diffs_27787265_28311552.jsonl
diffs_28311553_28835840.jsonl
diffs_28835841_29360128.jsonl
diffs_29360129_29884416.jsonl
diffs_29884417_30408704.jsonl
diffs_30408705_30932992.jsonl
diffs_30932993_31457280.jsonl
diffs_31457281_31981568.jsonl
diffs_3145729_3670016.jsonl
diffs_31981569_32505856.jsonl
diffs_32505857_33030144.jsonl
diffs_33030145_33554432.jsonl
diffs_33554433_34078720.jsonl
diffs_34078721_34603008.jsonl
diffs_34603009_35127296.jsonl
diffs_35127297_35651584.jsonl
diffs_35651585_36175872.jsonl
diffs_36175873_36700160.jsonl
diffs_36700161_37224448.jsonl
diffs_3670017_4194304.jsonl
diffs_37224449_37748736.jsonl
diffs_37748737_38273024.jsonl
diffs_48234497_48758784.jsonl
diffs_48758785_49283072.jsonl
diffs_49283073_49807360.jsonl
diffs_49807361_50331648.jsonl
diffs_50331649_50855936.jsonl
diffs_50855937_51380224.jsonl
diffs_51380225_51904512.jsonl
diffs_51904513_52428800.jsonl
diffs_52428801_52953088.jsonl
diffs_5242881_5767168.jsonl
diffs_524289_1048576.jsonl
diffs_52953089_53477376.jsonl
diffs_53477377_54001664.jsonl
diffs_54001665_54525952.jsonl
diffs_54525953_55050240.jsonl
diffs_55050241_55574528.jsonl
diffs_55574529_56098816.jsonl
diffs_56098817_56623104.jsonl
diffs_56623105_57147392.jsonl
diffs_57147393_57671680.jsonl
diffs_57671681_58195968.jsonl
diffs_5767169_6291456.jsonl
diffs_58195969_58720256.jsonl
diffs_58720257_59244544.jsonl
diffs_59244545_59768832.jsonl
diffs_59768833_60293120.jsonl
diffs_60293121_60817408.jsonl
diffs_60817409_61341696.jsonl
diffs_61341697_61865984.jsonl
diffs_61865985_62390272.jsonl
diffs_62390273_62914560.jsonl
diffs_62914561_63438848.jsonl
diffs_6291457_6815744.jsonl
diffs_63438849_63963136.jsonl
diffs_63963137_64487424.jsonl
diffs_64487425_65011712.jsonl
diffs_65011713_65536000.jsonl
diffs_65536001_66060288.jsonl
diffs_66060289_66584576.jsonl
diffs_66584577_67108864.jsonl
diffs_6815745_7340032.jsonl
diffs_7340033_7864320.jsonl
diffs_7864321_8388608.jsonl
diffs_8388609_8912896.jsonl
diffs_8912897_9437184.jsonl
diffs_9437185_9961472.jsonl
diffs_9961473_10485760.jsonl""".splitlines()

paths = ['diffs_42991617_43515904.jsonl', 'diffs_47185921_47710208.jsonl', 'diffs_4194305_4718592.jsonl', 'diffs_45613057_46137344.jsonl', 'diffs_42467329_42991616.jsonl',
'diffs_4718593_5242880.jsonl', 'diffs_40370177_40894464.jsonl', 'diffs_38797313_39321600.jsonl', 'diffs_44040193_44564480.jsonl', 'diffs_45088769_45613056.jsonl', 'diffs_47710209_48234496.jsonl',
'diffs_41418753_41943040.jsonl', 'diffs_43515905_44040192.jsonl', 'diffs_39845889_40370176.jsonl', 'diffs_46661633_47185920.jsonl', 'diffs_39321601_39845888.jsonl', 'diffs_40894465_41418752.jsonl',
'diffs_41943041_42467328.jsonl', 'diffs_38273025_38797312.jsonl', 'diffs_46137345_46661632.jsonl']

if __name__ == "__main__":

    with open("programming_languages.json", "r") as f:
        prog_langs = json.load(f)
    
    ext_to_lang = {}
    for lang, exts in prog_langs.items():
        for ext in exts:
            ext_to_lang[ext] = lang
    
    for path in paths:
        with open(path, 'r') as f:
            first_line = f.readline()
            if '"lang":' in first_line:
                continue    
        ds = datasets.load_dataset("json", data_files=path)

        def add_lang(example):
            ext = example["new_file"].split("/")[-1].split(".")[-1]
            if "." in example["new_file"]:
                ext = "." + ext
            example["lang"] = ext_to_lang.get(ext, "unknown")
            return example

        ds['train'].map(add_lang).to_json(path.replace(".jsonl", "_new.jsonl"), num_proc=NUM_PROC)


if False:#__name__ == "__main__":
    data = {}
    # licenses:
    # {"repos":"samoht/ocaml-conduit,samoht/ocaml-conduit,avsm/ocaml-conduit,mirage/ocaml-conduit,djs55/ocaml-conduit,rgrinberg/ocaml-conduit,rgrinberg/ocaml-conduit,djs55/ocaml-conduit","license":"isc"}
    with open('licenses_merged.jsonl', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            for repo in d['repos'].split(","):
                data[repo] = d['license']


    # path = "diffs_9961473_10485760.jsonl"
    for path in paths:
        # Check if "license" is already in the dataset
        # Do so by simply checking if it's in the first line of the jsonl file at path
        with open(path, 'r') as f:
            first_line = f.readline()
            if '"license":' in first_line:
                continue

        ds = datasets.load_dataset("json", data_files=path)

        print(ds)
        print(random.sample(data.items(), 10))

        def map_col(example):
            for repo in example["repos"].split(","):
                if repo in data:
                    example["license"] = data[repo]
                    return example
            example["license"] = 'unknown'
            return example

        def opt_out(example):
            repos = example["repos"].split(",")
            if (len(repos) == 1) and (repos[0].split("/")[0] in opt_out_github_login_the_stack_12):
                return False
            return True
        
        ds['train'].map(map_col).filter(opt_out).to_json(path.replace(".jsonl", "_new.jsonl"), num_proc=NUM_PROC)

"""
  AND ( (lang_table.language_name LIKE 'Python')
    OR (lang_table.language_name LIKE 'Java')
    OR (lang_table.language_name LIKE 'JavaScript')
    OR (lang_table.language_name LIKE 'HTML')
    OR (lang_table.language_name LIKE 'Common Lisp')
    OR (lang_table.language_name LIKE 'Shell')
    OR (lang_table.language_name LIKE 'R')
    OR (lang_table.language_name LIKE 'Perl%')
    OR (lang_table.language_name LIKE 'SQL')
    OR (lang_table.language_name LIKE 'C')
    OR (lang_table.language_name LIKE 'C#')
    OR (lang_table.language_name LIKE 'C++')
    OR (lang_table.language_name LIKE 'TypeScript')
    OR (lang_table.language_name LIKE 'Go')
    OR (lang_table.language_name LIKE 'Rust')
    OR (lang_table.language_name LIKE 'Swift')
    OR (lang_table.language_name LIKE 'PHP')
    OR (lang_table.language_name LIKE 'Dart')
    OR (lang_table.language_name LIKE 'Kotlin')
    OR (lang_table.language_name LIKE 'Matlab')
    OR (lang_table.language_name LIKE 'MATLAB')
    OR (lang_table.language_name LIKE 'Ruby') )
"""

if False:#__name__ == "__main__":

    with open("programming_languages.json", "r") as f:
        prog_langs = json.load(f)
    
    ext_to_lang = {}
    for lang, exts in prog_langs.items():
        for ext in exts:
            ext_to_lang[ext] = lang
    
    LANGS = [
        'Python',
        'Java',
        'JavaScript',
        'HTML',
        'Common Lisp',
        'Shell',
        'R',
        'Perl',
        'Perl6', # Differentiate Perl6 from Perl
        'SQL',
        'C',
        'C#',
        'C++',
        'TypeScript',
        'Go',
        'Rust',
        'Swift',
        'PHP',
        'Dart',
        'Kotlin',
        'Matlab',
        'MATLAB',
        'Ruby'
    ]

    for lang in LANGS:
        if lang not in prog_langs:
            print("Missing", lang)

    def add_lang(example):
        ext = example["new_file"].split("/")[-1].split(".")[-1]
        if "." in example["new_file"]:
            ext = "." + ext
        example["language"] = ext_to_lang.get(ext, "unknown")
        return example

    #for path in paths:
    #    ds = datasets.load_dataset("json", data_files=path)
    #    ds = ds['train'].map(add_lang)
    #    langs = ds.unique('language')
    #    for lang in langs:
    #        ds.filter(lambda x: x['language'] == lang).to_json(path.replace(".jsonl", f"_{lang}.jsonl"), num_proc=NUM_PROC)

    ds = datasets.load_dataset("json", data_files=paths)
    ds = ds['train'].map(add_lang)
    langs = ds.unique('language')
    for lang in langs:
        os.makedirs(lang, exist_ok=True)
        ds.filter(lambda x: x['language'] == lang).to_json(f"{lang}/data.jsonl", num_proc=NUM_PROC)


if False:#__name__ == "__main__":
    data = {}
    # licenses:
    # {"repos":"samoht/ocaml-conduit,samoht/ocaml-conduit,avsm/ocaml-conduit,mirage/ocaml-conduit,djs55/ocaml-conduit,rgrinberg/ocaml-conduit,rgrinberg/ocaml-conduit,djs55/ocaml-conduit","license":"isc"}
    with open('licenses_merged.jsonl', 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            d = json.loads(line)
            for repo in d['repos'].split(","):
                name, _ = repo.split("/")
                data.setdefault(name, set())
                data[name].add(repo)
    # Save to json
    with open('username_to_repo.json', 'w') as f:
        json.dump(data, f)


if False:#__name__ == "__main__":

    with open("programming_languages.json", "r") as f:
        prog_langs = json.load(f)

    ds = datasets.load_dataset("json", data_files=paths, ignore_verifications=True)
    for lang in prog_langs:
        os.makedirs(lang, exist_ok=True)
        ds.filter(lambda x: x['language'] == lang).to_json(f"{lang}/data.jsonl", num_proc=NUM_PROC)

import multiprocessing as mp
if False:#__name__ == "__main__":
    ds = datasets.load_dataset("json", data_files=paths, ignore_verifications=True)["train"]
    locks = {lang: mp.Lock() for lang in ds.unique("lang")}  # create a lock for each output file
    def add_lines(row):
        # row is a dict
        lang = row["lang"]
        with locks[lang]:
            with open(f"out/{lang}.jsonl", "a") as f:
                json.dump(dict(row), f)
                f.write("\n")  # add newline after each JSON object

    num_proc = 64 # number of processes to use
    ds.map(add_lines, num_proc=num_proc)


