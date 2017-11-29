#!/usr/bin/env python
import os
import shutil
import sys
import argparse
import numpy as np
# np.seterr(divide='ignore', invalid='ignore')

from mvpa2.datasets.mri import fmri_dataset, map2nifti
from mvpa2.mappers.zscore import zscore
from mvpa2.base.hdf5 import h5load

description="This script runs seed based whole brain correlation for a specific or set of masks using the python package pymvpa"

parser = argparse.ArgumentParser(description=description)
parser.add_argument("-s,", metavar="subject", action="store", dest="subject", type=str, required=True, help=('The subject number to be found in the study data directory.') )
parser.add_argument("-m,", metavar="mask", action="store", dest="mask", type=str, required=True, help=("The full path to the mask to use as the seed.") )
parser.add_argument("-it,", metavar="image-type", action="store", dest="imgtype", type=str, required=True, help=("Specify a saved image type to use - .npy, .hdf5, nifti") )
parser.add_argument("-b,", metavar="brainmask", action="store", dest="brainmask", type=str, default='/work/IRC/ls5/opt/apps/fsl-5.0.9/data/standard/MNI152_T1_2mm_brain_mask.nii.gz', required=False, help=("The full path to the brain mask to be used.") )
parser.add_argument("-cr,", metavar="corr-by-run", action="store", dest="corrrun", default="combo", required=False, help=("How to combine correlations across runs - default is to combine") )
parser.add_argument("-con,", metavar="con-image", action="store", dest="confounds", default=False, required=False, help=("Which image type - confound or not? - default confound TRUE") )
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
    print "Using brain image typme: %s"%args.imgtype
    exit()

# get the images different images for confounds
if args.confounds is True:
    print "using confound regressed out images\n"
    img_LR=os.path.join(args.subject,"LR/REST1/rfMRI_REST1_LR_hp2000_clean_FILT_s.nii.gz")
    img_RL=os.path.join(args.subject,"RL/REST1/rfMRI_REST1_RL_hp2000_clean_FILT_s.nii.gz")
    imgLRo='rfMRI_REST1_LR_hp2000_clean_FILT_s'
    imgRLo='rfMRI_REST1_RL_hp2000_clean_FILT_s'

else:
    print "using pure ica images\n"
    img_LR=os.path.join(args.subject,"LR/REST1/rfMRI_REST1_LR_hp2000_clean.nii.gz")
    img_RL=os.path.join(args.subject,"RL/REST1/rfMRI_REST1_RL_hp2000_clean.nii.gz")
    imgLRo='rfMRI_REST1_LR_hp2000_clean'
    imgRLo='rfMRI_REST1_RL_hp2000_clean'

# check to make sure each of the files exists
assert os.path.exists(args.subject)
assert os.path.exists(args.mask)
assert os.path.exists(args.brainmask)

# various variable
maskname="%s_non"%(os.path.basename(args.mask)[:-4])
outdir=os.path.join(args.subject,"processed")
brain_save = os.path.join(outdir, "brain_array_non")
if not os.path.exists(outdir):
    os.mkdir(outdir)

# read images - whole brain and mask - into pymvpa
hdfdat_LR=os.path.join(outdir,"%s.hdf5"%imgLRo)
hdfdat_RL=os.path.join(outdir,"%s.hdf5"%imgRLo)
npybrain=os.path.join(outdir,"brain_array_non.npy")

if args.imgtype == ".npy":
    print "loading existing processed .npy format data\n"    
    print npybrain
    assert os.path.exists(npybrain)
    cat_brain=np.load(npybrain)
    print cat_brain.shape

elif args.imgtype is ".hdf5":
    print "loading existing processed hdf5 format data\n"
    assert os.path.exists(hdfdat_RL)
    assert os.path.exists(hdfdat_LR)
    brain_LR = h5load(hdfdat_LR)
    brain_RL = h5load(hdfdat_RL)

elif args.imgtype is "nifti":
    print "loading and processing in imaging data\n"
    brain_LR = fmri_dataset(img_LR, mask=args.brainmask)
    brain_RL = fmri_dataset(img_RL, mask=args.brainmask)
    N, P = brain_LR.samples.shape
    brain_LR.sa['chunks']=['rest']*N
    brain_RL.sa['chunks']=['rest']*N
    zscore(ds=brain_LR,dtype='float32')
    zscore(ds=brain_RL,dtype='float32')

else:
    print "Error with imgtype specification - something slipped through."
    exit()

# get the mask data 
print "gathering mask data"
sname=os.path.basename(args.subject)
scratch_LR="/scratch/04635/adutcher/lonestar/hcp_112017/%s/LR/REST1/rfMRI_REST1_LR_hp2000_clean.nii.gz"%(sname)
scratch_LR="/scratch/04635/adutcher/lonestar/hcp_112017/%s/RL/REST1/rfMRI_REST1_RL_hp2000_clean.nii.gz"%(sname)
mask_LR = fmri_dataset(img_LR, mask=args.mask)
mask_RL = fmri_dataset(img_RL, mask=args.mask)
N = mask_LR.shape[0]

# standardize the data
# - need the chunks attribute to zscore the data
mask_LR.sa['chunks']=['rest']*N
mask_RL.sa['chunks']=['rest']*N

print "zscoring imaging data\n"
zscore(ds=mask_LR,dtype='float32')
zscore(ds=mask_RL,dtype='float32')

# saving hdf5 data objects
if not args.imgtype == ".npy":
    print "saving hdf5 data objects in %s"%outdir
    if not os.path.exists(hdfdat_LR):
        brain_LR.save( hdfdat_LR )
    if not os.path.exists(hdfdat_RL):
        brain_RL.save( hdfdat_RL )

