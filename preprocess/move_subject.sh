#!/bin/bash

if [ $# -lt 1 ]; then
exit 1
fi

sub=$1

LR=${WORK}/hcp_rest_behav/subjects/${sub}/LR/REST1/rfMRI_REST1_LR_hp2000_clean_FILT.nii.gz
RL=${WORK}/hcp_rest_behav/subjects/${sub}/RL/REST1/rfMRI_REST1_RL_hp2000_clean_FILT.nii.gz

# LR
if [ -e ${LR} ]; then
echo "${LR} exists, moving"
mv ${LR} $SCRATCH/hcp_112017/${sub}/LR/REST1
fi


# RL
if [ -e ${RL} ]; then
echo "${RL} exists, moving" 
mv ${RL} $SCRATCH/hcp_112017/${sub}/RL/REST1
fi

