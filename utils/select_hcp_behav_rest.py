#!/Users/anthonydutcher/anaconda/bin/python

import sys
import numpy as np
import pandas as pd

if len(sys.argv) < 2:
	sys.exit("must specify an output file name for correct subjects")

# read in the behavior
file='unrestricted_amdutcher_10_25_2017_14_22_5.csv'
data=pd.DataFrame( pd.read_csv(file) )

# this is the column we are interested in
interest_col='3T_RS-fMRI_Count'
outfile='out.txt'
outfile=sys.argv[1]

# cycle through subjects and put the ones that have 
subjects = np.unique( data.loc[:,'Subject'] )
include  = []
f=open( outfile, "w")
for sub in subjects:
	if int( data.loc[ data['Subject']==sub, interest_col].values ) > 1:
		release = data.loc[data.loc[:,'Subject']==sub, 'Release'].values[0]
		acquire = data.loc[data.loc[:,'Subject']==sub, 'Acquisition'].values[0]
		f.write("%s,%s,%s\n"%( release, sub, acquire ))
		include.append( sub )

f.close()