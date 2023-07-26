"""
Check if there are missing files when generating using the range scripts.
Usage: `python check_missing.py "generations_humanevalfixpython_wizardcoder*.json"`
"""
import sys
import glob

def find_missing_file(file_pattern):
    file_list = glob.glob(file_pattern)
    file_numbers = set()

    for file_name in file_list:
        try:
            file_number = int(file_name.split("_")[-1].split(".")[0])
            file_numbers.add(file_number)
        except ValueError:
            pass

    missing_numbers = set(range(0, 164)) - file_numbers

    print("Missing files: ", missing_numbers)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_missing <file_pattern>")
        sys.exit(1)

    file_pattern = sys.argv[1]

    find_missing_file(file_pattern)
