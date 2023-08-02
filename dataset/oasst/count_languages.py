"""
To count languages for OASST, use this script and run e.g.
python count_languages.py ../../../../Downloads/oasst_octopack.jsonl
python count_languages.py ../../../../Downloads/2023-04-12_oasst_all.messages.jsonl


To count languages for the self-instruct-starcoder dataset:

git clone https://huggingface.co/datasets/codeparrot/self-instruct-starcoder
from datasets import load_dataset; ds = load_dataset("./self-instruct-starcoder", "raw")
dsin = ds["raw"].select_columns("instruction")
dsin.to_json("./raw.jsonl")
Manually searching through the jsonl:

Python: 798
python: 595

C++: 33
c++: 2

SQL: 26
sql: 7

Java 25
java: 4

HTML: 20

JavaScript: 15
javascript: 2
Javascript: 2

GoLang: 5

PHP: 13

Shell: 2

Bash: 2

Rust: 1

C#: 1
"""
import json
import sys

# Manually checked for good samples
INDICES = [0, 1, 2, 3, 4, 6, 7, 9, 10, 15, 16, 19, 21, 24, 25, 27, 28, 29, 33, 36, 38, 39, 40, 41, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56, 57, 61, 63, 64, 67, 72, 73, 74, 77, 80, 81, 83, 84, 85, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 105, 108, 109, 110, 111, 115, 116, 117, 118, 120, 123, 124, 126, 129, 130, 132, 134, 136, 137, 138, 144, 145, 146, 148, 156, 157, 158, 160, 162, 165, 169, 170, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 198, 199, 200, 201, 202, 203, 212, 213, 214, 215, 216, 220, 221, 222, 223, 227, 230, 231, 232, 233, 235, 239, 240, 241, 244, 246, 250, 253, 257, 259, 261, 262, 267, 268, 269, 270, 274, 275, 276, 277, 279, 280, 281, 283, 284, 285, 286, 287, 291, 294, 298, 302, 305, 308, 313, 316, 331, 333, 335, 337, 345, 347, 357, 358, 360, 363, 367, 368, 370, 371, 372, 375, 376, 377, 384, 389, 391, 393, 394, 395, 403, 405, 407, 408, 417, 419, 440, 441, 442, 443, 450, 453, 456, 457, 478, 479, 485, 492, 499, 526, 532, 533, 534, 535, 536, 538, 539, 541, 544, 545, 546, 550, 551, 562, 567, 575, 576, 591, 597, 601, 605, 616, 625, 632, 638, 640, 643, 651, 661, 666, 667, 670, 704, 707, 708, 710, 715, 721, 723, 732, 756, 780, 802, 812, 853, 873, 884, 898, 904, 978, 979, 986, 997, 1020, 1021, 1044, 1058, 1067, 1077, 1082, 1088, 1126, 1137, 1155, 1159, 1190, 1196, 1198, 1200, 1204, 1209, 1210, 1229, 1230, 1254, 1261, 1264, 1268, 1273, 1330, 1345, 1348, 1352, 1364, 1372, 1377, 1396, 1421, 1423, 1454, 1471, 1472, 1474, 1485, 1492, 1518, 1521, 1525, 1535, 1536, 1547, 1552, 1554, 1557, 1566, 1569, 1586, 1588, 1635, 1637, 1642, 1643, 1648, 1651, 1658, 1670, 1681, 1692, 1711, 1712, 1724, 1734, 1742, 1753, 1754, 1765, 1766, 1782, 1783, 1800, 1803, 1816, 1820, 1823, 1826, 1834, 1835, 1837, 1843, 1850, 1865, 1874, 1881, 1884, 1888, 1889, 1890, 1891, 1892, 1893, 1898, 1900, 1901, 1904, 1914, 1920, 1928, 1929, 1933, 1938, 1939, 1943, 1944, 1946, 1949, 1951, 1957, 1960, 1961, 1965, 1968, 1980, 1992, 1995, 2002, 2004, 2012, 2017, 2020, 2029, 2035, 2037, 2038, 2047, 2049, 2055, 2056, 2059, 2061, 2066, 2085, 2086, 2089, 2093, 2094, 2097, 2098, 2100, 2102, 2111, 2112, 2113, 2124, 2126, 2149, 2153, 2155, 2157, 2158, 2164, 2165, 2176, 2177, 2178, 2181, 2190, 2199, 2200, 2201, 2208, 2214, 2216, 2223, 2226, 2231, 2234, 2240, 2246, 2259, 2261, 2262, 2264, 2265, 2271, 2275, 2279, 2288, 2290, 2295, 2298, 2306, 2307, 2308, 2310, 2311, 2312, 2321, 2334, 2338, 2340, 2341, 2344, 2345, 2346, 2347, 2358, 2376, 2382, 2384, 2388, 2391, 2394, 2395, 2397, 2400, 2405, 2408, 2410, 2412, 2419, 2425, 2428, 2432, 2433, 2434, 2437, 2453, 2454, 2465, 2469, 2474, 2476, 2481, 2486, 2487, 2498, 2501, 2505, 2512, 2514, 2518, 2519, 2525, 2526, 2528, 2530, 2531, 2539, 2540]
CHECK = False