# we need to ouput this correlation across all voxels to a single vector 
# I am assuming that the voxel vector from the correlation with the mask will be the
# same MNI locations - NEED TO CHECK THIS!

# concatenate LR and RL phase encoding directions or not - there may be
# effects combining across different phase encoding directions. 

if args.corrrun is "sep":
    # save a .npy array of the brain
    brain_save_LR = os.path.join(outdir, "brain_array_LR")
    if not os.path.exists( brain_save_LR ):
        np.save( brain_save_LR, brain_LR.samples )

    # save a .npy array of the brain
    brain_save_RL = os.path.join(outdir, "brain_array_RL")
    if not os.path.exists( brain_save_RL ):
        np.save( brain_save_RL, brain_RL.samples )
    
    print "running resting-state correlations with mask separatly for each run\n"
    # save a correlations matrix for within mask correlation
    np.save( "%s_corr_LR"%(os.path.join(outdir, maskname)), np.corrcoef(mask_LR.samples.T) )
    np.save( "%s_corr_RL"%(os.path.join(outdir, maskname)), np.corrcoef(mask_RL.samples.T) )

    # calculate the correlation between different runs
    print "saving within mask correaltion matrix for each run"
    mask_mts_LR=np.mean( mask_LR.samples, axis=1)
    mask_mts_RL=np.mean( mask_RL.samples, axis=1)
    np.save( "%s_mean_LR"%(os.path.join(outdir,maskname)), mask_mts_LR )
    np.save( "%s_mean_RL"%(os.path.join(outdir,maskname)), mask_mts_RL )

    # initialize variables for
    print "running the correlation using np.corrcoef"
    rsfc_LR=np.zeros([1,P])
    rsfc_RL=np.zeros([1,P])
    for v in np.arange(P):
        rsfc_LR[0,v]=np.corrcoef( mask_mts_LR, brain_LR.samples )
        rsfc_RL[0,v]=np.corrcoef( mask_mts_RL, brain_RL.samples )
    
    # save the variables separately.
    print "saving rsfc files (plural) in %s"%outdir
    np.save( os.path.join(outdir,"%s_rsfc_LR"%maskname), rsfc_LR)
    np.save( os.path.join(outdir,"%s_rsfc_RL"%maskname), rsfc_RL)

elif args.corrrun is "combo":
    print "running resting-state correlations with mask - concatenating  runs\n"
    if not args.imgtype == ".npy":
        cat_brain = np.vstack([brain_LR.samples, brain_RL.samples])
        # save a .npy array of the brain
        brain_save = os.path.join(outdir, "brain_array_non")
        if not os.path.exists( brain_save ):    
            np.save( brain_save, cat_brain )
    
    # create and save a .npy array of the mask
    cat_mask  = np.vstack([mask_LR.samples, mask_RL.samples])
    mask_save = os.path.join(outdir, "%s_array_non"%maskname)
    if not os.path.exists( mask_save ):
        np.save( mask_save, cat_mask )

    # save a correlations matrix for within mask correlation
    print "saving within mask correaltion matrix concatenating runs"
    np.save("%s_corr"%(os.path.join(outdir,maskname)), np.corrcoef(cat_mask.T) )

    # take across the voxels in the mask for each time point
    cat_mask_mts=np.mean( cat_mask, axis=1)
    np.save( "%s_mean"%(os.path.join(outdir,maskname)), cat_mask_mts )
    
    # run the correlation
    P=cat_brain.shape[1]
    rsfc=np.zeros([1,P])
    print "running the correlation using np.corrcoef"
    for v in np.arange(P):
        rsfc[0,v]=np.corrcoef(cat_mask_mts, cat_brain[:,v])[0,1]
    
    print "saving rsfc file in %s"%outdir
    np.save( os.path.join(outdir,"%s_rsfc"%(maskname)), rsfc)

if not args.imgtype == ".npy":
    # again, issues with size so moving to scratch
    scratchdir_LR="/scratch/04635/adutcher/lonestar/hcp_112017/%s/LR/REST1/"%(sname)
    if os.path.exists( os.path.join(scratchdir_LR, "%s.hdf5"%imgLRo) ) and os.path.exists( hdfdat_LR ):
        file_to_overwrite=os.path.join(scratchdir_LR, "%s.hdf5"%imgLRo)
        if os.path.exists( file_to_overwrite ):
            print "Found existing LR file on scratch - removing to move new file over."
            os.remove( file_to_overwrite )

        print "moving %s for %s"%(imgLRo,sname)
        shutil.move( hdfdat_LR, scratchdir_LR )
    else:
        print "NO %s for %s found"%(imgLRo,sname)

    scratchdir_RL="/scratch/04635/adutcher/lonestar/hcp_112017/%s/RL/REST1/"%(sname)
    if os.path.exists( os.path.join(scratchdir_RL, "%s.hdf5"%imgRLo) ) and os.path.exists( hdfdat_RL ):
        file_to_overwrite=os.path.join(scratchdir_RL, "%s.hdf5"%imgRLo)
        if os.path.exists( file_to_overwrite ):
            print "Found existing RL file on scratch - removing to move new file over."
            os.remove( file_to_overwrite )

        print "moving %s for %s"%(imgRLo,sname)
        shutil.move( hdfdat_RL, scratchdir_RL )
    else:
        print "NO %s for %s found"%(imgRLo,sname)

else:
    print "Skipping the whole hdf5 save thing\n"

