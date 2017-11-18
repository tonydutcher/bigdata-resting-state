#!/bin/bash

if [ $# -lt 1 ]; then
echo "Function to smooth data at 4 mm kernal using fslmaths (easily adjustable in source)
Input = subject id for hcp_rest_behav study directory"
exit 1
fi

sub=$1
birth=${WORK}/hcp_rest_behav/subjects

LR=${WORK}/hcp_rest_behav/subjects/${sub}/LR/REST1/rfMRI_REST1_LR_hp2000_clean_FILT.nii.gz
RL=${WORK}/hcp_rest_behav/subjects/${sub}/RL/REST1/rfMRI_REST1_RL_hp2000_clean_FILT.nii.gz
if [ -f ${LR} ]; then
echo "${LR} does exist"
echo " "
if ! [[ -d $SCRATCH/hcp_112017/${sub}/LR/REST1 ]]; then
echo "scratch sub-directory does not exist - creating"
echo  " "
#mkdir -p $SCRATCH/hcp_112017/${sub}/LR/REST1
else
echo "scratch sub-directory exists"
echo " "
fi

else
echo "${LR} does not exist"
echo " "

fi