oasstjsonl = sys.argv[1]
data = [] # Format: [assistant text, ...]

LIST_FORMAT = False
SAVE_TO_NEW_FILE = False

if SAVE_TO_NEW_FILE:
    data_original = []

if LIST_FORMAT:
    # python count_languages.py ../../../../Downloads/oasst_octopack.jsonl
    # https://huggingface.co/datasets/Muennighoff/oasst-octopack
    '''Format:
    [{"text": "¿Qué es una escala de blues?", "from": "user", "parent_id": null, "message_id": -7073520377949179376}, {"text": "La escala de blues es una escala musical que se utiliza en el género del blues y en otros géneros relacionados. Es una escala pentatónica con cinco notas, que se utiliza para crear melodías y acordes. La escala de blues se caracteriza por una sensación de tristeza y melancolía y se puede usar para crear una amplia variedad de tonos, desde el humor hasta la intensidad emocional.\n\nLas notas de la escala de blues son las siguientes: tono mayor, semitono menor, tono mayor, tono mayor y semitono menor. Estas notas pueden variar en función de la tonalidad en la que se encuentre la canción, pero la estructura básica de la escala de blues se mantiene.\n\nLa escala de blues se utiliza comúnmente en la improvisación musical y en la creación de solos de guitarra, y es un componente clave de la música blues. También se puede utilizar en otros géneros, como el rock, el jazz y el soul, y es una herramienta importante para los músicos que buscan crear una atmósfera específica en su música.", "from": "assistant", "parent_id": -7073520377949179376, "message_id": -788610489460529539}]
    [{"text": "Please suggest three useful applications that can be achieved using autohotkey and irfanview.", "from": "user", "parent_id": null, "message_id": 1047855468874266046}, {"text": "AutoHotkey is a free and open-source scripting language that allows users to automate repetitive tasks and customize their desktops. IrfanView is a lightweight and fast image viewer and editor that supports a wide range of formats. Here are three useful applications that can be achieved by combining AutoHotkey and IrfanView:\n\n1. Batch image editing: With AutoHotkey, you can create scripts to automate repetitive image editing tasks in IrfanView. For example, you can write a script that renames a group of files, converts them to a specific format, and applies a set of filters to each image. This can save a lot of time for photographers, graphic designers, and other professionals who work with large numbers of images.\n2. Screen capture and editing: AutoHotkey can be used to create custom keyboard shortcuts for capturing screenshots with IrfanView. Once the screenshot is captured, you can use IrfanView's built-in editing tools to crop, resize, or annotate the image. This can be especially useful for creating tutorials, documentation, or social media content.\n3. Image slideshow and presentation: AutoHotkey can be used to create custom scripts for controlling IrfanView's slideshow and presentation modes. For example, you can write a script that automatically plays a slideshow of images in a specific folder, with a specific transition effect and time interval. This can be useful for creating digital signage, presentations, or exhibitions.\n\nThese are just a few examples of the many applications that can be achieved with AutoHotkey and IrfanView. The possibilities are endless, and the best way to learn is by experimenting with the tools and exploring the many online resources available for both programs.", "from": "assistant", "parent_id": 1047855468874266046, "message_id": 3502446468537680109}, {"text": "Can you give me a specific example of how to do one of the above?", "from": "user", "parent_id": 3502446468537680109, "message_id": 5287513724223611599}, {"text": "Sure! Here's an example of how to use AutoHotkey and IrfanView for batch image editing:\n\nLet's say you have a folder with a hundred images that you need to resize, add a border, and save as a different file format. You can use AutoHotkey to automate this process in IrfanView with just a few lines of code:\n\nsql\nCopy code\n; Set the path to the folder containing the images\nImagePath := \"C:\\Images\"\n\n; Set the target file format and quality\nFormat := \"JPG\"\nQuality := 80\n\n; Set the target image dimensions and border size\nWidth := 800\nHeight := 600\nBorderSize := 10\n\n; Loop through each file in the folder and apply the editing\nLoop, %ImagePath%\\*.jpg\n{\n    ; Get the filename and extension of the current file\n    SplitPath, A_LoopFileFullPath, FileName, Extension\n\n    ; Open the image in IrfanView\n    Run, \"C:\\Program Files\\IrfanView\\i_view64.exe\" \"%A_LoopFileFullPath%\"\n\n    ; Resize the image\n    WinWaitActive, %FileName% - IrfanView\n    Send, ^r\n    WinWaitActive, Resize/Resample\n    Send, %Width% x %Height%\n    Send, {Enter}\n\n    ; Add a border\n    WinWaitActive, %FileName% - IrfanView\n    Send, ^b\n    WinWaitActive, Add border\n    Send, %BorderSize%\n    Send, {Enter}\n\n    ; Save the edited image\n    WinWaitActive, %FileName% - IrfanView\n    Send, ^s\n    WinWaitActive, Save as\n    Send, %ImagePath%\\%FileName%.%Format%\n    Send, {Enter}\n    Send, {Enter}\n\n    ; Close the image\n    WinWaitActive, %FileName% - IrfanView\n    Send, ^q\n}\n\n; Display a message when the editing is complete\nMsgBox, % \"Batch editing is complete!\"\nThis code uses a loop to go through each image in the folder and perform the editing steps one by one. It opens each image in IrfanView, resizes it, adds a border, and saves it as a JPG file with the specified dimensions and quality. Once all the images are processed, a message box is displayed to notify you that the batch editing is complete.\n\nOf course, this is just one example, and you can customize the code to suit your specific needs. With AutoHotkey and IrfanView, the possibilities for batch image editing are endless!", "from": "assistant", "parent_id": 5287513724223611599, "message_id": 8906576197775372008}]
    '''
    with open(oasstjsonl, "r") as f:
        # Load only the first two turns for each line & only the text
        for line in f.readlines():
            line = json.loads(line)
            data.append(line[1]["text"])
            if SAVE_TO_NEW_FILE:
                data_original.append(line)
