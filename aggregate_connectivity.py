#!/usr/bin/env python

import os
import glob
import numpy as np
import argparse

description="This script aggregates rsfc patterns across subjects for a specific mask"

parser = argparse.ArgumentParser(description=description)
parser.add_argument("-m,", metavar="mask", action="store", dest="mask", type=str, required=True, help=("The name of the mask to be used.") )
parser.add_argument("-d,",  action="store_true", dest="dryrun", default=False, required=False, help=("Run a dry run of the options.") )
args = parser.parse_args()

# necesary paths
studydir="/work/04635/adutcher/lonestar/hcp_rest_behav"
subdir=os.path.join(studydir,"subjects")
outdir=os.path.join(studydir,"grouped_raw/non_rsfc")
outfile=os.path.join(outdir,"%s_group_rsfc"%args.mask)

# print argument if you desire
if args.dryrun:
    print "INPUT ARGUMENTS"
    print "Subject directory: %s"%args.subject
    print "Mask being used: %s"%args.mask

# get all the files, these will not have any order
foundfiles=glob.glob(os.path.join(subdir,"??????/processed/%s_non_rsfc.npy"%args.mask))
nfiles=len(foundfiles)
print "Found %04d files pertaining to the %s mask"%(nfiles, args.mask)

# cycle through the files
count=0
while count <= (nfiles-1):
    s   = int(foundfiles[count].split('/')[7])
    arr = np.load(foundfiles[count])
    print "Loading in rsfc data for subject %s"%(s)
    if count == 0:
        data=np.zeros([nfiles,arr.shape[1]+1])

    if (data.shape[1]-1) == (arr.shape[1]):
	print "Adding subject %s to group"%(s)
        data[count,:]=np.concatenate( ( np.array([s]).ravel(), arr.ravel() ) )
    else:
        print "Not adding subject %s to group, dimension mismatch"%(s)
    count+=1

# saving outfile
print "Saving text file, %s"%outfile
np.savetxt(outfile, data, delimiter=" ")
np.save(outfile, data) 
