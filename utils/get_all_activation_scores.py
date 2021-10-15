__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: This code generates activation scores by using MsigDB. This code needs expression matrix by EntrezID index
"""

## Move to setting.env in the future
MSIGDB_PATH = "/Users/junheeyun/OpenKBC/multiple_sclerosis_proj/data/MsigDB_list/msigdb.v7.4.entrez.gmt"

import argparse
import pandas as pd
from lib.standard_gzscore import calculator

parser = argparse.ArgumentParser(prog='get_all_activattion_scores.py')
# Input data
parser.add_argument('-i','--input', type=str, dest='input_df', required=True,\
     help='Input data matrix')
# Output path
parser.add_argument('-o','--output', type=str, dest='output', required=True, default='./',\
     help='Output file')
args = parser.parse_args()

if __name__ == "__main__":
     # .gmt parsing
     count = 0
     gmt_arr = [] # gmt parsing array
     with open(MSIGDB_PATH, 'r') as infile:
        for line in infile:
             gmt_value = line.strip().split("\t") # splitting line
             sig_names = gmt_value[0] # signature name
             gene_list = gmt_value[2:] # gene list
             gmt_arr.append([sig_names]+gene_list)

     # Sample loading, and some entrezIDs are duplicated in the matrix
     gexpr = pd.read_csv(args.input_df, index_col=0)
     gexpr.index = [x.split(".")[0] for x in gexpr.index.tolist()] # remove effect from R make.names
     gexpr = gexpr.groupby(gexpr.index).max() # keeping max for duplicated index
     
     zscore_arr = [] # result array
     zscore_calculator = calculator(gexpr) # Set activation calculator
     for sig in gmt_arr:
          zscore_value = zscore_calculator.gs_zscore(names=sig[0], gene_set=sig[1:]) # using standard, threaded version has an error
          zscore_arr.append(zscore_value)
     zscore_df = pd.concat(zscore_arr, axis=1) # make dataframe
     zscore_df.to_csv(args.output)