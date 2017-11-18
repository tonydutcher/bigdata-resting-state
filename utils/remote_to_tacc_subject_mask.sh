#!/bin/bash

SUBJECT=$1
HOME2=$WORK/hcp_rest_behav
cd $HOME2

if [ $# -lt 1 ]; then
echo "Takes subject id as input and pulls from local directory APMac18
that has participant files"
exit 1
fi

# make sure the file we want to copy things to exists
if ![ -d subjects/${SUBJECT}/masks ]; then
mkdir -p subjects/${SUBJECT}/masks
echo "creating subjects/${SUBJECT}/masks, directory"
fi

# navigate to that folder
cd subjects/${SUBJECT}/masks

# pull from local directory to TACC
scp -vr prestonlab@apmac18.clm.utexas.edu:/Users/prestonlab18/Desktop/hcp/${SUBJECT}/masks/* subjects/${SUBJECT}/masks
echo "transfer of subject ${SUBJECT}, masks file complete"

cd ${HOME2}
