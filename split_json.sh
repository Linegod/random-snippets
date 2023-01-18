#!/bin/bash
# J.P. Pasnak, CD
# 2023-01-17
# Splits a json file into xMeg chunks
# Relies on jq and split
# 
# Converts ${INPUT} into single line objects,
# then splits on a given size.   Then uses --filter to
# place each split back into an array an outputs to 
# given filename
INPUT=$1
OUTPUT=$2
SIZE=$3
jq -c '.[]' ${INPUT} |
    split --filter="jq -s '.' >\${FILE}.json" -d -C ${SIZE}M - ${OUTPUT}
