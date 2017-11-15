#!/usr/bin/python

import sys
import argparse
import nibabel as nb

parser = argparse.ArgumentParser()
parser.add_argument("outdir", )
parser.add_argument("atlas")
parser.add_argument("rois")
parser.add_argument("maskpre")
args = parser.parse_args()

print args.outdir
print args.atlas
print args.rois
print args.maskpre

"""
atlas = fmri_dataset(samples=atlas_name)

for i in np.arange(0,n_rois):
    tmp=atlas.copy()
    tmp.samples=(tmp.samples==i).astype(int)
    tmpimg = map2nifti(tmp)
    tmpimg.to_filename( os.path.join(maskdir,'%s_%03d.nii'%(mask_prefixes,i ) ) )
"""
