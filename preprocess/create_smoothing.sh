#!/bin/bash

sub=$1
birth=${WORK}/hcp_rest_behav/subjects

LR=${WORK}/hcp_rest_behav/subjects/${sub}/LR/REST1/rfMRI_REST1_LR_hp2000_clean_FILT.nii.gz
RL=${WORK}/hcp_rest_behav/subjects/${sub}/RL/REST1/rfMRI_REST1_RL_hp2000_clean_FILT.nii.gz

# navigate to birthing directory
cd $birth

# change into subject mask directory 
cd ${sub}/LR/REST1

# resample the brainmask_fs into 2mm space
fslmaths ${LR} -s 1.69865806013249532869 ${LR%*.nii.gz}_s

# return to birth
cd $birth
