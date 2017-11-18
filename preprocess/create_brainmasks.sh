#!/bin/bash

sub=$1
birth=${WORK}/hcp_rest_behav/subjects
MNI2MM=/work/IRC/ls5/opt/apps/fsl-5.0.9/data/standard/MNI152_T1_2mm_brain.nii.gz

# navigate to birthing directory
cd $birth

# change into subject mask directory 
cd ${sub}/masks

# resample the brainmask_fs into 2mm space
flirt -in brainmask_fs.nii.gz -ref ${MNI2MM} -out tmp.nii.gz -applyisoxfm 2

# threshold the brain image
fslmaths tmp.nii.gz -thr 0.65 -bin brain2mm_thr065

# remove the temporary file.
rm tmp.nii.gz

# return to birth
cd $birth
