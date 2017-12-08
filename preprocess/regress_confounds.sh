#!/bin/bash
if [ $# -lt 5 ] || [ $1 = '-h' ]; then
        echo "  Usage: regress_confounds.sh <sid> <phase> <run> <dtype> <mvfile>
                INPUTS - separated by spaces
                sid    = subject id - refers to subject directory with image file (not full path)
                phase  = RL or LR - the phase encoding direction of image file
                run    = REST1 or REST2 - the run
                dtype  = FIX or PROC data type of image to create confound file for
                mvfile = y or n, move the original file to scratch?"
        exit 1

fi
#
#readopt='getopts $opts opt;rc=$?;[ $rc$opt == 0? ]&&exit 1;[ $rc == 0 ]||{ shift $[OPTIND-1];false; }'
#opts=amds:r:
#
## Enumerating options
#while eval $readopt; do
#    eval "arg_${opt}=${OPTARG-true}"
#done
#
## default: run both motion and alignment
#if [[ -z "$arg_a" ]] && [[ -z "$arg_m" ]] && [[ -z "$arg_d" ]]; then
#    arg_a=true
#    arg_m=true
#    arg_d=true
#fi

SUBJECT=$1
PHASE=$2
RUN=$3
DTYPE=$4
MVFILE=$5

# location of FIX confound variables
csffile=${WORK}/hcp_rest_behav/subjects/${SUBJECT}/${PHASE}/${RUN}/rfMRI_${RUN}_${PHASE}_CSF.txt
wmfile=${WORK}/hcp_rest_behav/subjects/${SUBJECT}/${PHASE}/${RUN}/rfMRI_${RUN}_${PHASE}_WM.txt
baseout=${WORK}/hcp_rest_behav/subjects/${SUBJECT}/${PHASE}/${RUN}/confounds
outfile=${baseout}.txt
outlog=${WORK}/hcp_rest_behav/subjects/${SUBJECT}/${PHASE}/${RUN}/hist_file.log

# image files
imgfile=${WORK}/hcp_rest_behav/subjects/${SUBJECT}/${PHASE}/${RUN}/rfMRI_${RUN}_${PHASE}_hp2000_clean.nii.gz
newfile=${WORK}/hcp_rest_behav/subjects/${SUBJECT}/${PHASE}/${RUN}/rfMRI_${RUN}_${PHASE}_hp2000_clean_FILT.nii.gz

# make sure these file exist
if ! [ -f $wmfile ] || ! [ -f $csffile ]; then
echo "WM or CSF file does not exist."
exit 1

elif [ -e ${newfile} ]; then
echo "${newfile} ALREAD EXISTS, exiting..."
exit 1
fi

# the FIX data type does not have motion correction as confound for subsequent analysis. 
if [ ${DTYPE} == FIX ]; then 

echo "Concatenating WM and CSF files into single confound file."
paste ${csffile} ${wmfile} | column -s $'\t' -t > ${outfile}
echo -e "paste rfMRI_${RUN}_${PHASE}_CSF.txt rfMRI_${RUN}_${PHASE}_WM.txt | column -s '\\t' -t > confounds.txt"
fi

# regress out confounds.
if [ -e ${outfile} ]; then

echo "Running fsl_glm -i ${imgfile} -d ${outfile} --out_res=${newfile}"
fsl_glm -i ${imgfile} -d ${outfile} --out_res=${newfile}

if [ -e ${newfile} ] && [ $MVFILE = 'y' ]; then
# move old file to scratch...
mkdir -p ${SCRATCH}/hcp_112017/${SUBJECT}/${PHASE}/${RUN}
echo "Moving ${imgfile}">>${outlog}
echo "To ${SCRATCH}/hcp_112017/${SUBJECT}/${PHASE}/${RUN}"
mv ${imgfile} ${SCRATCH}/hcp_112017/${SUBJECT}/${PHASE}/${RUN}
fi

elif ! [ -e ${imgfile} ]; then
echo "No image file to process for ${SUBJECT} ${PHASE} ${RUN}"

elif [ -e ${newfile} ] && [ $MVFILE = 'n' ]; then
echo "Image file for ${SUBJECT} ${PHASE} ${RUN} processed and not moved to scratch"
fi
