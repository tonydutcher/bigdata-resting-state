#!/usr/bin/env python
import os
import sys
import subprocess as sub
from glob import glob

# subject directory - full path
subdir = str(sys.argv[1])

# feat directory
featdir=os.path.join( subdir, 'processed', 'all.feat')

# identity files
identitydir = '/home1/04635/adutcher/analysis/fat/resources'
identity = os.path.join( identitydir, 'identity.mat' )

# fake highres
highres = os.path.join( subdir, 'LR', 'REST1', 'PhaseOne_gdc_dc.nii.gz')
reg_dir = os.path.join( featdir, 'reg')

/work/04635/adutcher/lonestar/hcp_rest_behav/subjects/205725/processed/BN_105_2mm_array_con-4mm_rsfc.nii.gz

p=sub.Popen('mkdir -p %s' % reg_dir, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
stdout,stderr=p.communicate()
p=sub.Popen('ln -sf %s %s' % (highres, os.path.join(reg_dir, 'highres.nii.gz')), stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
stdout,stderr=p.communicate()
p=sub.Popen('ln -sf %s %s' % (highres, os.path.join(reg_dir, 'standard.nii.gz')), stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
stdout,stderr=p.communicate()
p=sub.Popen('cp %s %s' % (identity, os.path.join(reg_dir, 'standard2example_func.mat')), stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
stdout,stderr=p.communicate()
p=sub.Popen('cp %s %s' % (identity, os.path.join(reg_dir, 'example_func2standard.mat')), stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
stdout,stderr=p.communicate()
p=sub.Popen('updatefeatreg %s -pngs' % featdir, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
stdout,stderr=p.communicate()
