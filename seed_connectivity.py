#!/usr/bin/env python
import os
import sys
import argparse
import numpy as np

from mvpa2.datasets.mri import fmri_dataset, map2nifti
from mvpa2.mappers.zscore import zscore
from mvpa2.base.hdf5 import h5load

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
    print "using confound regressed out images\n"
    img_LR=os.path.join(args.subject,"LR/REST1/rfMRI_REST1_LR_hp2000_clean_FILT_s.nii.gz")
    img_RL=os.path.join(args.subject,"RL/REST1/rfMRI_REST1_RL_hp2000_clean_FILT_s.nii.gz")
    assert os.path.exists(img_LR)
    assert os.path.exists(img_RL)

else:
    print "using pure ica images\n"
    img_LR=os.path.join(args.subject,"LR/REST1/rfMRI_REST1_LR_hp2000_clean.nii.gz")
    img_RL=os.path.join(args.subject,"RL/REST1/rfMRI_REST1_RL_hp2000_clean.nii.gz")
    assert os.path.exists(img_LR)
    assert os.path.exists(img_RL)

# check to make sure each of the files exists
assert os.path.exists(args.subject)
assert os.path.exists(args.mask)
assert os.path.exists(args.brainmask)

# various variable
maskname=os.path.basename(args.mask)[:-4]
outdir=os.path.join(args.subject,"processed")
if not os.path.exists(outdir):
    os.mkdir(outdir)

# read images - whole brain and mask - into pymvpa
hdfdat_LR=os.path.join(outdir,'rfMRI_REST1_LR_hp2000_clean_FILT_s.hdf5')
hdfdat_RL=os.path.join(outdir,'rfMRI_REST1_RL_hp2000_clean_FILT_s.hdf5')
if os.path.exists(hdfdat_LR):
    print "loading existing processed hdf5 format data\n"
    brain_LR = h5load(hdfdat_LR)
    brain_RL = h5load(hdfdat_RL)

else:
    print "loading and processing in imaging data\n"
    brain_LR = fmri_dataset(img_LR, mask=args.brainmask)
    brain_RL = fmri_dataset(img_RL, mask=args.brainmask)

# get the mask data 
print "gathering mask data"
mask_LR = fmri_dataset(img_LR, mask=args.mask)
mask_RL = fmri_dataset(img_RL, mask=args.mask)
N, P = brain_LR.samples.shape

# standardize the data
# - need the chunks attribute to zscore the data
brain_LR.sa['chunks']=['rest']*N
brain_RL.sa['chunks']=['rest']*N
mask_LR.sa['chunks']=['rest']*N
mask_RL.sa['chunks']=['rest']*N

print "zscoring imaging data\n"
zscore(ds=brain_LR,dtype='float32')
zscore(ds=brain_RL,dtype='float32')
zscore(ds=mask_LR,dtype='float32')
zscore(ds=mask_RL,dtype='float32')

# saving hdf5 data objects
print "saving hdf5 data objects in %s"%outdir
brain_LR.save( os.path.join(outdir,'rfMRI_REST1_LR_hp2000_clean_FILT_s.hdf5') )
brain_RL.save( os.path.join(outdir,'rfMRI_REST1_RL_hp2000_clean_FILT_s.hdf5') )

# we need to ouput this correlation across all voxels to a single vector 
# I am assuming that the voxel vector from the correlation with the mask will be the
# same MNI locations - NEED TO CHECK THIS!

# concatenate LR and RL phase encoding directions or not - there may be
# effects combining across different phase encoding directions. 

if args.corrrun is "sep":
    print "running resting-state correlations with mask separatly for each run\n"
    # save a correlations matrix for within mask correlation
    np.save( "%s_corr_LR_FILT_s"%(os.path.join(outdir, maskname)), np.corrcoef(mask_LR.samples.T) )
    np.save( "%s_corr_RL_FILT_s"%(os.path.join(outdir, maskname)), np.corrcoef(mask_RL.samples.T) )

    # calculate the correlation between different runs
    print "saving within mask correaltion matrix for each run"
    mask_mts_LR=np.mean( mask_LR.samples, axis=1)
    mask_mts_RL=np.mean( mask_RL.samples, axis=1)
    np.save( "%s_mean_LR_FILT_s"%(os.path.join(outdir,maskname)), mask_mts_LR )
    np.save( "%s_mean_RL_FILT_s"%(os.path.join(outdir,maskname)), mask_mts_RL )
    # initialize variables for
    print "running the correlation using np.corrcoef"
    rsfc_LR=np.zeros([1,P])
    rsfc_RL=np.zeros([1,P])
    for v in np.arange(P):
        rsfc_LR[0,v]=np.corrcoef( mask_mts_LR, brain_LR.samples )
        rsfc_RL[0,v]=np.corrcoef( mask_mts_RL, brain_RL.samples )
    
    # save the variables separately.
    print "saving rsfc files (plural) in %s"%outdir
    np.save( os.path.join(outdir,"_rsfc_LR_FILT_s"%maskname), rsfc_LR)
    np.save( os.path.join(outdir,"_rsfc_RL_FILT_s"%maskname), rsfc_RL)

elif args.corrrun is "combo":
    print "running resting-state correlations with mask - concatenating  runs\n"
    cat_brain = np.vstack([brain_LR.samples, brain_RL.samples])
    cat_mask  = np.vstack([mask_LR.samples, mask_RL.samples])
    
    # save a correlations matrix for within mask correlation
    print "saving within mask correaltion matrix concatenating runs"
    np.save("%s_corr_FILT_s"%(os.path.join(outdir,maskname)), np.corrcoef(cat_mask.T) )

    # take across the voxels in the mask for each time point
    cat_mask_mts=np.mean( cat_mask, axis=1)
    np.save( "%s_mean_FILT_s"%(os.path.join(outdir,maskname)), cat_mask_mts )
    
    # run the correlation
    rsfc=np.zeros([1,P])
    print "running the correlation using np.corrcoef"
    for v in np.arange(P):
        rsfc[0,v]=np.corrcoef(cat_mask_mts, cat_brain[:,v])[0,1]
    
    print "saving rsfc file in %s"%outdir
    np.save( os.path.join(outdir,"_rsfc_FILT_s"%maskname), rsfc)

# again, issues with size so moving files out.
print "moving non-hdf5 data into scratch :("
sname=os.basename(args.subject)
os.rename(img_LR, "/scratch/04635/adutcher/lonestar/hcp_112017/%s/LR/REST1/"%(sname))

