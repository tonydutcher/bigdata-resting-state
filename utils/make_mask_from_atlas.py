#!/usr/bin/env python
import os
import sys
import argparse
import numpy as np

from mvpa2.datasets.mri import fmri_dataset, map2nifti

parser = argparse.ArgumentParser(description="Create masks from atlas")

parser.add_argument("-o", metavar="out-dir", action="store", dest="outdir", type=str, required=True, help=('The fullpath to the output directory - where to put these masks.') )

parser.add_argument("-i", metavar="in-atlas", action="store", dest="atlas_name", type=str, required=True, help=("The fullpath to the atlas being used.") )

parser.add_argument("-n", metavar="N-rois", action="store", dest="n_rois", type=int, required=True, help=("Number of ROIs in atlas.") )

parser.add_argument("-p", metavar="mask-prefix", action="store", dest="mask_prefix", type=str, required=True, help=("The prefix to each mask ROI output.") )

parser.add_argument("-d",  action="store_true", dest="dryrun", default=False, required=False, help=("Run a dry run of the options.") )

args = parser.parse_args()

if args.dryrun:
    print "INPUT ARGUMENTS:"
    print "Output directory:%s"%args.outdir
    print "Atlas being used: %s"%args.atlas_name
    print "Number of ROIs in atlas: %03d"%args.n_rois
    print "Mask prefix on individual mask images: %s"%args.mask_prefix

atlas = fmri_dataset(samples=args.atlas_name)

for i in np.arange(1,args.n_rois+1):
    tmp=atlas.copy()
    tmp.samples=(tmp.samples==i).astype(int)
    tmpimg = map2nifti(tmp)
    fname=os.path.join(args.outdir,'%s_%03d_2mm.nii'%(args.mask_prefix,i ) )
    if args.dryrun:
        print "There appears to be no errors - will save mask %03d as %s"%(i, fname)
    else:
        tmpimg.to_filename( fname )
