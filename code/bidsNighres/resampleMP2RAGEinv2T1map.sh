#!/bin/sh

# to be called from "code/bidsNighres"

participant="pilot001 pilot004 pilot005"

# resample_factor=2

root_dataset=${PWD}/../..

input_dataset=${root_dataset}/inputs/raw/

output_location=${root_dataset}/outputs/derivatives/bidsNighres/

filter_file=${root_dataset}/code/bidsNighres/filter_file_resample.json

echo "${input_dataset}"

python3 ../lib/run_resample.py \
    --input-datasets "${input_dataset}" \
    --output-location "${output_location}" \
    --participant-label "${participant}" \
    --bids-filter-file "${filter_file}"
