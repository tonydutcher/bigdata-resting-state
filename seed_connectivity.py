#!/usr/bin/env python
import os
import sys
import argparse
import numpy as np

from mvpa2.datasets.mri import fmri_dataset, map2nifti

description="This script runs seed based whole brain correlation for a specific or set of masks using the python package pymvpa"

parser = argparse.ArgumentParser(description=description)

parser.add_argument("-s,", metavar="subject", action="store", dest="subject", type=str, required=True, help=('The subject number to be found in the study data directory.') )

parser.add_argument("-i,", metavar="input-volume", action="store", dest="img", type=str, required=True, help=("The full path to the resting-state volume.") )

parser.add_argument("-m,", metavar="mask", action="store", dest="mask", type=str, required=True, help=("The full path to the mask to use as the seed.") )

parser.add_argument("-b,", metavar="brainmask", action="store", dest="brainmask", type=str, required=True, help=("The full path to the brain mask to be used.") )

parser.add_argument("-d,",  action="store_true", dest="dryrun", default=False, required=False, help=("Run a dry run of the options.") )

args = parser.parse_args()

if args.dryrun:
    print "INPUT ARGUMENTS"
    print "Output directory: %s"%args.subject
    print "Input volume: %s"%args.img
    print "Mask being used: %s"%args.mask
    print "The brainmask: %s"%args.brainmask

# check to make sure each of the files exists. 
assert os.path.exist(args.subject)
assert os.path.exist(args.img)
assert os.path.exist(args.mask)
assert os.path.exist(args.brainmask)

subject='/work/04635/adutcher/lonestar/hcp_rest_behav/subjects/102008'
img='/work/04635/adutcher/lonestar/hcp_rest_behav/subjects/102008/LR/REST1/rfMRI_REST1_LR_hp2000_clean_FILT.nii.gz'
mask='/work/04635/adutcher/lonestar/masks/bn/BN_187_2mm.nii'

# read images - whole brain and mask - into pymvpa
brain = fmri_dataset(img, mask=brainmask)
mask  = fmri_dataset(img, mask=mask)

# standardize the data
brain_ts_array=brain.samples-np.mean(brain.samples, axis=1)
brain_ts_array=brain_ts_array/np.std(brain_ts_array, axis=0)

# take across the voxels in the mask for each time point
mask_ts=np.mean(mask.samples, axis=1)

# 






brain=fmri_dataset(args.img)
mask=fmri_dataset(args.img, mask=args.mask)



