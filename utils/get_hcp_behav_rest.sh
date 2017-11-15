#!/bin/bash

DBHOST=https://db.humanconnectome.org
db_user=amdutcher
db_password=pE34imA!
PHASE=RL

# https://db.humanconnectome.org/data/archive/projects/HCP_1200/subjects/100307/experiments/100307_CREST/resources/100307_CREST/files/MNINonLinear/Results/rfMRI_REST1_LR/rfMRI_REST1_LR_Atlas.dtseries.nii

# get subject list for all subjects that have resting state data
if ! [ -f "out.txt" ]; then
	python select_hcp_behav_rest.py "out.txt"
fi

count=1
while IFS=, read -r col1 col2 col3; do
	#echo "$col1|$col2|$col3"
	#RELNUM=`echo "$col1" | grep -o -E '[0-9]+'`
	#PROJECT=`echo HCP_$RELNUM`
	SUBJECT=$col2
	#ACQUIRE=$col3
	PROJECT=HCP_1200
	
	# rest prefix
	REST_URL_PREFIX=$DBHOST/data/archive/projects/$PROJECT/subjects
	
	# subject prefix
	subject_url_prefix=$REST_URL_PREFIX/${SUBJECT}/experiments/${SUBJECT}_CREST/resources/${SUBJECT}_CREST/files
	
	# make a directory
	if ! [ -d $SUBJECT ]; then
		mkdir $SUBJECT
	fi
	
	# navigate to the directory
	cd $SUBJECT
	
	if ! [ -d $PHASE ]; then
		mkdir $PHASE
	fi
	
	# navigate to RL directory
	cd RL

	# cycle through files
	while read line
	do
		if [ -z $line ]; then 
			exit 0
		fi
		file_relative_path=MNINonLinear/Results/rfMRI_REST1_${PHASE}/${line}
		full_path=${subject_url_prefix}/${file_relative_path}
		echo "Downloading ${line} for subject $SUBJECT"
	
		# does the work
		#curl
		#wget --user=$db_user --password=$db_password --no-check-certificate -O $line ${full_path}
	
	done < ../../files_to_get_${PHASE}
	
	# navigate back up
	cd ../..
	
	# counter
	count=`echo "${count}+1" | bc -l`
	echo $count
	
	# early exit for checking purposes
	if [ $count -eq 200 ]; then
		exit 1
	fi

done < "out.txt"
