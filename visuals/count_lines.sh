#!/bin/bash

# Iterate through directories in the ./data/ directory
for dir in ./data/*; do
    # Extract the directory name
    dirname=$(basename "$dir")
    # Count the total number of lines in jsonl files within the directory
    count=$(find "$dir" -name "*.jsonl" | xargs cat | wc -l)
    # Print the directory name and line count
    echo "data/$dirname: $count"
done > line_count.txt
