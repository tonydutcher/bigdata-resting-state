#!/bin/bash

file=$1

while read s; do

echo $s

echo "Running: $HOME/analysis/hcp_rest_behav/preprocess/create_brainmasks.sh $s"
$HOME/analysis/hcp_rest_behav/preprocess/create_brainmasks.sh $s

done < "$file"
