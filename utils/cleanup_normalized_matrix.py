__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: This code cleans normalized matrix which contains informal Ensembl ID as index and columns with informal string, 
and it takes care of duplications of Ensembl IDs. After doing this code, R/IDconverter.R is highly recommended to convert ID(CSV only).
"""

import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(prog='cleanup_normalized_matrix.py')
# Input data
parser.add_argument('-i','--input', type=str, dest='input_df', required=True,\
     help='Input data matrix')
# Output path
parser.add_argument('-o','--output', type=str, dest='output', required=True,\
     help='Output file name including path')

parser.add_argument('-v','--vst', dest='vst', action='store_true',default=False,\
     help='Input data is vst normalized or not, default = False')
args = parser.parse_args()

if __name__ == "__main__":
    # Load data
    if '.csv' in args.input_df:
        df = pd.read_csv(args.input_df, index_col=0)
    elif '.feather' in args.input_df:
        df = pd.read_feather(args.input_df, index_col=0)
    
    if '.csv' not in args.output and '.feather' not in args.output:
        raise TypeError("No output format,  please fill in extension in the name of output (.csv or .feather)")

    df.index = [x.split(".")[0] for x in df.index.tolist()] # New index names
    df.columns = [x.split(".")[0] for x in df.columns.tolist()] # New column names
    df = df[~df.index.duplicated(keep='first')] # Taking first values in duplicated index

    if args.vst==False:
        df=df.applymap(lambda x: np.log2(x+1)) # Apply log2 for non-vst normalized data

    ## Need to add file name handler
    if '.csv' in args.input_df:
        df.to_csv(args.output)
    elif '.feather' in args.input_df:
        df.to_feather(args.output)