#!/bin/bash

batchdir=/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/batch
launchdir=/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/batch/launch
scriptdir=/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/analysis
subjectdir=/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects
outdir=/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/logs

# get the subjects we want to perform the analyses on.
cd ${subjectdir}
subjects=`ls -d ??????`

# navigate to batch dir to create launchscripts in
cd ${batchdir}
count=1
batchnum=1

# file names to save output and to launch
basefile=launch_regress_subjects_batch
logfile=${basefile}_RAN_SUBJECTS.log

# removes any files by this name in batch dir
if [ -f ${basefile}_1.sh ]; then
echo " "
echo "Removing the existing ${basefile}* from batch directory."
echo " "

rm launch_regress_subjects_batch_*.sh
#echo " "
#echo "Must remove ${basefile}* files from batch directory."
#echo " "
#exit 1
fi

# cycle through the subjects
for sub in ${subjects[@]}; do

# launchfile for this batch of subjects
launchfile=${basefile}_${batchnum}.sh

# collect a variable to let us know what subjects have actually been run.
echo "${sub}">>${outdir}/${logfile}

# this creates a launch file to send to TACC
echo "${scriptdir}/regress_subject.sh ${sub}">>${launchfile}

# keep 16 subjects within a single launch script
if [ ${count} -eq 16 ]; then
echo ${batchnum}

if [ ${batchnum} -ge 3 ]; then
launch -s ${launchfile} -r 05:00:00 -o ${outdir}/${launchfile%.sh}.o -m amdutcher@utexas.edu -N 1 -n 2 -A ANTS -J ${launchdir}/${launchfile%.sh}_JOBFILE
fi
batchnum=`echo "${batchnum}+1 " | bc -l`
count=1
fi

# 
if [ ${batchnum} -eq 51 ];then
echo "Reached 50 slurm scripts. Exiting..."
exit 1
fi

count=`echo "${count}+1" | bc -l`

done
