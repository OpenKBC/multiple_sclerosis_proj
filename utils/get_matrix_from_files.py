__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: This code generates expression matrix by using raw data files from GEO.
We have normalized data and we don't need to use this usually, but to get original read_count, this would be helpful.s
"""

import glob
import os
import argparse
import pandas as pd
from .lib.externalHandler import handlers

parser = argparse.ArgumentParser(prog='get_matrix_from_files.py')
# Mode selection
parser.add_argument('-t','--ftype', type=str, dest='filetype', default='genes',\
     choices=['genes','isoforms'],help='Mode for getting matrix (isoforms or genes), default = genes')
# Input data path
parser.add_argument('-p','--path', type=str, dest='filepath', required=True,\
     help='Directory path for input files')
# Data value for extraction
parser.add_argument('-v','--value', type=str, dest='valuetype', required=True,\
     choices=['FPKM','TPM','expected_count'],help='Value type for extraction, default = TPM')
# Immune cell type
parser.add_argument('-c','--ctype', type=str, dest='celltype', required=True,\
     choices=['CD4','CD8','CD14'],help='Cell type for extraction, default = CD8')
# Output file name
parser.add_argument('-o','--output', type=str, dest='output', required=True, \
     help='Output file path and name')
# Output type     
parser.add_argument('-u','--outtype', type=str, dest='outtype', default='csv',\
     choices=['csv', 'feather'], help='Output type, csv or feather, default=csv')
args = parser.parse_args()

if __name__ == "__main__":
     COUNT_PATH = args.filepath # DIR path
     filelist = glob.glob(COUNT_PATH+"*-"+args.celltype+"."+args.filetype+".results") # File path
     filelist = [os.path.basename(cursor) for cursor in filelist] # Extracting base file name
     sampleName = handlers.get_samplename(filelist)
    
     result_arr = [] # result array
     # sampleName and filelist have same order, and appending to result array
     for filename in filelist:
         sampleValues = handlers.get_column(COUNT_PATH+filename, args.valuetype)
         result_arr.append(sampleValues)
     result_df = pd.concat(result_arr, axis=1)
     result_df.columns = sampleName # Change column name by using sample names
    
     if args.outtype=='csv':
          result_df.to_csv(args.output+".csv") # Feather output
     elif args.outtype=='feather':
          result_df = result_df.reset_index() # reset index for feather format
          result_df.to_feather(args.output+".feather") # Feather output