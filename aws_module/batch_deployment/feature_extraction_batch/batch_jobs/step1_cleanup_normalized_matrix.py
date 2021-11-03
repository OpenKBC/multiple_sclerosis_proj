__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: This code cleans normalized matrix which contains informal Ensembl ID as index and columns with informal string, 
and it takes care of duplications of Ensembl IDs. After doing this code, R/IDconverter.R is highly recommended to convert ID(CSV only).
"""

import os
import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(prog='cleanup_normalized_matrix.py')
# Input data
parser.add_argument('-v','--vst', dest='vst', action='store_true',default=False,\
     help='Input data is vst normalized or not, default = False')
args = parser.parse_args()

if __name__ == "__main__":
    # Input Name: step0_name.csv

    SharedFilePath = os.environ['efspoint'] # Main data path here, goes to EFS volume
    inputFile = os.environ['startFile'] # counts_normalized/rawFiles/counts_vst_CD4.csv

    # Load data
    if '.csv' in inputFile:
        df = pd.read_csv(SharedFilePath+inputFile, index_col=0)
    elif '.feather' in inputFile:
        df = pd.read_feather(SharedFilePath+inputFile, index_col=0)
    
    df.index = [x.split(".")[0] for x in df.index.tolist()] # New index names
    df.columns = [x.split(".")[0] for x in df.columns.tolist()] # New column names
    df = df[~df.index.duplicated(keep='first')] # Taking first values in duplicated index

    if args.vst==False:
        df=df.applymap(lambda x: np.log2(x+1)) # Apply log2 for non-vst normalized data

    ## Need to add file name handler
    df.to_csv(SharedFilePath+os.path.basename(inputFile).replace('.csv', '.step1.csv'))
    # Output Name: step0_name.step1.csv