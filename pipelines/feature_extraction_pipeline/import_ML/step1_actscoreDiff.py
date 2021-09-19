__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: Mimic of notebook code for pipeline work, please see step1 in Jun notebook archive
"""

import pandas as pd
import numpy as np
from sys import argv
from lib.statFunction import StatHandler

# Copy of OpenKbcMSToolkit.py
def _get_sample_name_by_contValues(dataframe, sampleColumn, dataColname, threshold):
    cont_df = dataframe.dropna(subset=[dataColname]) # continuous perspective dataframe
    cont_df[dataColname] = cont_df[dataColname].astype(float) # make float

    threshValue = np.percentile(cont_df[dataColname].values.tolist(), threshold)
    greater_samples = cont_df.loc[ cont_df[dataColname] >= threshValue, sampleColumn]
    less_samples = cont_df.loc[ cont_df[dataColname] < threshValue, sampleColumn]  
    return (less_samples, greater_samples)

# This is not global function for other codes, specifically fixed path and data, don't use other purposes.
def _LoadDiseaseDuration(df, meta_data):
    """
    df : Expression or activation score matrix
    meta_data : meta data which contains duration and sample ID
    output: long DD samples and short DD samples by list
    """
    longDD_samples, shortDD_samples = _get_sample_name_by_contValues(meta_data, 'HCVB_ID', 'DiseaseDuration', 50)
    longDD_samples = list(set(longDD_samples.values.tolist()).intersection(df.columns.tolist())) # intersected with act score matrix
    shortDD_samples = list(set(shortDD_samples.values.tolist()).intersection(df.columns.tolist())) # intersected with act score matrix
    return longDD_samples, shortDD_samples

# Simple control for snakemake(no argparse)
actScoreInput=argv[1]
metaData=argv[2]
outputFile=argv[3]

if __name__ == "__main__":
    df = pd.read_csv(actScoreInput, engine='c', index_col=0).T.dropna() # Activation Score
    meta_data = pd.read_csv(metaData) # Meta data
    longDD_samples, shortDD_samples = _LoadDiseaseDuration(df, meta_data)
    ranksumSig = StatHandler.calculate_ranksum(df, shortDD_samples, longDD_samples) # get ranksum result
    df.loc[ranksumSig["Names"].values.tolist()].to_csv(outputFile) # Writing