else:
    # python count_languages.py ../../../../Downloads/2023-04-12_oasst_all.messages.jsonl
    # https://huggingface.co/datasets/OpenAssistant/oasst1/resolve/main/2023-04-12_oasst_all.messages.jsonl.gz
    '''Format:
    {"message_id": "c8e83833-ecbc-44fe-b6db-735228c25a1c", "parent_id": "6ab24d72-0181-4594-a9cd-deaf170242fb", "user_id": "2c96e467-66f0-4be7-9693-bda51356a424", "created_date": "2023-02-06T13:50:44.657083+00:00", "text": "\"Monopsony\" refers to a market structure where there is only one buyer for a particular good or service. In economics, this term is particularly relevant in the labor market, where a monopsony employer has significant power over the wages and working conditions of their employees. The presence of a monopsony can result in lower wages and reduced employment opportunities for workers, as the employer has little incentive to increase wages or provide better working conditions.\n\nRecent research has identified potential monopsonies in industries such as retail and fast food, where a few large companies control a significant portion of the market (Bivens & Mishel, 2013). In these industries, workers often face low wages, limited benefits, and reduced bargaining power, leading to a situation where they are dependent on the employer for their livelihood. This dependence can result in further suppression of wages and a decline in working conditions.\n\nOverall, the concept of monopsony is essential to understanding the dynamics of labor markets and the impact of market power on workers. Further research is needed to understand the extent and impact of monopsonies on the economy and to develop policies to address this issue.\n\nReferences:\nBivens, J., & Mishel, L. (2013). The Pay of Corporate Executives and Financial Professionals as Evidence of Rents in Top 1 Percent Incomes. Journal of Economic Perspectives, 27(3), 57-78.", "role": "assistant", "lang": "en", "review_count": 3, "review_result": true, "deleted": false, "rank": 0, "synthetic": false, "emojis": {"+1": 3, "_skip_labeling": 1}, "labels": {"spam": {"value": 0.0, "count": 3}, "fails_task": {"value": 0.0, "count": 2}, "lang_mismatch": {"value": 0.0, "count": 3}, "pii": {"value": 0.0, "count": 2}, "not_appropriate": {"value": 0.0, "count": 2}, "hate_speech": {"value": 0.0, "count": 2}, "sexual_content": {"value": 0.0, "count": 2}, "quality": {"value": 0.9166666666666666, "count": 3}, "toxicity": {"value": 0.375, "count": 2}, "humor": {"value": 0.375, "count": 2}, "helpfulness": {"value": 0.75, "count": 2}, "creativity": {"value": 0.375, "count": 2}, "violence": {"value": 0.0, "count": 2}}, "detoxify": {"toxicity": 0.00026396565954200923, "severe_toxicity": 2.7454958399175666e-05, "obscene": 0.00013584605767391622, "identity_attack": 9.263094398193061e-05, "insult": 0.0001668655313551426, "threat": 3.769186878344044e-05, "sexual_explicit": 2.500762275303714e-05}, "message_tree_id": "6ab24d72-0181-4594-a9cd-deaf170242fb", "tree_state": "ready_for_export"}
    '''
    with open(oasstjsonl, "r") as f:
        # Load only the first two turns for each line & only the text
        for line in f.readlines():
            line = json.loads(line)
            data.append(line["text"])

