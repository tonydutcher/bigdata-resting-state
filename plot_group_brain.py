#!/usr/bin/env python
import os
import sys
import numpy as np
import nibabel as nb
from nilearn import plotting
from nilearn.image import threshold_img

from rvm_hcp_rest_behav import get_hcp_maskrsfc
from mvpa2.datasets.mri import fmri_dataset

assert len(sys.argv)>1

# the mask list we want to make group plots with.
#masks=(BN_105_2mm_r_con-4mm_rsfc BN_106_2mm_r_con-4mm_rsfc BN_107_2mm_r_con-4mm_rsfc BN_108_2mm_r_con-4mm_rsfc BN_187_2mm_r_con-4mm_rsfc BN_188_2mm_r_con-4mm_rsfc l_hip_ant_2mm_r_con-4mm_rsfc r_hip_ant_2mm_r_con-4mm_rsfc l_hip_tail_2mm_r_con-4mm_rsfc r_hip_tail_2mm_r_con-4mm_rsfc)
# maskname  = 'BN_105_2mm_r_con-4mm_rsfc'
# pref_dir  = 'rsfc'
# imgsuf    = 'v2'

maskname  = sys.argv[1]
pref_dir  = sys.argv[2]
imgsuf    = sys.argv[3]

# the MNI space brain we are using as a common place to map participant responses to.
bg_brain  = '/work/IRC/ls5/opt/apps/fsl-5.0.9/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'
data_dir  = os.path.join('/work/04635/adutcher/lonestar/hcp_rest_behav/grouped_raw', pref_dir )
out_dir   = os.path.join('/work/04635/adutcher/lonestar/hcp_rest_behav/group_results')

# mask input to file
mask      = os.path.join( data_dir, "%s"%(maskname) )

# average a single mask and save as .nii
subs,m    = get_hcp_maskrsfc( maskname="%s.npy"%( mask ) )
N,P = m.shape
mz  = np.zeros([N,P])
for i in np.arange(0,N):
    mz[i,:] = np.arctanh(m[0,:])
mean_m     = np.zeros( [1, P] )
mean_mz    = np.zeros( [1, P] )
mean_m[:]  = m.mean( axis=0 )
mean_mz[:] = mz.mean( axis=0 )

# get a brain to map scores back into.
mnispace  = fmri_dataset( bg_brain, mask=bg_brain )

# pearson r image
rmap_file = os.path.join( out_dir,"%s_r_%s_group.nii.gz"%( mask, imgsuf ) )
mnirsfc   = mnispace.a.mapper.reverse( mean_m )
mnirsfc   = np.squeeze( mnirsfc )
nimg      = nb.Nifti1Image( mnirsfc, mnispace.a.imgaffine )
nimg.to_filename( rmap_file )
assert os.path.exists( rmap_file )

# fisher z image
zmap_file = os.path.join( out_dir,"%s_z_%s_group.nii.gz"%( mask, imgsuf ) )
zmnirsfc  = mnispace.a.mapper.reverse( mean_mz )
zmnirsfc  = np.squeeze( zmnirsfc )
znimg     = nb.Niftiq1Image( zmnirsfc, mnispace.a.imgaffine )
znimg.to_filename( zmap_file )
assert os.path.exists( zmap_file )

# # seed locations in MNI space.
# BN_105_2mm     = ([63, 34, 28])
# BN_106_2mm     = ([28, 34, 28])
# BN_107_2mm     = ([65, 28, 30])
# BN_108_2mm     = ([25, 28, 30])
# l_hip_ant_2mm  = ([58, 57, 28])
# l_hip_tail_2mm = ([28, 27, 28])
# r_hip_ant_2mm  = ([28, 57, 28])
# r_hip_tail_2mm = ([28, 27, 28])
# from nilearn import plotting
# # save output images
# # FIGURE TYPE 1
# display = plotting.plot_stat_map( zmap_file,
#                                 threshold=0.3, 
#                                 cut_coords=l_hip_ant_2mm)
# display.add_markers(marker_coords=l_hip_ant_2mm[0], 
#                     marker_color='g',
#                     marker_size=300)
# display.savefig('%s.pdf'%maskname)
# # FIGURE TYPE 1

# FIGURE TYPE 2
# Figure 1 type

# still needs title situation.
#fig, axes = plt.subplots(3, 1, figsize=(15,15))
#fig.set_facecolor('w')
#x=plotting.plot_stat_map( zmap_file, title='Left Anterior Cingulate Cortex', figure=fig, axes=axes[0], threshold=0.3, display_mode='x',cut_coords=5, colorbar=True )
#y=plotting.plot_stat_map( zmap_file, figure=fig, axes=axes[1], threshold=0.3, display_mode='z',cut_coords=5, colorbar=True )
#z=plotting.plot_stat_map( zmap_file, figure=fig, axes=axes[2], threshold=0.3, display_mode='y',cut_coords=5, colorbar=True )

# FIGURE TYPE 2
