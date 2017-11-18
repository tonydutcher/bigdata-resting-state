#!/bin/bash

SUBJECT=$1
PHASE=$2
HOME=`pwd`

# make sure the file we want to copy things to exists
if ! [ -d subjects/${SUBJECT}/${PHASE} ]; then
	mkdir subjects/${SUBJECT}/${PHASE}
	echo "creating subjects/${SUBJECT}/${PHASE}, directory"
fi

# navigate to that folder
cd subjects/${SUBJECT}/${PHASE}

# pull from local directory to TACC
scp -vr prestonlab@apmac18.clm.utexas.edu:/Users/prestonlab18/Desktop/hcp_test/${SUBJECT}/${PHASE}/* .
echo "transfer of subject ${SUBJECT}, phase ${PHASE} complete"
 
cd ${HOME}
