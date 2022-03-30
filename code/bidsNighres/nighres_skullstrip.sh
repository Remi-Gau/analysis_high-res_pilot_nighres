#!/bin/sh

# to be called from the root of the dataset

participant=pilot001

root_dataset=${PWD}/../..

input_dataset=${root_dataset}/outputs/derivatives/cpp_spm-preproc/

output_location=${root_dataset}/outputs/derivatives/bidsNighres/

filter_file=${root_dataset}/code/filter_file.json

echo "${input_dataset}"

python ../lib/bidsNighres/run.py \
    --input-datasets "${input_dataset}" \
    --output-location "${output_location}" \
    --analysis-level subject \
    --participant-label "${participant}" \
    --action skullstrip \
    --bids-filter-file "${filter_file}"

python ../lib/bidsNighres/run.py \
    --input-datasets "${input_dataset}" \
    --output-location "${output_location}" \
    --analysis-level subject \
    --participant-label "${participant}" \
    --action segment \
    --bids-filter-file "${filter_file}"
