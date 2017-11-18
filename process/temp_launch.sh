#!/bin/bash

batchdir=/work/04635/adutcher/lonestar/hcp_rest_behav/batch
launchdir=/work/04635/adutcher/lonestar/hcp_rest_behav/batch/launch
scriptdir=${HOME}/analysis/hcp_rest_behav
subjectdir=/work/04635/adutcher/lonestar/hcp_rest_behav/subjects
outdir=/work/04635/adutcher/lonestar/hcp_rest_behav/logs
basefile=launch_regress_subjects_batch_UPDATE
logfile=${basefile}_RAN_SUBJECTS.log

launchfile=${basefile}_RAN_SUBJECTS.sh

cd ${batchdir}

while read line; do

echo "${scriptdir}/regress_subject.sh ${line}">>${launchfile}

done < ${outdir}/need_to_run.txt

launch -s ${launchfile} -r 10:00:00 -o ${outdir}/${launchfile%.sh}.o -m amdutcher@utexas.edu -N 1 -n 2 -A ANTS -J ${launchdir}/${launchfile%.sh}_JOBFILE
