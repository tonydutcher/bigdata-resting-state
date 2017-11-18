#!/bin/bash

flirt -in brainmask_fs.nii.gz -ref /work/IRC/ls5/opt/apps/fsl-5.0.9/data/standard/MNI152_T1_2mm_brain.nii.gz -out brain_2mm.nii.gz -applyisoxfm 2
