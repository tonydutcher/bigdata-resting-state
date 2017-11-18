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

#############
##    LR   ##
#############

# navigate to birthing directory
cd $birth

# change into bold run directory
cd ${sub}/LR/REST1

# run some smoothing
if [ -f ${LR} ]; then
echo "${LR} exists"

echo "Running: fslmaths ${LR} -s 1.69865806013249532869 ${LR%*.nii.gz}_s"
echo " "
fslmaths ${LR} -s 1.69865806013249532869 ${LR%*.nii.gz}_s

# space is tight so I have to move it out to scratch... :(
if ! [[ -d $SCRATCH/hcp_112017/${sub}/LR/REST1 ]]; then
echo "scratch sub-directory doesn't exist - creating"
echo " "
mkdir -p $SCRATCH/hcp_112017/${sub}/LR/REST1
fi

echo "Moving unsmoothed file to scratch"
echo " "
mv -v ${LR} $SCRATCH/hcp_112017/${sub}/LR/REST1

else
echo "${LR} does not exist - skipping."
echo " "

fi

############
##    RL   ##
#############

# return to birth
cd $birth

# change into subject bold run directory 
cd ${sub}/RL/REST1

# run some smoothing
if [ -f ${RL} ]; then
echo "${RL} exists"
echo "Running: fslmaths ${RL} -s 1.69865806013249532869 ${RL%*.nii.gz}_s"
echo " "
fslmaths ${RL} -s 1.69865806013249532869 ${RL%*.nii.gz}_s

# space is tight so I have to move it out to scratch... :(
if ! [[ -d $SCRATCH/hcp_112017/${sub}/RL/REST1 ]]; then
echo "scratch sub-directory doesn't exist - creating"
echo " "
mkdir -p $SCRATCH/hcp_112017/${sub}/RL/REST1
fi
echo "Moving unsmoothed file to scratch"
echo " "
mv -v ${RL} $SCRATCH/hcp_112017/${sub}/RL/REST1

else

echo "${RL} does not exist - skipping."
echo " "

fi

# return to birth
cd $birth
