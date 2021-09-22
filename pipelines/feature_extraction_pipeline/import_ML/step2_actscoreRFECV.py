__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: Mimic of notebook code for pipeline work, please see step2 in Jun notebook archive
Step4 is the same process with different input(activation socre -> gene expression)
"""

import pandas as pd
from sys import argv

## call previous step for calling internal function
import step1_actscoreDiff
from lib.statFunction import StatHandler


# Simple control for snakemake(no argparse)
actScoreInput=argv[1]
metaData=argv[2]
rankingthresh=int(argv[3])
outputFile=argv[4]

if __name__ == "__main__":
    #Data loading
    df = pd.read_csv(actScoreInput, engine='c', index_col=0)
    meta_data = pd.read_csv(metaData)
    longDD_samples, shortDD_samples = step1_actscoreDiff._LoadDiseaseDuration(df, meta_data)
    df = df[longDD_samples+shortDD_samples].dropna() # reform df with intersected samples

    # Make training samples
    X = df.T.values # Training sample
    y = [0]*len(longDD_samples)+[1]*len(shortDD_samples) # Training y

    # features and ranking
    rankarr = StatHandler.calculate_RFECV(df, X, y, rankingthresh) # get ranksum result
    df.loc[df.index[rankarr]].to_csv(outputFile) # Writing