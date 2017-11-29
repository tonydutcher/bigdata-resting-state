#!/usr/bin/env python

from mvpa2.datasets.mri import fmri_dataset, map2nifti
from mvpa2.mappers.zscore import zscore
from mvpa2.base.hdf5 import h5load

plotimg='/work/04635/adutcher/lonestar/hcp_rest_behav/grouped_raw/non_rsfc/test_zimg.npy'
source='/work/IRC/ls5/opt/apps/fsl-5.0.9/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'

ds=fmri_dataset(source, mask=source)
