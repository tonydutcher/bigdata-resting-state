#!/usr/bin/env python
import os
import sys
import argparse
import numpy as np

from mvpa2.datasets.mri import fmri_dataset, map2nifti

description="This script runs seed based whole brain correlation for a specific subject.\n\
Input\n
-s, subject - full path to subject directory\n\
-i, input   - full path to input resting-state volume\n\
-m, mask    - fill path to a mask or : separated list of masks\n"

parser = argparse.ArgumentParser(description=description)

parser.add_argument("-s", metavar="subject", action="store", dest="subject", type=str, required=True, help=('The subject number to be found in the study data directory.') )

parser.add_argument("-m", metavar="seed-mask", action="store", dest="seed", type=str, required=True, help=("The full path to the mask to use as the seed.") )

parser.add_argument("-d",  action="store_true", dest="dryrun", default=False, required=False, help=("Run a dry run of the options.") )

args = parser.parse_args()

if args.dryrun:
    print "INPUT ARGUMENTS:"
    print "Output directory:%s"%args.subject
    print "Mask being used: %s"%args.seed

class SeedCorrelations(object):
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
