import glob
import os
import argparse
import pandas as pd

# Naming rule
# SampleName-CD-genes(isoforms).results

parser = argparse.ArgumentParser(prog='get_matrix_from_files.py')
# Mode selection
parser.add_argument('-t','--ftype', type=str, dest='filetype', required=True, default='genes',\
     choices=['genes','isoforms'],help='Mode for getting matrix (isoforms or genes), default = genes')
# Input data path
parser.add_argument('-p','--path', type=str, dest='filepath', required=True, default='./',\
     help='Directory path for input files, default = ./')
# Data value for extraction
parser.add_argument('-v','--value', type=str, dest='valuetype', required=True, default='TPM',\
     choices=['FPKM','TPM','expected_count'],help='Value type for extraction, default = TPM')
# Immune cell type
parser.add_argument('-c','--ctype', type=str, dest='celltype', required=True, default='CD8',\
     choices=['CD4','CD8','CD14'],help='Cell type for extraction, default = CD8')
# Output file name
parser.add_argument('-o','--output', type=str, dest='output', required=True, default='./output',\
     help='Output file path and name')
args = parser.parse_args()

def _get_column(filename_with_path,  ext_value, annot='gene_id', sep="\t"):
    """
    filename_with_path = filepath + basename
    ext_value = column name of file
    sep = separator
    """
    temp = pd.read_csv(filename_with_path, sep=sep).set_index(annot) # temp loading
    return temp[[ext_value]]

def _get_samplename(filelist):
    """
    filelist = list of basename
    Lambda function could be--
    _get_samplename = lambda filelist : [x.split("-")[0] for x in filelist]
    """
    sampleName = [x.split("-")[0] for x in filelist]
    return sampleName

if __name__ == "__main__":
    COUNT_PATH = args.filepath # DIR path
    filelist = glob.glob(COUNT_PATH+"*-"+args.celltype+"."+args.filetype+".results") # File path
    filelist = [os.path.basename(cursor) for cursor in filelist] # Extracting base file name
    sampleName = _get_samplename(filelist)
    
    result_arr = [] # result array
    # sampleName and filelist have same order, and appending to result array
    for filename in filelist:
        sampleValues = _get_column(COUNT_PATH+filename, args.valuetype)
        result_arr.append(sampleValues)
    result_df = pd.concat(result_arr, axis=1)
    result_df.columns = sampleName # Change column name by using sample names
    
    result_df = result_df.reset_index() # reset index for feather format
    result_df.to_feather(args.output+".feather") # Feather output