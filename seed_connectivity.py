#!/usr/bin/env python
import os
import shutil
import sys
import argparse
import numpy as np
import nibabel as nb
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
parser.add_argument("-con,", action="store_true", dest="confounds", default=True, required=False, help=("Which image type - confound or not? - default confound TRUE") )
parser.add_argument("-d,",  action="store_true", dest="dryrun", default=False, required=False, help=("Run a dry run of the options.") )
args = parser.parse_args()

## DESCRIBE THE DATA THAT IS BEING USED.
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
if args.confounds and args.imgtype == 'nifti':
    print "Using confound regressed out images for seed correlation."
    img_LR=os.path.join(args.subject,"LR/REST1/rfMRI_REST1_LR_hp2000_clean_FILT_s.nii.gz")
    img_RL=os.path.join(args.subject,"RL/REST1/rfMRI_REST1_RL_hp2000_clean_FILT_s.nii.gz")
    imgLRo='rfMRI_REST1_LR_hp2000_clean_FILT_s'
    imgRLo='rfMRI_REST1_RL_hp2000_clean_FILT_s'
    assert os.path.exists(img_LR)
    assert os.path.exists(img_RL)

elif args.imgtype == 'nifti':
    print "Using pure ica images for seed correlation."
    img_LR=os.path.join(args.subject,"LR/REST1/rfMRI_REST1_LR_hp2000_clean.nii.gz")
    img_RL=os.path.join(args.subject,"RL/REST1/rfMRI_REST1_RL_hp2000_clean.nii.gz")
    imgLRo='rfMRI_REST1_LR_hp2000_clean'
    imgRLo='rfMRI_REST1_RL_hp2000_clean'
    assert os.path.exists(img_LR)
    assert os.path.exists(img_RL)

elif args.imgtype == 'npy':
    print "NOT using nifti images for analysis"    

else:
   print "Error in specifying brain images to be used for analysis."
   exit()

# check to make sure each of the files exists
assert os.path.exists(args.subject)
assert os.path.exists(args.mask)
assert os.path.exists(args.brainmask)

# hard coded mask name variable can be soft coded around the . split.
raw_maskname="%s"%(os.path.basename(args.mask))
if raw_maskname[-1]=='z':
    maskname="%s"%(raw_maskname[:-7])
elif raw_maskname[-1]=='i':
    maskname="%s"%(raw_maskname[:-4])
else:
    print "Check mask name variable - continuing..."

# ouput directory for seed connectivity and brain array name
outdir=os.path.join(args.subject,"processed")
brain_save=os.path.join(outdir,"brain_array")
if not os.path.exists(outdir):
    os.mkdir(outdir)

npybrain = os.path.join(outdir,"brain_array.npy")
maskpref = os.path.join(outdir,"%s_array_con-4mm"%maskname)
## DESCRIBE THE DATA THAT IS BEING USED.



## READ IN AND PROCESS BRAIN AND MASK DATA
# BRAIN DATA
if args.imgtype == 'npy':
    print "Loading existing processed .npy format data - already z-scored"    
    print npybrain
    assert os.path.exists(npybrain)
    cat_brain=np.load(npybrain)

else:
    print "Loading and processing in imaging data"
    brain_LR = fmri_dataset(img_LR, mask=args.brainmask)
    brain_RL = fmri_dataset(img_RL, mask=args.brainmask)
    N, P = brain_LR.samples.shape

    print "z-scoring the loaded imaging data."
    brain_LR.sa['chunks']=['rest']*N
    brain_RL.sa['chunks']=['rest']*N
    zscore(ds=brain_LR,dtype='float32')
    zscore(ds=brain_RL,dtype='float32')
    cat_brain = np.vstack([brain_LR.samples, brain_RL.samples])

# BRAIN DATA

# MASK DATA
print "Gathering mask data"
sname=os.path.basename(args.subject)

