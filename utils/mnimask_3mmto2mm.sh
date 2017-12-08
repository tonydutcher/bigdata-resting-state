#!/bin/bash

if [ $# -lt 1 ]; then
echo "usage: $0 <input 1mm mask> <out>"
exit
fi

in=$1
out=$2

echo "resample 3mm mask to a 2mm mask"

flirt -in ${in} -ref $FSLDIR/data/standard/MNI152_T1_2mm -applyxfm -usesqform -out temp_01
fslmaths temp_01.nii.gz -bin ${out}

rm temp_01.nii.gz
