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

cd ${batchdir}

# file names to save output and to launch
basefile=launch_rvr_mask
logfile=${basefile}_RAN_SUBJECTS.log

# launchfile for this batch of subjects
launchfile=${basefile}.sh

echo -e "python ${scriptdir}/test_rvr.py -m /work/04635/adutcher/lonestar/hcp_rest_behav/grouped_raw/non_rsfc/BN_218_2mm_group_rsfc">>${launchfile}
echo -e "python ${scriptdir}/test_rvr.py -m /work/04635/adutcher/lonestar/hcp_rest_behav/grouped_raw/non_rsfc/BN_217_2mm_group_rsfc">>${launchfile}

launch -s ${launchfile} -r 02:00:00 -o ${outdir}/${launchfile%.sh}.o -m amdutcher@utexas.edu -N 1 -n 2 -A ANTS -J ${launchdir}/${launchfile%.sh}_JOBFILE
