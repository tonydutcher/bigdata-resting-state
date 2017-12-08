#!/bin/bash

cd $STUDYDIR/subjects

SUBJECTS=`ls -d ??????`

for SUBJECT in $SUBJECTS; do

${SRCDIR}/preprocess/move_subject.sh $SUBJECT

done
