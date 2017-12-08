#!/bin/bash

if [ $# -lt 1 ] || [ $1 = '-h' ]; then

echo "Function to run a set of functions on a single subject by run.
 - Input = subject id for hcp_rest_behav study directory (not full path)"
exit 1

fi

SUBJECT=$1
echo "Working on ${SUBJECT}"
echo " "

echo "Running: $HOME/analysis/hcp_rest_behav/preprocess/regress_subjects.sh ${SUBJECT} LR  REST1 FIX 'n'"
${SRCDIR}/preprocess/regress_confounds.sh ${SUBJECT} LR REST1 FIX 'n'

echo "Running: $HOME/analysis/hcp_rest_behav/preprocess/create_smoothing.sh ${SUBJECT} LR  REST1 _FILT 'y'"
${SRCDIR}/preprocess/create_smoothing.sh ${SUBJECT} LR REST1 _FILT 'y'

echo "Running: $HOME/analysis/hcp_rest_behav/preprocess/regress_subjects.sh ${SUBJECT} RL  REST1 FIX 'n'"
${SRCDIR}/preprocess/regress_confounds.sh ${SUBJECT} RL REST1 FIX 'n'

echo "Running: $HOME/analysis/hcp_rest_behav/preprocess/create_smoothing.sh ${SUBJECT} RL  REST1 _FILT 'y'"
${SRCDIR}/preprocess/create_smoothing.sh ${SUBJECT} RL REST1 _FILT 'y'
