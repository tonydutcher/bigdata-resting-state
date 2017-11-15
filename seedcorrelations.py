"""
import os
import nibabel as nb
import numpy as np
import pandas as pd # TESTING ONLY
from glob import glob
from nilearn.masking import apply_mask
from nilearn.image import new_img_like, mean_img
from nilearn.input_data import NiftiMasker

MASKDIR='/work/04635/adutcher/lonestar/prestonlab/hcp'

class SeedCorrelations(object):
    def __init__(self, subject_dir, verbose=0):
        self.subject_dir = subject_dir
        self.runs_pre = ['REST1', 'REST2']
        self.phases_pre = ['LR', 'RL']
        self.mask_list = {}

        self.mask_list_paths = []
        self.confound_file = os.path.join( self.subject_dir, 'confounds.txt' )
        self.brain_mask = os.path.join( self.subject_dir, 'Brainmask.2.nii.gz' )
        self.imgs_backup = os.path.join( self.subject_dir, 'img_backup' )
        if os.path.exists( self.imgs_backup ):
            os.mkdir( self.imgs_backup )
        # mask object (may or may not be used)
        self.brain_masker = NiftiMasker( mask_strategy='epi',
            smoothing_fwhm=None, detrend=False, standardize=True, t_r=0.72,
            memory='nilearn_cache', memory_level=5, verbose=3 )

        if os.path.exists( self.confound_file ):
            if verbose:
                print "FOUND the confound file. It's always good to double check \
                    to\nmake sure this is the right one and it has the \nright \
                    things in it.\n\n If uncertain rerun create_confounds.sh - \
                    this will create a new file, overwriting an existing file. \
                    \n Use -h option to see usage of create_confounds.sh"
        else:
            print "DID NOT find the confound file, should be 'confounds.txt'\
                \n\n Run create_confounds.sh, see -h usage"


    def find_runs(self, runs=self.runs, phases=self.phases):
        print "finding runs..."
        self.img_files = []
        for phase in self.phases_pre:
            for run in self.runs_pre:
                fname = os.path.join(self.subject_dir,phase,run,'rfMRI_%s_%s_hp2000_clean.nii.gz'%(run,phase))
                if os.path.exists( fname ):
                    print "loading volume: %s"%fname
                    img = nb.load(fname)
                    self.img_files.append(img)
                else:
                    print "%s, volumne does not exist"%fname


    def add_mask(self, mask_name=None, mask_path=None):
        if mask_name is None or mask_path is None:
            print "Must specify mask name and mask path."

        else:
            self.mask_list[mask_name] = os.path.join(subject_dir, 'masks', mask)

    def load_runs(self):
        print "loading data and preprocessing (if necessary)..." 
        self.imgs = np.concatenate( 
[ self.brain_masker.fit_transform(r, confounds=self.confounds_list[i]) for i,r in enumerate(self.img_files) ] )

    def seed_correlation(self, mask_name=None):
        if mask_name is None:
            print "Must specify a mask name to use as seed for whole brain correlation"

        else:
            print "Using %s as seed."%mask_name 
"""

import os
import numpy as np

from mvpa2.tutorial_suite import *
rsn='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100307/LR/REST1/rfMRI_REST1_LR_hp2000_clean_FILT.nii.gz'
bold_fname = rsn
brainmask='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100307/LR/REST1/brainmask_fs.2.nii.gz'
parcelmask='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/atlas/BN_Atlas_246_2mm.nii.gz'

mask_fname = brainmask
mask_fname = parcelmask
import time
start=time.clock()
fds = fmri_dataset(samples=bold_fname,mask=mask_fname)
end=time.clock()
elapsed=end-start
elapsed
