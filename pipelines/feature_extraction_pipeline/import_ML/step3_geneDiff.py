__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: Mimic of notebook code for pipeline work, please see step3 in Jun notebook archive
"""

from scipy.stats import ranksums
import pandas as pd
from sys import argv

## call previous step for calling internal function
import step1_actscoreDiff
from lib.statFunction import StatHandler
import itertools

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

# Simple control for snakemake(no argparse)
actScoreInput=argv[1]
geneExprInput=argv[2]
metaData=argv[3]
msigDBPath=argv[4]
outputFile=argv[5]

if __name__ == "__main__":

    df_expr = pd.read_csv(geneExprInput, engine='c', index_col=0) # get expr
    meta_data = pd.read_csv(metaData) # metadata
    longDD_samples, shortDD_samples = step1_actscoreDiff._LoadDiseaseDuration(df_expr, meta_data) # get samples for LDD SDD

    geneList = _extract_geneSignature(actScoreInput, msigDBPath) # Extracting genes
    print("Total extracted genes: "+ str(len(geneList)))

    gene_intersected = list(set(geneList).intersection(df_expr.index.tolist())) # intersected between expr and actScore sig
    df_expr = df_expr[longDD_samples+shortDD_samples].loc[gene_intersected].dropna() # selected expr only
    
    ranksumSig = StatHandler.calculate_ranksum(df_expr, shortDD_samples, longDD_samples) # get ranksum result
    df_expr.loc[ranksumSig["Names"].values.tolist()].to_csv(outputFile) # Writing