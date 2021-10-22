__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: This is batch job for transforming data to DESeq input
"""

import pandas as pd
import numpy as np
import os
import glob
import argparse

from libraries.botoClass import botoHandler
from libraries.externalHandler import handlers as dataHandler

## argparse setting
parser = argparse.ArgumentParser(prog='step1_get_DESeq2_input.py')

parser.add_argument('-c','--ctype', type=str, dest='celltype', required=True,\
     choices=['CD4','CD8','CD14'],help='Cell type for extraction, default = CD8')

parser.add_argument('-v','--condcolumn', type=str, dest='condcolumn', required=True,\
     help='Column name which is using for condition value')

parser.add_argument('-x','--cond1', type=str, dest='cond1', required=True,\
     help='condition1 for metadata')

parser.add_argument('-y','--cond2', type=str, dest='cond2', required=True,\
     help='condition2 for metadata')

args = parser.parse_args()

# Main function
if __name__ == "__main__":

    ### Get ENV variables
    mainDataBucket = os.environ['mainbucket'] # openkbc-ms-maindata-bucket
    metaName = os.environ['metafile'] # EPIC_HCvB_metadata_baseline_updated-share.csv
    outputPath = os.environ['efspoint'] # /output/

    ### Error handling here

    ### Data prepration
    s3 = botoHandler(mainDataBucket) # Call boto3
    COUNT_PATH = "/data/" # Main data path

    META_PATH = s3.getFile([metaName]) ## This is FIXED parameter
    s3.getDirFiles('rsem_counts/', destpath=COUNT_PATH) # Download all count files
    
    filelist = glob.glob(COUNT_PATH+"*-"+args.celltype+".genes.results") # File path
    filelist = [os.path.basename(cursor) for cursor in filelist] # Extracting base file name
    sampleName = dataHandler.get_samplename(filelist)
    
    result_arr = [] # result array
    # sampleName and filelist have same order, and appending to result array
    for filename in filelist:
        sampleValues = dataHandler.get_column(COUNT_PATH+filename, 'expected_count')
        result_arr.append(sampleValues)
    result_df = pd.concat(result_arr, axis=1)
    result_df.columns = sampleName # Change column name by using sample names
    
    metadata = pd.read_csv(META_PATH) # read meta data

    # get meta result
    meta_result_df = dataHandler.get_condtionMatrix_by_category(metadata, 'HCVB_ID', args.condcolumn, [args.cond1, args.cond2])
    overlapped_samples = list(set(meta_result_df.index.tolist()).intersection(set(result_df.columns.tolist()))) # Overlapped samples
    
    # Extract overlapped samples
    meta_result_df = meta_result_df.loc[overlapped_samples]
    result_df = result_df[overlapped_samples]
    result_df.astype(int).to_csv(outputPath+args.celltype+"_output.csv") # Output
    meta_result_df.to_csv(outputPath+args.celltype+"_meta_output.csv")