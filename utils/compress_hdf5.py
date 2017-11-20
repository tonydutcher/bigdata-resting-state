#!/usr/bin/env python
import os
import shutil
import sys
import argparse
import numpy as np

from mvpa2.datasets.mri import fmri_dataset, map2nifti
from mvpa2.mappers.zscore import zscore
from mvpa2.base.hdf5 import h5load, h5save

parser = argparse.ArgumentParser()
parser.add_argument("-s,", metavar="subject", action="store", dest="subject", type=str, required=True, help=('The subject number to be found in the study data directory.') )
args = parser.parse_args()

sname=os.path.basename(args.subject)
outdir=os.path.join(args.subject,"processed")

imgLRo='rfMRI_REST1_LR_hp2000_clean'
imgRLo='rfMRI_REST1_RL_hp2000_clean'

hdfdat_LR=os.path.join(outdir,"%s.hdf5"%imgLRo)
hdfdat_RL=os.path.join(outdir,"%s.hdf5"%imgRLo)
#if os.path.exists(hdfdat_LR):
#    print "loading existing processed hdf5 format data\n"
#    brain_LR = h5load(hdfdat_LR)
#    brain_RL = h5load(hdfdat_RL)
#else:
#    print "No hdf5 data found."
#    assert os.path.exists(hdfdat_LR)

#h5save(os.path.join(outdir,"%s.gzipped.hdf5"%imgLRo), brain_LR, compression=9)
#h5save(os.path.join(outdir,"%s.gzipped.hdf5"%imgLRo), brain_RL, compression=9)

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
