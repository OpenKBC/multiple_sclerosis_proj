__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: Mimic of notebook code for pipeline work, please see step3 in Jun notebook archive
"""

import os
from scipy.stats import ranksums
import pandas as pd

## call previous step for calling internal function
import step4_actscoreDiff
from libraries.statFunction import StatHandler
import itertools
import argparse

def _extract_geneSignature(actInput, msigDBPath):
    #Data loading
    df = pd.read_csv(actInput, engine='c', index_col=0) # activation score data for extracting gene signature

    # MsigDB Parsing
    gmt_arr = [] # gmt parsing array
    with open(msigDBPath, 'r') as infile:
        for line in infile:
            gmt_value = line.strip().split("\t") # splitting line
            sig_names = gmt_value[0] # signature name
            gene_list = gmt_value[2:] # gene list
            gmt_arr.append([sig_names]+gene_list)

    gmt_ext_arr = [x[1:] for x in gmt_arr if x[0] in df.index.tolist()] # Selected signature genes
    gmt_ext_arr = list(itertools.chain(*gmt_ext_arr))
    gmt_ext_arr = list(set(gmt_ext_arr)) # remove duplicated
    return gmt_ext_arr

parser = argparse.ArgumentParser(prog='step6_geneDiff.py')
# Input data
parser.add_argument('-t','--type', dest='resultType', default='RR,CIS',\
     help='Result type, ex: long, healthy, "RR,CIS" ')
args = parser.parse_args()


if __name__ == "__main__":

    SharedFilePath = os.environ['efspoint'] # Main data path here, goes to EFS volume
    metaName = os.environ['metafile'] # EPIC_HCvB_metadata_baseline_updated-share.csv
    msigFile = os.environ['msigDBPATH'] # msigdb.v7.4.entrez.gmt
    step1Input = os.environ['startFile'] # counts_vst_CD4.csv

    inputExprFile = SharedFilePath+os.path.basename(step1Input).replace('.csv', '.step2.csv') # replace to step2 input, expression
    inputFile = SharedFilePath+os.path.basename(step1Input).replace('.csv', '.step5.csv') # replace to step5 input

    df_expr = pd.read_csv(SharedFilePath+inputExprFile, engine='c', index_col=0) # get expr
    meta_data = pd.read_csv(SharedFilePath+metaName) # metadata
    longDD_samples, shortDD_samples = step4_actscoreDiff._LoadDiseaseDuration(df_expr, meta_data, args.resultType) # get samples for LDD SDD

    geneList = _extract_geneSignature(inputFile, SharedFilePath+msigFile) # Extracting genes
    print("Total extracted genes: "+ str(len(geneList)))

    gene_intersected = list(set(geneList).intersection(df_expr.index.tolist())) # intersected between expr and actScore sig
    df_expr = df_expr[longDD_samples+shortDD_samples].loc[gene_intersected].dropna() # selected expr only
    
    outputFile = SharedFilePath+os.path.basename(step1Input).replace('.csv', '.step6.csv') # replace to step6 output
    ranksumSig = StatHandler.calculate_ranksum(df_expr, shortDD_samples, longDD_samples) # get ranksum result
    df_expr.loc[ranksumSig["Names"].values.tolist()].to_csv(outputFile) # Writing