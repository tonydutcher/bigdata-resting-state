#!/bin/bash

SUBJECT=$1
HOME=`pwd`

# make sure the file we want to copy things to exists
if ! [ -d subjects/${SUBJECT}/masks ]; then
	mkdir subjects/${SUBJECT}/masks
	echo "creating subjects/${SUBJECT}/masks, directory"
fi

# navigate to that folder
cd subjects/${SUBJECT}/masks

# pull from local directory to TACC
scp -vr prestonlab@apmac18.clm.utexas.edu:/Users/prestonlab18/Desktop/hcp_test/${SUBJECT}/masks/* .
echo "transfer of subject ${SUBJECT}, masks file complete"
 
cd ${HOME}
