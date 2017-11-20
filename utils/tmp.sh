#!/bin/bash

subdir=$WORK/hcp_rest_behav/subjects

cd $subdir
subjects=`ls -d ??????`
count=1
for s in ${subjects[@]}; do
 
${HOME}/analysis/hcp_rest_behav/utils/compress_hdf5.py -s ${subdir}/${s}

#if [ ${count} -eq 4 ];then
#echo "Check to make sure things worked."
#exit 1
#fi

count=`echo "${count}+1" | bc -l`
done
