#!/bin/bash

FILE=$1

MASKDIR1=${WORK}/masks/mni_mtl
MASKDIR2=${WORK}/masks/bn

m1=l_hip_tail_2mm.nii.gz
m2=r_hip_tail_2mm.nii.gz
m3=l_hip_ant_2mm.nii.gz
m4=r_hip_ant_2mm.nii.gz
m5=BN_105_2mm.nii
m6=BN_106_2mm.nii
m7=BN_107_2mm.nii
m8=BN_108_2mm.nii
m9=BN_187_2mm.nii
m10=BN_188_2mm.nii

LAUNCHDIR=${BATCHDIR}/launch
SUBJECTDIR=${STUDYDIR}/subjects
OUTDIR=${STUDYDIR}/logs

# get the subjects we want to perform the analyses on.
cd ${SUBJECTDIR}
SUBJECTS=`ls -d ??????`
#SUBJECTS=(`cat ${SRCDIR}/file_to_run`)
#echo ${SUBJECTS}

# navigate to batch dir to create launchscripts in
cd ${BATCHDIR}
COUNT=1
BATCHNUM=1

# file names to save output and to launch
BASEFILE=launch_connectivity_con_subjects_batch
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
for SUBJECT in ${SUBJECTS[@]}; do

#SUBJECT=$(basename ${SUBJECT})

# launchfile for this batch of subjects
LAUNCHFILE=${BASEFILE}_${BATCHNUM}.sh

# this creates a launch file to send to TACC
echo -e "python ${SRCDIR}/seed_connectivity.py -s ${SUBJECTDIR}/${SUBJECT} -m ${MASKDIR1}/${m1} -it 'npy'">>${LAUNCHFILE}
echo -e "python ${SRCDIR}/seed_connectivity.py -s ${SUBJECTDIR}/${SUBJECT} -m ${MASKDIR1}/${m2} -it 'npy'">>${LAUNCHFILE}
echo -e "python ${SRCDIR}/seed_connectivity.py -s ${SUBJECTDIR}/${SUBJECT} -m ${MASKDIR1}/${m3} -it 'npy'">>${LAUNCHFILE}
echo -e "python ${SRCDIR}/seed_connectivity.py -s ${SUBJECTDIR}/${SUBJECT} -m ${MASKDIR1}/${m4} -it 'npy'">>${LAUNCHFILE}
echo -e "python ${SRCDIR}/seed_connectivity.py -s ${SUBJECTDIR}/${SUBJECT} -m ${MASKDIR2}/${m5} -it 'npy'">>${LAUNCHFILE}
echo -e "python ${SRCDIR}/seed_connectivity.py -s ${SUBJECTDIR}/${SUBJECT} -m ${MASKDIR2}/${m6} -it 'npy'">>${LAUNCHFILE}
echo -e "python ${SRCDIR}/seed_connectivity.py -s ${SUBJECTDIR}/${SUBJECT} -m ${MASKDIR2}/${m7} -it 'npy'">>${LAUNCHFILE}
echo -e "python ${SRCDIR}/seed_connectivity.py -s ${SUBJECTDIR}/${SUBJECT} -m ${MASKDIR2}/${m8} -it 'npy'">>${LAUNCHFILE}
echo -e "python ${SRCDIR}/seed_connectivity.py -s ${SUBJECTDIR}/${SUBJECT} -m ${MASKDIR2}/${m9} -it 'npy'">>${LAUNCHFILE}
echo -e "python ${SRCDIR}/seed_connectivity.py -s ${SUBJECTDIR}/${SUBJECT} -m ${MASKDIR2}/${m10} -it 'npy'">>${LAUNCHFILE}

# keep 16 subjects within a single launch script
if [ ${COUNT} -eq 15 ]; then
echo ${BATCHNUM}

if [ ${BATCHNUM} -ge 0 ]; then
launch -s ${LAUNCHFILE} -r 01:30:00 -o ${OUTDIR}/${LAUNCHFILE%.sh}.o -m amdutcher@utexas.edu -N 1 -n 3 -A ANTS -J ${LAUNCHDIR}/${LAUNCHFILE%.sh}_JOBFILE
fi
BATCHNUM=`echo "${BATCHNUM}+1 " | bc -l`
COUNT=1
fi

# 
if [ ${BATCHNUM} -eq 51 ];then
echo "Reached 50 slurm scripts. Exiting..."
exit 1
fi

COUNT=`echo "${COUNT}+1" | bc -l`

done
