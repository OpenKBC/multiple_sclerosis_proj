__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: This code generates activation scores by using MsigDB. This code needs expression matrix by EntrezID index
"""

## Move to setting.env in the future
MSIGDB_PATH = "/Users/junheeyun/OpenKBC/multiple_sclerosis_proj/data/MsigDB_list/msigdb.v7.4.entrez.gmt"

import os
import pandas as pd
from libraries.standard_gzscore import calculator

if __name__ == "__main__":

     SharedFilePath = os.environ['efspoint'] # Main data path here, goes to EFS volume
     metaName = os.environ['metafile'] # EPIC_HCvB_metadata_baseline_updated-share.csv
     msigFile = os.environ['msigDBPATH'] # msigdb.v7.4.entrez.gmt
     step1Input = os.environ['startFile'] # counts_vst_CD4.csv
     inputFile = SharedFilePath+os.path.basename(step1Input).replace('.csv', '.step2.csv') # replace to step3 input

     # .gmt parsing
     count = 0
     gmt_arr = [] # gmt parsing array
     MSIGDB_PATH = SharedFilePath+msigFile
     with open(MSIGDB_PATH, 'r') as infile:
        for line in infile:
             gmt_value = line.strip().split("\t") # splitting line
             sig_names = gmt_value[0] # signature name
             gene_list = gmt_value[2:] # gene list
             gmt_arr.append([sig_names]+gene_list)

     # Sample loading, and some entrezIDs are duplicated in the matrix
     gexpr = pd.read_csv(inputFile, index_col=0)
     gexpr.index = [x.split(".")[0] for x in gexpr.index.tolist()] # remove effect from R make.names
     gexpr = gexpr.groupby(gexpr.index).max() # keeping max for duplicated index
     
     zscore_arr = [] # result array
     zscore_calculator = calculator(gexpr) # Set activation calculator
     for sig in gmt_arr:
          zscore_value = zscore_calculator.gs_zscore(names=sig[0], gene_set=sig[1:]) # using standard, threaded version has an error
          zscore_arr.append(zscore_value)
     zscore_df = pd.concat(zscore_arr, axis=1) # make dataframe

     outputFile = SharedFilePath+os.path.basename(step1Input).replace('.csv', '.step3.csv') # replace to step3 output
     zscore_df.to_csv(outputFile)