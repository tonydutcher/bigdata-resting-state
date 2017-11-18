#!/bin/bash

file=$1

batchdir=/work/04635/adutcher/lonestar/hcp_rest_behav/batch
launchdir=/work/04635/adutcher/lonestar/hcp_rest_behav/batch/launch
scriptdir=${HOME}/analysis/hcp_rest_behav/preprocess
subjectdir=/work/04635/adutcher/lonestar/hcp_rest_behav/subjects
outdir=/work/04635/adutcher/lonestar/hcp_rest_behav/logs
basefile=launch_xreate_smoothing_batch_UPDATE
logfile=${basefile}_RAN_SUBJECTS.log
launchfile=${basefile}_RAN_SUBJECTS.sh

cd ${batchdir}

while read line; do

echo "${scriptdir}/create_smoothing.sh ${line}">>${launchfile}

done < "$file"

launch -s ${launchfile} -r 10:00:00 -o ${outdir}/${launchfile%.sh}.o -m amdutcher@utexas.edu -N 1 -n 3 -A ANTS -J ${launchdir}/${launchfile%.sh}_JOBFILE
