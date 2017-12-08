#!/bin/bash

LAUNCHDIR=${BATCHDIR}/launch
SUBJECTDIR=${STUDYDIR}/subjects
OUTDIR=${STUDYDIR}/logs

# get the subjects we want to perform the analyses on.
cd ${SUBJECTDIR}
SUBJECTS=`ls -d ??????`

# navigate to batch dir to create launchscripts in
cd ${BATCHDIR}
COUNT=1
BATCHNUM=1

# file names to save output and to launch
BASEFILE=launch_preprocess_subjects_batch
LOGFILE=${BASEFILE}_RAN_SUBJECTS.log

# removes any files by this name in batch dir
if [ -e ${BASEFILE}_1.sh ]; then
echo " "
echo "Removing the existing ${BASEFILE}* from batch directory."
echo " "
rm ${BASEFILE}_*.sh
#echo " "
#echo "Must remove ${basefile}* files from batch directory."
#echo " "
#exit 1
fi

# cycle through the subjects
for SUBJECT in ${SUBJECTS}; do

# launchfile for this batch of subjects
LAUNCHFILE=${BASEFILE}_${BATCHNUM}.sh

# this creates a launch file to send to TACC
echo -e "${SRCDIR}/preprocess/preprocess_subject.sh ${SUBJECT}">>${LAUNCHFILE}

# keep 16 subjects within a single launch script
if [ ${COUNT} -eq 16 ]; then
echo ${BATCHNUM}

if [ ${BATCHNUM} -ge 0 ]; then
launch -s ${LAUNCHFILE} -r 05:00:00 -o ${OUTDIR}/${LAUNCHFILE%.sh}.o -m amdutcher@utexas.edu -N 1 -n 2 -A ANTS -J ${LAUNCHDIR}/${LAUNCHFILE%.sh}_JOBFILE
fi
BATCHNUM=`echo "${BATCHNUM}+1 " | bc -l`
COUNT=1
fi

# 
if [ ${BATCHNUM} -eq 51 ];then
echo "Reached 2 slurm scripts. Exiting..."
exit 1
fi

COUNT=`echo "${COUNT}+1" | bc -l`

done
