# read in the data
with open('kilobytes.txt') as f:
    data = f.read()

# split the data into lines
lines = data.strip().split('\n')

# create a dictionary to store the byte counts for each language
byte_counts = {}
total_bytes = 0
for line in lines:
    parts = line.split()
    print(parts)
    kb = int(parts[0]) / 1000 # Convert to megabytes
    name = parts[1]
    byte_counts[name] = kb
    if name != "total":
        total_bytes += kb

# create the markdown table header
print('| Name | Megabytes | % of total |')
print('| --- | --- | --- |')

# create the markdown table rows
for name, kb in sorted(byte_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = round(kb / total_bytes * 100, 4)
    print(f'| {name} | {kb} | {percentage}% |')
