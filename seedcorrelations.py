#!/usr/bin/env python
import os
import sys
import numpy as np

from mvpa2.datasets.mri import fmri_dataset, map2nifti

Class SeedCorrelations(object):
    def __init__(self, subject, verbose=0):
        self.subject_dir = os.path.join('/work/04635/adutcher/lonestar/hcp_behav_rest/subjects/%s'%str(subject) )
        self.runs_pre = ['REST1', 'REST2']
        self.phases_pre = ['LR', 'RL']
        self.mask_list = {}
        self.mask_list_paths = []
        self.confound_file = os.path.join( self.subject_dir, 'confounds.txt' )
        self.brain_mask = os.path.join( self.subject_dir, 'Brainmask.2.nii.gz' )
        self.imgs_backup = os.path.join( self.subject_dir, 'img_backup' )
        if os.path.exists( self.imgs_backup ):
            os.mkdir( self.imgs_back


    def find_runs(self, runs=self.runs, phases=self.phases):
        print "finding runs..."
        self.img_files = []
        for phase in self.phases_pre:
            for run in self.runs_pre:
                fname = os.path.join(self.subject_dir,phase,run,'rfMRI_%s_%s_hp2000_clean_FILT.nii.gz'%(run,phase))
                if os.path.exists( fname ):
                    print "loading volume: %s"%fname
                    imgs = fmri_dataset(fname).samples
                    self.img_files.append(img)
                else:
                    print "%s, volumne does not exist"%fname


    def add_mask(self, mask_name=None, mask_path=None):
        if mask_name is None or mask_path is None:
            print "Must specify mask name and mask path."

        else:
            self.mask_list[mask_name] = os.path.join(subject_dir, 'masks', mask)
