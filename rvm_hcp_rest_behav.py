#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

from sklearn.preprocessing import scale
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.utils.estimator_checks import check_estimator
from fast_rvr import RegressionARD,ClassificationARD,RVR,RVC

datadir='/work/04635/adutcher/lonestar/hcp_rest_behav/grouped_raw/non_rsfc'
outdir=os.path.join(datadir,'results')

def test_behav_mask_alignment():
    pass
    # return test_results

def get_hcp_maskrsfc(maskname=None):
    """
    Takes a .npy mask filename as input
        - The mask file name should be in the current directory if the full path isn't specified.
        - The subject name and rsfc brain connectivity with this mask region are in the file. 
    """
    # Asserts the mask file exists and that it is the current directory. 
    assert os.path.exists(maskname)
    
    # The file should be a .npy file, it will give an error if not.
    x=np.load(maskname)

    # Apparently there are zeros in the subject list
    # This kind of malicious activity SHOULD NOT be tolerated - except for a little bit.
    x=x[x[:,0]!=0,:]

    # Sort the array in ascending order
    x=x[x[:,0].argsort()]

    # This grabs the subjects only.
    subs=x[:,0]

    # This grabs the data in the rest of the array.
    mask=x[:,1:]

    # This gets rid of NaNs and sets them to zero.
    mask[np.isnan(mask)]=0
    
    # This returns both as separate variables. Note that these rows should be shuffled in unison. 
    return subs, mask


def get_hcp_behav(full_file=None, interest_file=None, subject_array=None):
    """
    This gets the behavior we are interested in comparing with rsfc masks.

    **IMPORTANT**
     The function 'get_hcp_maskrsfc' should already have been run to produce a subject array
     and corresponding rsfc patterns that are in ascending subject order. This is key for matching
     the behavior with the resting-state connectivity patterns in the mask file.

    """
    #datadir='/work/04635/adutcher/lonestar/hcp_rest_behav/grouped_raw/non_rsfc'

    # Asserts the existence of the file with the column names for the columns of interest.
    # The full path is not specified therefore it needs to be in the current directory.
    assert os.path.exists(interest_file)
    assert os.path.exists(full_file)

    # This grabs the behavior data.
    headers = tuple( pd.read_csv(full_file, nrows=1).columns )
    
    # This gets the columns in the behavir data we are interested in.
    with open(interest_file) as f:
        interest = f.read().splitlines()

    # This is because I don't know how to read in pandas by column strings. 
    index = [ i for i,h in enumerate(headers) if (h in interest) ]

    # This finally reads in the behavior data for only the columns we are interested in (indexed numerically).
    behav = pd.read_csv(full_file, usecols=index)

    # Now we restrict the behavioral responses to subjects in the subject list.
    # behav.query('Subject in subjects') -- I wish this worked...
    behav = behav[behav.Subject.isin(subject_array)]

    return behav

def rvr_mask(Xx=None, Yy=None, plot=True, behaviorname=None, maskname=None):
    
    # Set some parameters.
    cv  = KFold(n_splits=10, shuffle=True, random_state=None)
    #rvr = RVR(kernel='linear')
    rvr = RegressionARD(n_iter=320, verbose=True)

    # Cycle through the training and testing sets. 
    active_vectors = []
    error          = []
    prediction     = np.zeros([len(Xx), 2])
    for k, (train, test) in enumerate(cv.split(Xx, Yy)):
        print "CV fold = %d"%k

        # This fits the training data.
        rvr.fit(Xx[train,:40000], Yy[train])
    
        # This fits the held-out test data.
        y_hat, var = rvr.predict_dist(Xx[test,:40000])
    
        # This measures the error in the model.
        error.append( mean_squared_error(y_hat,Yy[test]))
    
        # Save predicted score.
        prediction[test,0]=test
        prediction[test,1]=y_hat
    
        # Saves the active vectors.
        active_vectors.append( rvr.active_ )
    
    if plot:
        plt.scatter( prediction[:,1], Yy )
        plt.title( "%s_%s_predict-vs-actual"%(behaviorname, maskname) )
        plt.savefig( os.path.join( outdir, "%s_%s_predict-vs-actual.png"%(behaviorname, maskname) ) )

    # save output
    np.save(os.path.join( outdir, "%s_%s_cv_error"%(behaviorname, maskname)), np.array(error) )
    np.save(os.path.join( outdir, "%s_%s_preds"%(behaviorname, maskname)), prediction )

    return active_vectors, error, prediction 
