# CMD: du -sc data/* | sort -h > kilobytes.txt
# read in the data
with open('kilobytes.txt') as f:
    data_kb = f.read()

# CMD: wc -l * | sort -hr > line_counts.txt
# wc -l */*.jsonl | sort -h > line_counts.txt
with open('line_counts.txt') as f:
    data_l = f.read()

# split the data into lines
kbs = data_kb.strip().split('\n')
ls = data_l.strip().split('\n')

# create a dictionary to store the byte counts for each language
byte_counts = {}
total_bytes = 0
for line in kbs:
    parts = line.split()
    print(parts)
    kb = int(parts[0]) / 1000 # Convert to megabytes
    name = parts[1]
    byte_counts[name] = kb
    if name != "total":
        total_bytes += kb

line_counts = {}
total_lines = 0
for line in ls:
    parts = line.split()
    print(parts)
    l = int(parts[1])
    name = parts[0].split("/")[-1][:-1]
    line_counts[name] = l
    if name != "total":
        total_lines += l
line_counts["total"] = total_lines

# create the markdown table header
print('| Name | Megabytes | % of total | Samples | % of total |')
print('| --- | --- | --- | --- | --- |')

# create the markdown table rows
# Sort lines acc to byte count 

for name, kb in sorted(byte_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = round(kb / total_bytes * 100, 4)
    ls = line_counts[name]
    l_percentage = round(ls / total_lines * 100, 4)
    print(f'| {name} | {kb} | {percentage}% | {ls} | {l_percentage}% |')

################

# CMD: du -sc data/* | sort -h > kilobytes.txt
# read in the data
with open('kilobytes_filtered.txt') as f:
    data_kb = f.read()

# CMD: wc -l * | sort -hr > line_counts.txt
# wc -l */*.jsonl | sort -h > line_counts.txt
with open('line_counts_filtered.txt') as f:
    data_l = f.read()

# split the data into lines
kbs = data_kb.strip().split('\n')
ls = data_l.strip().split('\n')

# create a dictionary to store the byte counts for each language
byte_counts_f = {}
total_bytes_f = 0
for line in kbs:
    parts = line.split()
    print(parts)
    kb = int(parts[0]) / 1000 # Convert to megabytes
    name = parts[1]
    byte_counts_f[name] = kb
    if name != "total":
        total_bytes_f += kb

line_counts_f = {}
total_lines_f = 0
for line in ls:
    parts = line.split()
    print(parts)
    l = int(parts[1])
    name = parts[0].split("/")[-1][:-1]
    line_counts_f[name] = l
    if name != "total":
        total_lines_f += l
line_counts_f["total"] = total_lines_f

# create the markdown table header
print('| Name | Megabytes | % of total | Samples | % of total |')
print('| --- | --- | --- | --- | --- |')

# create the markdown table rows
# Sort lines acc to byte count 

for name, kb in sorted(byte_counts_f.items(), key=lambda x: x[1], reverse=True):
    percentage = round(kb / total_bytes_f * 100, 4)
    ls = line_counts_f[name]
    l_percentage = round(ls / total_lines_f * 100, 4)
    print(f'| {name} | {kb} | {percentage}% | {ls} | {l_percentage}% |')

################

# Latex table
print("-"*80)
print(' & \\multicolumn{3}{c}{Raw} & \\multicolumn{3}{c}{Filtered} \\\\')
print('Name & Megabytes & Samples % of total (MB) & Samples & Megabytes & % of total (MB) \\\\')
print('\\midrule')
for name, kb in sorted(byte_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = round(kb / total_bytes * 100, 4)
    ls = line_counts[name]
    l_percentage = round(ls / total_lines * 100, 4)
    kb_f = byte_counts_f.get(name, 0)
    percentage_f = round(kb_f / total_bytes_f * 100, 4)
    ls_f = line_counts_f.get(name, 0)
    l_percentage_f = round(ls_f / total_lines_f * 100, 4)
    print(f'{name} & {kb} & {ls} & {percentage} & {kb_f} & {ls_f} & {percentage_f} \\\\')