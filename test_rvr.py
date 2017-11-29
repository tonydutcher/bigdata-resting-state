#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import argparse

from sklearn.preprocessing import scale
from rvm_hcp_rest_behav import get_hcp_behav, get_hcp_maskrsfc, rvr_mask

description="This script runs RVR using a python package that interfaces with sklearn\
    - see https://github.com/AmazaspShumik/sklearn-bayes for details on the method and implementation"

parser = argparse.ArgumentParser(description=description)
parser.add_argument("-m,", metavar="mask name", action="store", dest="MASKNAME", type=str, required=True, help=("The mask to use as the seed.") )
args = parser.parse_args()

####################################################################
###### Getting neural and behavioral data into format.
####################################################################

datadir='/work/04635/adutcher/lonestar/hcp_rest_behav/grouped_raw/non_rsfc'

# This needs to be made into a separate function with mask and 
# behavior columns of interest as input.
print "Working on mask %s"%args.MASKNAME
maskfile='%s.npy'%args.MASKNAME
interestfile=os.path.join(datadir, 'columns.txt')
fullfile=os.path.join(datadir, 'unrestricted_amdutcher_10_25_2017_14_22_5.csv')

# This function will pull in mask data, sort subjects in ascending order
#   and separate the subject ids from the mask data - nans still exist in here :(.
subs, mask = get_hcp_maskrsfc(maskname=maskfile)

# This function will pull in the behavior data from a master file and grab only the variable
#   names of interest 'column headers from the csv file' from the interesfile specified. The
#   names in the interestfile should match exactly the names in the master file to exact.
#   ALSO, the subject array argument assums get_hcp_maskrsfc has been run because mask data
#   is not necessarily in acsending order, but this function assume all data, including mask
#   patterns is in order at this point.
behav = get_hcp_behav(full_file=fullfile, interest_file=interestfile, subject_array=subs)

# This gets specific variables we are interested in and puts them into a numpy array
cs=behav.loc[:,'CardSort_Unadj'].values
fl=behav.loc[:,'Flanker_Unadj'].values

####################################################################
###### Use rvm with resting-state and behavior.
####################################################################

# This takes out the single nan subject in the behavioral score.
ind = np.invert( np.isnan(cs) )

#### We need to do either Fisher r-to-z-transformation or scale
# Fisher r-to-z-transformation
print "Runnning fisher-z transform"
Xx  = mask[ ind ]
Xxz = np.zeros([Xx.shape[0], Xx.shape[1]])
for i in np.arange(Xx.shape[0]):
    for j in np.arange(Xx.shape[1]):
        Xxz[i,j] = np.arctanh(Xx[i,j])

print "Finished fisher-z transform, saving mean image for plotting"
mean_zimg=Xxz.mean(axis=0)
np.save(('%s_mean_zimg.npy'%args.MASKNAME),mean_zimg)

# This scales the data.
#Xx  = scale( mask[ ind ] )
Yy1 = scale( fl[ ind ] )
Yy2 = scale( cs[ ind ] )

####################################################################
###### Cross-validation across the training set and test sets
####################################################################

# Cycle through the masks, start with the 4 hippocampal regions.
#   The 4 hippocampal regions will predict the flanker task and 
#   dimensional card sort task.

###########################################################x#########
###### Revelance Vector Regression.
####################################################################
#The relationship between predicted performance (predicted performance) 
#obtained from the relevance vector regression models and actual location 
#memory performance (actual performance), measured as proportion correct 
#responses, in the object-location task, for each of the four seed regions, 
#left and right, anterior and posterior hippocampus

print "Running abbreviated RVR with fl behavior."
active_vectors, error, prediction = rvr_mask(Xx=Xxz, Yy=Yy1, plot=True, behaviorname='fl', maskname=args.MASKNAME)

print "Running abbreviated RVR with cs behavior."
active_vectors, error, prediction = rvr_mask(Xx=Xxz, Yy=Yy2, plot=True, behaviorname='cs', maskname=args.MASKNAME)

####################################################################
###### Get Resting state netorks.
####################################################################
#
# Get the 264 mask from Powers et al. 2011.
#
# Try to apply the 264 mask to the brain data within each subject
#   and plot the connections above a certain threshold.
#