with open("../commitpack/programming_languages.json", "r") as f:
    prog_langs = json.load(f)

prog_langs = [lang.lower() for lang in prog_langs]



SHORTCUT_TO_LANG = {
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "c": "c",
    "rs": "rust",
    "vb": "visual basic",
    "sh": "shell",
    "bash": "shell",
    "zsh": "shell",
    "latex": "tex",
    "cpp": "c++",
    "csharp": "c#",
    "terminal": "shell",
    "hs": "haskell",
    "tsx": "typescript",
    "jsx": "javascript",
    "md": "markdown",
    "delphi": "pascal",
    "vbscript": "visual basic",
    "gradle": "groovy",
    "vba": "visual basic",
    "vbnet": "visual basic",
    "vim": "viml",
    "txt": "text",
    "nim": "nimrod",
    "cs": "c#",
    "wolfram": "mathematica",
    "basic": "visual basic",
    "git": "shell",
    "asm": "assembly",
}

print("Example")
print(data[0])

def get_code(text):
    first_backticks = text.find("```") # First backticks
    if first_backticks == -1:
        # No backticks
        return False
    # Get the programming language e.g. ....\n```python\n...
    lang = text[first_backticks + 3 : text.find("\n", first_backticks + 3)].strip().lower()
    if (not(lang)) or (len(lang) > 20) or ("*" in lang) or ("{" in lang) or ("}" in lang) or ("`" in lang) or (":" in lang) or ("\\" in lang) or ("." in lang) or (lang.startswith(("import ", "let ", "pythonimport", "using ", ")", "<", "html<", "type="))):
        # Probably not a programming language
        return False
    if lang in SHORTCUT_TO_LANG:
        lang = SHORTCUT_TO_LANG[lang]
    if lang not in prog_langs:
        # Not a programming language
        print(lang)
        return False
    return lang

lang_counts = {}
for i, assistant in enumerate(data):
    lang = get_code(assistant)
    if lang:
        if lang in lang_counts:
            lang_counts[lang] += 1
        else:
            lang_counts[lang] = 1
        if SAVE_TO_NEW_FILE:
            data = {
                "prompt": data_original[i][0]["text"],
                "completion": assistant,
            }
            with open(f"oasstcommitpackftmanual.jsonl", "a") as f:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
    elif CHECK:
        if i <= INDICES[-1]:
            continue
        # Check if okay
        print("-"*50)
        print(assistant)
        print("-"*50)
        is_ok = input("Is this OK? [y/n]") # n to break out; just enter for no
        if is_ok == "n":
            break
        elif is_ok == "y":
            INDICES.append(i)
    elif (SAVE_TO_NEW_FILE) and (i in INDICES):
        data = {
            "prompt": data_original[i][0]["text"],
            "completion": assistant,
        }
        with open(f"oasstcommitpackftmanual.jsonl", "a") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")


print(sorted(lang_counts.items(), key=lambda x: x[1], reverse=True))
print("Num prgramming languages: ", len(lang_counts))
print("Num prgramming samples: ", sum(lang_counts.values()))
print(INDICES)
print("Samples: ", len(INDICES))