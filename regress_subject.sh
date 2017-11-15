#!/bin/bash
if [ $# -eq 0 ]; then 
echo "Give subject number for FIX ica data from HCP"
exit 1
fi
# a subject for slurm
subject=$1
/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/analysis/regress_confounds.sh $subject LR REST1 FIX
/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/analysis/regress_confounds.sh $subject RL REST1 FIX
