#!/bin/bash

if [ $# -lt 5 ] || [ $1 = '-h' ]; then
echo "Function to smooth data at 4 mm kernal using fslmaths (easily adjustable in source)
Input = subject id for hcp_rest_behav study directory"
    echo "  Usage: create_smoothing.sh <sid> <phase> <run> <dtype> <mvfile>
            INPUTS - separated by spaces
            sid    = subject id - refers to subject directory with image file (not full path)
            phase  = RL or LR - the phase encoding direction of image file
            run    = REST1 or REST2 - the run
            imgsuf = can be blank or suffix of a filtered image e.g. '_FILT' (see regress confounds)
            mvfile = y or n, move the original file to scratch?"
    exit 1

fi

SUBJECT=$1
PHASE=$2
RUN=$3
IMGSUF=$4
MVFILE=$5

# image files
imgfile=${STUDYDIR}/subjects/${SUBJECT}/${PHASE}/${RUN}/rfMRI_${RUN}_${PHASE}_hp2000_clean${IMGSUF}.nii.gz
newfile=${STUDYDIR}/subjects/${SUBJECT}/${PHASE}/${RUN}/rfMRI_${RUN}_${PHASE}_hp2000_clean${IMGSUF}_s.nii.gz
npyfile=${STUDYDIR}/subjects/${SUBJECT}/processed/brain_array_non.npy

if [ -e ${newfile} ]; then
echo "${newfile} ALREADY EXISTS"
exit 1

elif [ -e ${imgfile} ]; then
echo "Running: fslmaths ${imgfile} -s 1.69865806013249532869 ${newfile}"
fslmaths ${imgfile} -s 1.69865806013249532869 ${newfile}

elif ! [ -e ${imgfile} ]; then
echo "No image file to process for ${SUBJECT} ${PHASE} ${RUN}"
exit 1
fi

# space is tight so I have to move it out to scratch... :(
if [ $MVFILE = 'y' ]; then
mv ${imgfile} ${SCRATCH}/hcp_112017/${SUBJECT}/${PHASE}/${RUN}

elif [ $MVFILE = 'n' ]; then
echo "Image file for ${SUBJECT} ${PHASE} ${RUN} was processed and nothing was moved to scratch in its place"
fi
