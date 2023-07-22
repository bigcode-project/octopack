#!/bin/bash

input_file="diffs_33554432_41943040.jsonl"
input_file="diffs_58720256_67108864.jsonl"
input_file="diffs_0_8388608.jsonl"
total_lines=8388608
num_shards=16

lines_per_shard=$((total_lines / num_shards))
start_line=1

for i in $(seq 1 $num_shards); do
    end_line=$((start_line + lines_per_shard - 1))
    start_range=$((start_line + 0))
    end_range=$((end_line + 0))
    output_file="diffs_${start_range}_${end_range}.jsonl"
    sed -n "${start_line},${end_line}p" $input_file > $output_file
    start_line=$((end_line + 1))
done

