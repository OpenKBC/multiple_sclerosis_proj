__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: Copy from utils directory
Example: python get_DESeq2_input_from_files.py -p inputpath/ -m meta.csv -s HCVB_ID -v DiseaseCourse -x RR -y CIS -c CD4 -o outputpath/outputfile
It needs some changes because of docker memory issue
"""

import glob
import os
import argparse
import pandas as pd
from lib.externalHandler import handlers as dataHandler

parser = argparse.ArgumentParser(prog='get_matrix_from_files.py')
# Mode selection
parser.add_argument('-t','--ftype', type=str, dest='filetype', default='genes',\
     choices=['genes','isoforms'],help='Mode for getting matrix (isoforms or genes), default = genes')
# Input data path
parser.add_argument('-p','--path', type=str, dest='filepath', required=True,\
     help='Directory path for input files')
# Input data path
parser.add_argument('-m','--meta', type=str, dest='metafile', required=True,\
     help='Meta data file')

## Probably these could be unified if it is using dictionary type as argparse input
parser.add_argument('-s','--sampcolumn', type=str, dest='sampcolumn', required=True,\
     help='Column name which is using for Sample ID')
parser.add_argument('-v','--condcolumn', type=str, dest='condcolumn', required=True,\
     help='Column name which is using for condition value')
parser.add_argument('-x','--cond1', type=str, dest='cond1', required=True,\
     help='condition1 for metadata')
parser.add_argument('-y','--cond2', type=str, dest='cond2', required=True,\
     help='condition2 for metadata')
## Probably these could be unified if it is using dictionary type as argparse input

# Immune cell type
parser.add_argument('-c','--ctype', type=str, dest='celltype', required=True,\
     choices=['CD4','CD8','CD14'],help='Cell type for extraction, default = CD8')
# Output file name (Modified for snakemake)
parser.add_argument('-o','--outputExpr', type=str, dest='outputExpr', required=True, \
     help='Output file path and name')
parser.add_argument('-r','--outputMeta', type=str, dest='outputMeta', required=True, \
     help='Output file path and name')
args = parser.parse_args()

if __name__ == "__main__":
    COUNT_PATH = args.filepath+"/" # DIR path
    filelist = glob.glob(COUNT_PATH+"*-"+args.celltype+"."+args.filetype+".results") # File path
    filelist = [os.path.basename(cursor) for cursor in filelist] # Extracting base file name
    sampleName = dataHandler.get_samplename(filelist)
    
    result_arr = [] # result array
    # sampleName and filelist have same order, and appending to result array
    for filename in filelist:
        sampleValues = dataHandler.get_column(COUNT_PATH+filename, 'expected_count')
        result_arr.append(sampleValues)
    result_df = pd.concat(result_arr, axis=1)
    result_df.columns = sampleName # Change column name by using sample names
    
    metadata = pd.read_csv(args.metafile) # read meta data
    assert args.sampcolumn in metadata.columns.tolist(), "Cannot find column name in meta" # Check
    assert args.condcolumn in metadata.columns.tolist(), "Cannot find column name in meta"

    # get meta result
    meta_result_df = dataHandler.get_condtionMatrix_by_category(metadata, args.sampcolumn, args.condcolumn, [args.cond1, args.cond2])
    overlapped_samples = list(set(meta_result_df.index.tolist()).intersection(set(result_df.columns.tolist()))) # Overlapped samples
    
    # Extract overlapped samples
    meta_result_df = meta_result_df.loc[overlapped_samples]
    result_df = result_df[overlapped_samples]

    result_df.astype(int).to_csv(args.outputExpr) # Output
    meta_result_df.to_csv(args.outputMeta)