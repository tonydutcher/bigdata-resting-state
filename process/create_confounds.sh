#!/bin/bash

if [ $# -lt 4 ]; then
	echo "	Usage: create_confounds.sh <sid> <phase> <run> <dtype>
    		INPUTS - separated by spaces
    		sid   = subject id - refers to subject directory with image file
    		phase = RL or LR - the phase encoding direction of image file
    		run   = REST1 or REST2 - the run
		dtype = FIX or PROC data type of image to create confound file for"
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

# location of FIX confound variables
csffile=${WORK}/test_hcp/hcp_behav_rest/subjects/${SUBJECT}/${PHASE}/${RUN}/rfMRI_${RUN}_${PHASE}_CSF.txt
wmfile=${WORK}/test_hcp/hcp_behav_rest/subjects/${SUBJECT}/${PHASE}/${RUN}/rfMRI_${RUN}_${PHASE}_WM.txt
baseout=${WORK}/test_hcp/hcp_behav_rest/subjects/${SUBJECT}/${PHASE}/${RUN}/confounds
outfile=${baseout}.txt
outlog=${baseout}.log


# make sure these file exist
if ! [ -f $wmfile ] || ! [ -f $csffile ]; then
echo "WM or CSF file does not exist."
exit 1
fi

# the FIX data type does not have motion correction as confound for subsequent analysis. 
if [ ${DTYPE} == FIX ]; then 

echo "Concatenating WM and CSF files into single confound file."
paste ${csffile} ${wmfile} | column -s $'\t' -t > ${outfile}
echo -e "paste rfMRI_${RUN}_${PHASE}_CSF.txt rfMRI_${RUN}_${PHASE}_WM.txt | column -s '\t' -t > confounds.txt">>${outlog}
fi
