#!/usr/bin/env python

import os
from glob import glob
import numpy as np
import argparse

description="This script aggregates rsfc patterns across subjects for a specific mask"

parser = argparse.ArgumentParser(description=description)
parser.add_argument("-m,", metavar="mask", action="store", dest="mask", type=str, required=False, help=("The name of the mask to be used. - no full path") )
parser.add_argument("-d,", action="store_true", dest="dryrun", default=False, required=False, help=("Run a dry run of the options.") )
args = parser.parse_args()

if args.mask is None:
    print "Must specify a mask (not the full path)."
    exit()

# necesary paths
studydir="/work/04635/adutcher/lonestar/hcp_rest_behav"
subdir=os.path.join(studydir,"subjects")
outdir=os.path.join(studydir,"grouped_raw/rsfc")
imgsuf='r_con-4mm_rsfc'
if not os.path.exists( outdir ):
    os.mkdir( outdir )

outfile=os.path.join( outdir,"%s_%s"%(args.mask, imgsuf) )

# print argument if you desire
if args.dryrun:
    print "INPUT ARGUMENTS"
    print "Subject directory: %s"%args.subject
    print "Mask being used: %s"%args.mask
    exit()

# get all the files, these will not have any order
foundfiles=glob(os.path.join(subdir,"??????/processed/%s_%s.npy"%(args.mask, imgsuf) ) )
nfiles=len(foundfiles)
print "Found %04d files pertaining to the %s mask"%(nfiles, args.mask)

# cycle through the files
count=0
while count <= (nfiles-1):
    # get sid for file
    s   = int(foundfiles[count].split('/')[7])
    arr = np.load(foundfiles[count])

    #print "Loading in rsfc data for subject %s"%(s)
    if count == 0:
        data=np.zeros([nfiles,arr.shape[1]+1])

    if (data.shape[1]-1) == (arr.shape[1]):
	#print "Adding subject %s to group"%(s)
        data[count,:]=np.concatenate( ( np.array([s]).ravel(), arr.ravel() ) )
        
    else:
        pass
        #print "Not adding subject %s to group, dimension mismatch"%(s)
    
    count+=1

# saving outfile
print "Saving text file, %s"%outfile
np.savetxt(("%s.txt"%outfile), data, delimiter=" ")
np.save(outfile, data) 
