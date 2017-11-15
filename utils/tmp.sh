#!/bin/bash

cd subjects

subjects=`ls -d ??????`

for s in ${subjects[@]}; do

cd $s
cd RL
mkdir REST1
mv *.nii.gz *.txt REST1
cd ..

cd LR
mkdir REST1
mv *.nii.gz *.txt REST1
cd ..

mkdir RL/REST2
mkdir LR/REST2

cd ..

done
cd ..
