4#!/bin/sh

# to be called from "code/bidsNighres"

participant="pilot001 pilot004 pilot005"

root_dataset=${PWD}/../..

input_dataset=${root_dataset}/inputs/raw/

output_location=${root_dataset}/outputs/derivatives/bidsNighres/

filter_file=${root_dataset}/code/bidsNighres/filter_file.json

echo "${input_dataset}"

python ../lib/bidsNighres/run.py \
    --input-datasets "${input_dataset}" \
    --output-location "${output_location}" \
    --analysis-level subject \
    --participant-label "${participant}" \
    --action layer \
    --nb-layers 6 \
    --bids-filter-file "${filter_file}"
