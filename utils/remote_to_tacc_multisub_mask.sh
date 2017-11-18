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

if [ -f $HOME/analysis/hcp_rest_behav/utils/remote_to_tacc_subject_mask.sh ]; then
$HOME/analysis/hcp_rest_behav/utils/remote_to_tacc_subject_mask.sh $subject
else
echo "Calling a script that does not exist"
exit 1
fi
echo "completed subject, $subject"

done < "$FILE"
