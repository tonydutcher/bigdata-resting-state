#!/usr/bin/env python
import os
import sys
import argparse
import numpy as np

from mvpa2.datasets.mri import fmri_dataset, map2nifti
from mvpa2.mappers.zscore import zscore

description="This script runs seed based whole brain correlation for a specific or set of masks using the python package pymvpa"

parser = argparse.ArgumentParser(description=description)
parser.add_argument("-s,", metavar="subject", action="store", dest="subject", type=str, required=True, help=('The subject number to be found in the study data directory.') )
parser.add_argument("-m,", metavar="mask", action="store", dest="mask", type=str, required=True, help=("The full path to the mask to use as the seed.") )
parser.add_argument("-b,", metavar="brainmask", action="store", dest="brainmask", type=str, required=True, help=("The full path to the brain mask to be used.") )
parser.add_argument("-cr,", metavar="corr-by-run", action="store", dest="corrrun", default="combo", required=False, help=("How to combine correlations across runs - default is to combine") )
parser.add_argument("-con,", metavar="con-image", action="store", dest="confounds", default=True, required=False, help=("Which image type - confound or not? - default confound TRUE") )
parser.add_argument("-d,",  action="store_true", dest="dryrun", default=False, required=False, help=("Run a dry run of the options.") )
args = parser.parse_args()

# prints for dry run
if args.dryrun:
    print "INPUT ARGUMENTS"
    print "Subject directory: %s"%args.subject
    print "Mask being used: %s"%args.mask
    print "The brainmask: %s"%args.brainmask
    print "Running correlation across runs: %s"%args.corrrun
    print "Using confounds: %s"%args.confounds

# get the images different images for confounds
if args.confounds:
    img_LR=os.path.join(args.subject,"LR/REST1/rfMRI_REST1_LR_hp2000_clean.nii.gz")
    img_RL=os.path.join(args.subject,"RL/REST1/rfMRI_REST1_RL_hp2000_clean.nii.gz")
    assert os.path.exists(img_LR)
    assert os.path.exists(img_RL)
else:
    img_LR=os.path.join(args.subject,"LR/REST1/rfMRI_REST1_LR_hp2000_clean.nii.gz")
    img_RL=os.path.join(args.subject,"RL/REST1/rfMRI_REST1_RL_hp2000_clean.nii.gz")
    assert os.path.exists(img_LR)
    assert os.path.exists(img_RL)

# check to make sure each of the files exists
assert os.path.exists(args.subject)
assert os.path.exists(args.mask)
assert os.path.exists(args.brainmask)

# various variable
maskname=os.path.basename(mask)[:-4]
outdir=os.path.join(args.subject,"processed")
if not os.path.exists(outdir):
    os.mkdir(outdir)

# read images - whole brain and mask - into pymvpa
brain_LR = fmri_dataset(img_LR, mask=mask2)
brain_RL = fmri_dataset(img_RL, mask=mask2)
mask_LR = fmri_dataset(img_LR, mask=mask)
mask_RL = fmri_dataset(img_RL, mask=mask)
N, P = brain_LR.samples.shape

# standardize the data
# - need the chunks attribute to zscore the data
brain_LR.sa['chunks']=['rest']*N
brain_RL.sa['chunks']=['rest']*N
mask_LR.sa['chunks']=['rest']*N
mask_RL.sa['chunks']=['rest']*N
zscore(ds=brain_LR,dtype='float32')
zscore(ds=brain_RL,dtype='float32')
zscore(ds=mask_LR,dtype='float32')
zscore(ds=mask_RL,dtype='float32')

# we need to ouput this correlation across all voxels to a single vector 
# I am assuming that the voxel vector from the correlation with the mask will be the
# same MNI locations - NEED TO CHECK THIS!

# concatenate LR and RL phase encoding directions or not - there may be
# effects combining across different phase encoding directions. 
if args.corrrun is "sep":
    # save a correlations matrix for within mask correlation
    np.save( np.corrcoef(mask_RL.samples.T) )
    np.save( np.corrcoef(mask_LR.samples.T) )

    # calculate the correlation between different runs
    mask_mts_LR=np.mean( mask_LR.samples, axis=1)
    mask_mts_RL=np.mean( mask_RL.samples, axis=1)

    # initialize variables for 
    rsfc_LR=np.zeros([1,P])
    rsfc_RL=np.zeros([1,P])
    for v in np.arange(P):
        rsfc_LR[0,v]=np.corrcoef( mask_mts_LR, brain_LR.samples )
        rsfc_RL[0,v]=np.corrcoef( mask_mts_RL, brain_RL.samples )
    
    # save the variables separately. 
    np.save( os.path.join(outdir,"_LR"%maskname), rsfc_LR)
    np.save( os.path.join(outdir,"_RL"%maskname), rsfc_RL)

elif args.corrrun is "combo":
    cat_brain = np.vstack([brain_LR.samples, brain_RL.samples])
    cat_mask  = np.vstack([mask_LR.samples, mask_RL.samples])
    
    # save a correlations matrix for within mask correlation
    np.save("", np.corrcoef(cat_mask.T) )

    # take across the voxels in the mask for each time point
    cat_mask_mts=np.mean( cat_mask, axis=1)

    # run the correlation
    rsfc=np.zeros([1,P])
    for v in np.arange(P):
        rsfc[0,v]=np.corrcoef(cat_mask_mts, cat_brain[:,v])[0,1]
    
    np.save(os.path.join(outdir,maskname), rsfc)
