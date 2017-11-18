#!/bin/bash

FILE=$1

if [ $# -lt 1 ]; then
echo "need two input argument
Takes the full path to a file as single input with the subjects 
to be copied from remote to tacc - uses remote_to_tacc_subject_mask.sh
function - see function for details."
exit 1
fi
while read subject; do

echo "working on subject, $subject"

$HOME/analysis/hcp_rest_behave/utils/remote_to_tacc_subject_masks.sh $subject

echo "completed subject, $subject"

done < "$FILE"
