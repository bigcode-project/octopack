import ast
import json
import sys

oasstjsonl = sys.argv[1]
'''Format:
[{"text": "¿Qué es una escala de blues?", "from": "user", "parent_id": null, "message_id": -7073520377949179376}, {"text": "La escala de blues es una escala musical que se utiliza en el género del blues y en otros géneros relacionados. Es una escala pentatónica con cinco notas, que se utiliza para crear melodías y acordes. La escala de blues se caracteriza por una sensación de tristeza y melancolía y se puede usar para crear una amplia variedad de tonos, desde el humor hasta la intensidad emocional.\n\nLas notas de la escala de blues son las siguientes: tono mayor, semitono menor, tono mayor, tono mayor y semitono menor. Estas notas pueden variar en función de la tonalidad en la que se encuentre la canción, pero la estructura básica de la escala de blues se mantiene.\n\nLa escala de blues se utiliza comúnmente en la improvisación musical y en la creación de solos de guitarra, y es un componente clave de la música blues. También se puede utilizar en otros géneros, como el rock, el jazz y el soul, y es una herramienta importante para los músicos que buscan crear una atmósfera específica en su música.", "from": "assistant", "parent_id": -7073520377949179376, "message_id": -788610489460529539}]
[{"text": "Please suggest three useful applications that can be achieved using autohotkey and irfanview.", "from": "user", "parent_id": null, "message_id": 1047855468874266046}, {"text": "AutoHotkey is a free and open-source scripting language that allows users to automate repetitive tasks and customize their desktops. IrfanView is a lightweight and fast image viewer and editor that supports a wide range of formats. Here are three useful applications that can be achieved by combining AutoHotkey and IrfanView:\n\n1. Batch image editing: With AutoHotkey, you can create scripts to automate repetitive image editing tasks in IrfanView. For example, you can write a script that renames a group of files, converts them to a specific format, and applies a set of filters to each image. This can save a lot of time for photographers, graphic designers, and other professionals who work with large numbers of images.\n2. Screen capture and editing: AutoHotkey can be used to create custom keyboard shortcuts for capturing screenshots with IrfanView. Once the screenshot is captured, you can use IrfanView's built-in editing tools to crop, resize, or annotate the image. This can be especially useful for creating tutorials, documentation, or social media content.\n3. Image slideshow and presentation: AutoHotkey can be used to create custom scripts for controlling IrfanView's slideshow and presentation modes. For example, you can write a script that automatically plays a slideshow of images in a specific folder, with a specific transition effect and time interval. This can be useful for creating digital signage, presentations, or exhibitions.\n\nThese are just a few examples of the many applications that can be achieved with AutoHotkey and IrfanView. The possibilities are endless, and the best way to learn is by experimenting with the tools and exploring the many online resources available for both programs.", "from": "assistant", "parent_id": 1047855468874266046, "message_id": 3502446468537680109}, {"text": "Can you give me a specific example of how to do one of the above?", "from": "user", "parent_id": 3502446468537680109, "message_id": 5287513724223611599}, {"text": "Sure! Here's an example of how to use AutoHotkey and IrfanView for batch image editing:\n\nLet's say you have a folder with a hundred images that you need to resize, add a border, and save as a different file format. You can use AutoHotkey to automate this process in IrfanView with just a few lines of code:\n\nsql\nCopy code\n; Set the path to the folder containing the images\nImagePath := \"C:\\Images\"\n\n; Set the target file format and quality\nFormat := \"JPG\"\nQuality := 80\n\n; Set the target image dimensions and border size\nWidth := 800\nHeight := 600\nBorderSize := 10\n\n; Loop through each file in the folder and apply the editing\nLoop, %ImagePath%\\*.jpg\n{\n    ; Get the filename and extension of the current file\n    SplitPath, A_LoopFileFullPath, FileName, Extension\n\n    ; Open the image in IrfanView\n    Run, \"C:\\Program Files\\IrfanView\\i_view64.exe\" \"%A_LoopFileFullPath%\"\n\n    ; Resize the image\n    WinWaitActive, %FileName% - IrfanView\n    Send, ^r\n    WinWaitActive, Resize/Resample\n    Send, %Width% x %Height%\n    Send, {Enter}\n\n    ; Add a border\n    WinWaitActive, %FileName% - IrfanView\n    Send, ^b\n    WinWaitActive, Add border\n    Send, %BorderSize%\n    Send, {Enter}\n\n    ; Save the edited image\n    WinWaitActive, %FileName% - IrfanView\n    Send, ^s\n    WinWaitActive, Save as\n    Send, %ImagePath%\\%FileName%.%Format%\n    Send, {Enter}\n    Send, {Enter}\n\n    ; Close the image\n    WinWaitActive, %FileName% - IrfanView\n    Send, ^q\n}\n\n; Display a message when the editing is complete\nMsgBox, % \"Batch editing is complete!\"\nThis code uses a loop to go through each image in the folder and perform the editing steps one by one. It opens each image in IrfanView, resizes it, adds a border, and saves it as a JPG file with the specified dimensions and quality. Once all the images are processed, a message box is displayed to notify you that the batch editing is complete.\n\nOf course, this is just one example, and you can customize the code to suit your specific needs. With AutoHotkey and IrfanView, the possibilities for batch image editing are endless!", "from": "assistant", "parent_id": 5287513724223611599, "message_id": 8906576197775372008}]
'''
data = [] # Format: [(user text, assistant text), ...]
with open(oasstjsonl, "r") as f:
    # Load only the first two turns for each line & only the text
    for line in f.readlines():
        line = json.loads(line)
        data.append((line[0]["text"], line[1]["text"]))

print("Example")
print(data[0])

def get_code(text):
    first_backticks = text.find("```") # First backticks
    if first_backticks == -1:
        # No backticks
        return False
    # Get the programming language e.g. ....\n```python\n...
    lang = text[first_backticks + 3 : text.find("\n", first_backticks + 3)].strip()
    if (not(lang)) or (len(lang) > 20):
        # Probably not a programming language
        return False
    print(lang)
    return lang

lang_counts = {}
for user, assistant in data:
    lang = get_code(assistant)
    if lang:
        if lang in lang_counts:
            lang_counts[lang] += 1
        else:
            lang_counts[lang] = 1

print(sorted(lang_counts.items(), key=lambda x: x[1], reverse=True))