

subjectdir=/work/04635/adutcher/lonestar/hcp_rest_behav/subjects
maskdir=/work/04635/adutcher/lonestar/masks/bn
s=100307
m=BN_002_2mm.nii
b=masks/brain2mm_thr065.nii.gz
python seed_connectivity.py -s ${subjectdir}/${s} -m ${maskdir}/${m} -b ${subjectdir}/${s}/${b}

