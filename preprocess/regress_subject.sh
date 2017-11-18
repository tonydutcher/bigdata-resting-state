#!/bin/bash
if [ $# -lt 1 ]; then 
echo "Give subject number (NOT FULL PATH) for FIX ica data from HCP"
exit 1
fi
# a subject for slurm
subject=$1
${HOME}/analysis/hcp_rest_behav/regress_confounds.sh $subject LR REST1 FIX
${HOME}/analysis/hcp_rest_behav/regress_confounds.sh $subject RL REST1 FIX
