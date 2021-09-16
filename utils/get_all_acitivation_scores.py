import glob
import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(prog='get_all_activattion_scores.py')
# Input data
parser.add_argument('-i','--input', type=str, dest='input_df', required=True,\
     help='Input data matrix')
# Output path
parser.add_argument('-o','--output', type=str, dest='filepath', required=True, default='./',\
     help='Output directory')
args = parser.parse_args()

MSIGDB_PATH = "data/MsigDB_list/msigdb.v7.4.entrez.gmt"
