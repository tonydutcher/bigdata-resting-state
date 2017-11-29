#!/bin/bash

# study specific paths
subdir=/work/04635/adutcher/lonestar/hcp_rest_behav/subjects
maskdir=/work/04635/adutcher/lonestar/masks/bn
outdir=/work/04635/adutcher/lonestar/hcp_rest_behav/logs
scriptdir=/home1/04635/adutcher/analysis/hcp_rest_behav
batchdir=/work/04635/adutcher/lonestar/hcp_rest_behav/batch
launchdir=/work/04635/adutcher/lonestar/hcp_rest_behav/batch/launch
m1=BN_179_2mm.nii
m2=BN_180_2mm.nii
m3=BN_178_2mm.nii
m4=BN_177_2mm.nii
m5=BN_029_2mm.nii
m6=BN_030_2mm.nii
m7=BN_218_2mm.nii
m8=BN_217_2mm.nii

cd ${subdir}
subjects=`ls -d ??????`

cd ${batchdir}
count=1
batchnum=1

# file names to save output and to launch
basefile=launch_seed_connectivity_8-masks_batch_
logfile=${basefile}_RAN_SUBJECTS.log

# removes any files by this name in batch dir
if [ -f ${basefile}_1.sh ]; then
echo " "
echo "Removing the existing ${basefile}* from batch directory."
echo " "

rm launch_seed_connectivity_8-masks_batch_*.sh
#echo " "
#echo "Must remove ${basefile}* files from batch directory."
#echo " "
#exit 1
fi

# cycle through roi list
for s in ${subjects[@]}; do
echo $s

# launchfile for this batch of subjects
launchfile=${basefile}_${batchnum}.sh

echo -e "python ${scriptdir}/seed_connectivity.py -s ${subdir}/${s} -m ${maskdir}/${m1} -it '.npy'">>${launchfile}
echo -e "python ${scriptdir}/seed_connectivity.py -s ${subdir}/${s} -m ${maskdir}/${m2} -it '.npy'">>${launchfile}
echo -e "python ${scriptdir}/seed_connectivity.py -s ${subdir}/${s} -m ${maskdir}/${m3} -it '.npy'">>${launchfile}
echo -e "python ${scriptdir}/seed_connectivity.py -s ${subdir}/${s} -m ${maskdir}/${m4} -it '.npy'">>${launchfile}
echo -e "python ${scriptdir}/seed_connectivity.py -s ${subdir}/${s} -m ${maskdir}/${m5} -it '.npy'">>${launchfile}
echo -e "python ${scriptdir}/seed_connectivity.py -s ${subdir}/${s} -m ${maskdir}/${m6} -it '.npy'">>${launchfile}
echo -e "python ${scriptdir}/seed_connectivity.py -s ${subdir}/${s} -m ${maskdir}/${m7} -it '.npy'">>${launchfile}
echo -e "python ${scriptdir}/seed_connectivity.py -s ${subdir}/${s} -m ${maskdir}/${m8} -it '.npy'">>${launchfile}

# keep 16 subjects within a single launch script
if [ ${count} -eq 15 ]; then
echo ${batchnum}

if [ ${batchnum} -ge 0 ]; then
launch -s ${launchfile} -r 03:45:00 -o ${outdir}/${launchfile%.sh}.o -m amdutcher@utexas.edu -N 1 -n 3 -A ANTS -J ${launchdir}/${launchfile%.sh}_JOBFILE
fi
batchnum=`echo "${batchnum}+1 " | bc -l`
count=1
fi

#
if [ ${batchnum} -eq 30 ];then
echo "Reached 30 slurm scripts. Exiting..."
exit 1
fi

count=`echo "${count}+1" | bc -l`

done
