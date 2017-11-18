#!/bin/bash

FILE=$1
PHASE=$2

if [ -z $1 ] || [ -z $2 ]; then
	echo "need two input arguments
		1 is a file with a column of subject names
		2 is the phase encoding direction - RL or LR"
	exit 1
fi
while IFS=, read -r col1; do

echo "working on subject, ${col1}"

$HOME/analysis/hcp_rest_behav/utils/remote_to_tacc_subject_bold.sh ${col1} ${PHASE}

echo "completed subject, ${col1}"

done < "${FILE}"
