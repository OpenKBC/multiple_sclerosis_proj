__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: Mimic of notebook code for pipeline work, please see step2 in Jun notebook archive
Step4 is the same process with different input(activation socre -> gene expression)
"""

import pandas as pd
import argparse
import os

## call previous step for calling internal function
import step4_actscoreDiff
from libraries.statFunction import StatHandler


parser = argparse.ArgumentParser(prog='actscoreDiff.py')
# Input data
parser.add_argument('-r','--rthresh', dest='rankingthresh', required=True,\
     help='Threshold for RFECV" ')
parser.add_argument('-t','--type', dest='resultType', default='RR,CIS',\
     help='Result type, ex: long, healthy, "RR,CIS" ')
args = parser.parse_args()

# Simple control for snakemake(no argparse)
if __name__ == "__main__":

    SharedFilePath = os.environ['efspoint'] # Main data path here, goes to EFS volume
    metaName = os.environ['metafile'] # EPIC_HCvB_metadata_baseline_updated-share.csv
    msigFile = os.environ['msigDBPATH'] # msigdb.v7.4.entrez.gmt
    step1Input = os.environ['startFile'] # counts_vst_CD4.csv
    inputFile = SharedFilePath+os.path.basename(step1Input).replace('.csv', '.step6.csv') # replace to step4 input

    #Data loading
    df = pd.read_csv(inputFile, engine='c', index_col=0)
    meta_data = pd.read_csv(SharedFilePath+metaName)
    longDD_samples, shortDD_samples = step4_actscoreDiff._LoadDiseaseDuration(df, meta_data, args.resultType)
    df = df[longDD_samples+shortDD_samples].dropna() # reform df with intersected samples

    # Make training samples
    X = df.T.values # Training sample
    y = [0]*len(longDD_samples)+[1]*len(shortDD_samples) # Training y

    # features and ranking
    outputFile = SharedFilePath+os.path.basename(step1Input).replace('.csv', '.step7.csv') # replace to step5 output
    rankarr = StatHandler.calculate_RFECV(df, X, y, args.rankingthresh) # get ranksum result
    df.loc[df.index[rankarr]].to_csv(outputFile) # Writing