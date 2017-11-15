#!/usr/bin/python

import os
import numpy as np
import nibabel as nb

from seedcorrelations import SeedCorrelations
from nilearn.input_data import NiftiMasker

subject_dir='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100206'
runs=['REST1', 'REST2']
phases=['LR', 'RL']

def find_confound_files(subject_dir, runs, phases):
	confound_files=[]
	for phase in phases:
		for run in runs:
			fname=os.path.join( subject_dir, phase, run, 'confounds.txt' )
			if os.path.exists( os.path.join( fname ) ):
				confound_files.append( os.path.join( subject_dir, phase, run, 'confounds.txt' ) )
	return confound_files



def find_runs(subject_dir, runs, phases):
        print "finding runs..."
        imgs=[]
	img_fnames=[]
        for phase in phases:
		for run in runs:
                	fname = os.path.join(subject_dir,phase,run,'rfMRI_%s_%s_hp2000_clean.nii.gz'%(run,phase))
			if os.path.exists( fname ):
                    		print "loading volume: %s"%fname
                    		img = nb.load(fname)
				img_fnames.append(fname)
                    		imgs.append(img)
                	else:
                    		print "%s, volumne does not exist"%fname
	return img_fnames, imgs



def load_runs(images,brain_masker,confounds_list):
	print "loading data and preprocessing (if necessary)..." 
	imgs = np.concatenate([brain_masker.fit_transform(r,confounds=confounds_list[i]) for i,r in enumerate(images)])
	return imgs

"""
def seed_correlation(self, mask_name=None):
if mask_name is None:
print "Must specify a mask name to use as seed for whole brain correlation"
else:
print "Using %s as seed."%mask_name 
"""
"""
from run_brain_fit import find_confound_files
from run_brain_fit import find_runs
from run_brain_fit import load_runs
subject_dir='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100206'
runs=['REST1', 'REST2']
phases=['LR', 'RL']

from nilearn.input_data import NiftiMasker
import os
brain_masker=NiftiMasker(smoothing_fwhm=None,detrend=False,standardize=True,t_r=0.72,memory='nilearn_cache',memory_level=5,verbose=3)

f=find_confound_files(subject_dir, runs, phases)
img_fnames,imgs=find_runs(subject_dir, runs, phases)
img_fnames[0]='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100206/LR/REST1/rfMRI_REST1_LR_hp2000_clean_100.nii.gz'
import time
start = time.clock()
py_imgs = brain_masker.fit_transform(img_fnames[0], f[0])
elapsed = time.clock()
spent = elapsed - start
spent
rsn='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100206/LR/REST1/rfMRI_REST1_LR_hp2000_clean_100.nii.gz'
from nilearn import image
print(image.load_img(rsn).shape)

###############################33
from nilearn.input_data import NiftiMasker
import numpy as np
import nibabel as nb
import os

brainmask='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100307/LR/REST1/brainmask_fs.2.nii.gz'
brainmask='/work/04635/adutcher/lonestar/prestonlab/hcp/masks/mni_mtl/mtl_resample/mtl_4_2mm.nii.gz'

brain_masker = NiftiMasker(mask_img=brainmask,smoothing_fwhm=None,
    detrend=False, standardize=False,
    low_pass=None, high_pass=None, t_r=0.72,
    memory='nilearn_cache', memory_level=1, verbose=5)

rsn='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100307/LR/REST1/rfMRI_REST1_LR_hp2000_clean_10.nii.gz'
rsn='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100307/LR/REST1/func_REST1_LR.nii.gz'
imgs = brain_masker.fit_transform(rsn)
imgs1=nb.load(rsn)

import nilearn.masking as nlm
x=nlm.compute_background_mask(imgs1)
arr=img.get_data()

brainmask='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100307/LR/REST1/brainmask_fs.2.nii.gz'
mask=nb.load(brainmask)
marr=mask.get_data()

from mvpa2.tutorial_suite import *
rsn='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100307/LR/REST1/func_REST1_LR.nii.gz'
bold_fname = rsn
brainmask='/work/04635/adutcher/lonestar/test_hcp/hcp_behav_rest/subjects/100307/LR/REST1/brainmask_fs.2.nii.gz'
mask_fname = brainmask

import time
start=time.clock()
fds = fmri_dataset(samples=bold_fname,mask=mask_fname)
end=time.clock()
elapsed=end-start
elapsed

"""
