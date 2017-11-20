#!/bin/bash
subjectdir=/work/04635/adutcher/lonestar/hcp_rest_behav/subjects
maskdir=/work/04635/adutcher/lonestar/masks/bn
m1=BN_016_2mm.nii
m2=BN_017_2mm.nii
python seed_connectivity.py -s ${subjectdir}/100307 -m ${maskdir}/${m1} -it ".npy"
python seed_connectivity.py -s ${subjectdir}/100307 -m ${maskdir}/${m2}