if args.imgtype == 'npy':
    print "Getting mask information from a saved/processed npy array."
    assert os.path.exists(npybrain)
    mask  = fmri_dataset(args.mask, mask=args.brainmask)
    index = mask.samples[0,:]!=0
    cat_mask = cat_brain[:,index]
    print cat_mask.shape
    cat_mask_mts = np.mean( cat_mask, axis=1)
    print cat_mask_mts.shape

else:
    print "Getting mask information from nifti brain images."
    mask_LR = fmri_dataset(img_LR, mask=args.mask)
    mask_RL = fmri_dataset(img_RL, mask=args.mask)

    # standardize the data
    # - need the chunks attribute to zscore the data
    mask_LR.sa['chunks']=['rest']*N
    mask_RL.sa['chunks']=['rest']*N
    
    print "zscoring imaging data"
    zscore(ds=mask_LR,dtype='float32')
    zscore(ds=mask_RL,dtype='float32')
    cat_mask = np.vstack([mask_LR.samples, mask_RL.samples])
    cat_mask_mts = np.mean( cat_mask, axis=1)

# save brain npy if it does not exist
if not os.path.exists( npybrain ):
    print "Saving a brain array"
    np.save( npybrain, cat_brain )
else:
    print "Found a previous .npy brain array, not overwriting."
    
# save a mask time-series .npy if it does not exist
if not os.path.exists( maskpref ):
    print "Saving a mask array."
    np.save( maskpref, cat_mask )
else:
    print "Found a previous .npy brain array, not overwriting."
    
# save a .txt file of mask mean time-series.
print "Saving a mean time-series mask in a .txt file."
np.savetxt( "%s_mean.txt"%maskpref, cat_mask_mts )
## READ IN AND PROCESS BRAIN AND MASK DATA



## RUN THE CORRELATION
print "Running resting-state seed correlations with the rest of the brain, see numpyp.corrcoef()."
P=cat_brain.shape[1]
rsfc=np.zeros([1,P])
for v in np.arange(P):
    rsfc[0,v]=np.corrcoef(cat_mask_mts, cat_brain[:,v])[0,1]
## RUN THE CORRELATION



## SAVE OUTPUT FROM THE CORRELATION
print "Saving rsfc .npy and .nii.gz file in %s"%outdir
np.save( os.path.join(outdir,"%s_rsfc"%(maskpref)), rsfc)
mnispace  = fmri_dataset( args.brainmask, mask=args.brainmask )
mnirsfc   = mnispace.a.mapper.reverse( rsfc )
nimg      = nb.Nifti1Image( mnirsfc, mnispace.a.imgaffine )
nimg.to_filename(os.path.join(outdir,"%s_rsfc.nii.gz"%(maskpref)))
## SAVE OUTPUT FROM THE CORRELATION



## MOVE FILES AWAY
if not args.imgtype == 'npy' and os.path.exists( npybrain ):
    # again, issues with size so moving to scratch
    scratchdir_LR="/scratch/04635/adutcher/lonestar/hcp_112017/%s/LR/REST1"%(sname)
    if os.path.exists( scratchdir_LR ):
        file_to_overwrite=os.path.join(scratchdir_LR, "%s.nii.gz"%imgLRo)
        if os.path.exists( file_to_overwrite ):
            print "Found existing LR file on scratch - removing to move new file over." 
            os.remove( file_to_overwrite )

        print "moving %s for %s"%(imgLRo,sname)
        shutil.move( img_LR, scratchdir_LR )
    else:
        print "NO %s for %s found"%(imgLRo,sname)

    scratchdir_RL="/scratch/04635/adutcher/lonestar/hcp_112017/%s/RL/REST1"%(sname)
    if os.path.exists( scratchdir_RL ):
        file_to_overwrite=os.path.join(scratchdir_RL, "%s.nii.gz"%imgRLo)
        if os.path.exists( file_to_overwrite ):
            print "Found existing RL file on scratch - removing to move new file over."
            os.remove( file_to_overwrite )

        print "moving %s for %s"%(imgRLo,sname)
        shutil.move( img_RL, scratchdir_RL )
    else:
        print "NO %s for %s found"%(imgRLo,sname)

else:
    print "Skipping the moving of data."
## MOVE FILES AWAY
