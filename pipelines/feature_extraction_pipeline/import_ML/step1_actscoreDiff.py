__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: Mimic of notebook code for pipeline work, please see step1 in Jun notebook archive
"""

import pandas as pd
import numpy as np
import itertools
from sys import argv
from lib.statFunction import StatHandler

# Copy of OpenKbcMSToolkit.py
def _get_sample_name_by_contValues(dataframe, sampleColumn, dataColname, threshold):
    cont_df = dataframe.dropna(subset=[dataColname]) # continuous perspective dataframe
    cont_df[dataColname] = cont_df[dataColname].astype(float) # make float

    #threshValue = np.percentile(cont_df[dataColname].values.tolist(), threshold)
    #greater_samples = cont_df.loc[ cont_df[dataColname] >= threshValue, sampleColumn]
    #less_samples = cont_df.loc[ cont_df[dataColname] < threshValue, sampleColumn]  
    
    threshValue_below = np.percentile(cont_df[dataColname].values.tolist(), 100-threshold)
    threshValue_above = np.percentile(cont_df[dataColname].values.tolist(), threshold)

    greater_samples = cont_df.loc[ cont_df[dataColname] > threshValue_below, sampleColumn]
    less_samples = cont_df.loc[ cont_df[dataColname] <= threshValue_above, sampleColumn]

    return (less_samples, greater_samples)

# Copy of OpenKbcMSToolkit.py
def _get_sample_name_by_category(dataframe, sampleColumn, dataColname):
    sample_category = dataframe[dataColname].unique() # get unique value for category
    result = [] # empty list
    for x in sample_category: 
        data = dataframe[dataframe[dataColname]==x][sampleColumn] # get sample name
        result.append(data.values.tolist())
    
    return (result, sample_category)

# This is not global function for other codes, specifically fixed path and data, don't use other purposes.
def _LoadDiseaseDuration(df, meta_data, returntype='long'):
    """
    df : Expression or activation score matrix
    meta_data : meta data which contains duration and sample ID
    output: long DD samples and short DD samples by list, or healthy samples and short DD samples by list
    """
    # checking multiple element for returntype
    if returntype.count(',')>1: raise ValueError('No more than 2 elements for returntype')

    if returntype.find(',')==-1: # if returnType is single(long and healthy)
        # Sample by disease category
        sample_list, sample_category = _get_sample_name_by_category(dataframe=meta_data, sampleColumn='HCVB_ID', dataColname='DiseaseCourse')
        
        # Sort by disease category and exclude uknown samples
        patient_samples = [] # patient samples
        healthy_samples = [] # healthy samples
        for samples, category in zip(sample_list, sample_category):
            if category=='Healthy':
                healthy_samples = samples
            else:
                if category!='Unknown':# Excluding unknown samples
                    patient_samples.append(samples)

        patient_samples = list(itertools.chain(*patient_samples)) # flatten
        patient_samples = list(set(patient_samples).intersection(df.columns.tolist())) # intersected with act score matrix
        healthy_samples = list(set(healthy_samples).intersection(df.columns.tolist())) # intersected with act score matrix
        patient_meta = meta_data.loc[meta_data['HCVB_ID'].isin(patient_samples)] # Make patient metadata

        longDD_samples, shortDD_samples = _get_sample_name_by_contValues(patient_meta, 'HCVB_ID', 'DiseaseDuration', 25)
        longDD_samples = list(set(longDD_samples.values.tolist()).intersection(df.columns.tolist())) # intersected with act score matrix
        shortDD_samples = list(set(shortDD_samples.values.tolist()).intersection(df.columns.tolist())) # intersected with act score matrix

    else: # if returnType is multiple(List)
        # Sample by disease category
        sample_list, sample_category = _get_sample_name_by_category(dataframe=meta_data, sampleColumn='HCVB_ID', dataColname='DiseaseCourse')
        category1 = returntype.split(',')[0]
        category2 = returntype.split(',')[1]
        
        # Sort by disease category and exclude uknown samples
        patient_samples = [] # patient samples
        healthy_samples = [] # healthy samples
        for samples, category in zip(sample_list, sample_category):
            if category==category1:
                category1_samples = list(set(samples).intersection(df.columns.tolist())) # intersected with act score matrix
            elif category==category2:
                category2_samples = list(set(samples).intersection(df.columns.tolist())) # intersected with act score matrix

    # return result
    if returntype=='long':
        return longDD_samples, shortDD_samples
    elif returntype=='healthy':
        return healthy_samples, shortDD_samples
    else:
        return category1_samples, category2_samples

# Simple control for snakemake(no argparse)
actScoreInput=argv[1]
metaData=argv[2]
resultType=argv[3]
outputFile=argv[4]

if __name__ == "__main__":
    df = pd.read_csv(actScoreInput, engine='c', index_col=0).T.dropna() # Activation Score
    meta_data = pd.read_csv(metaData) # Meta data
    longDD_samples, shortDD_samples = _LoadDiseaseDuration(df, meta_data, resultType)
    ranksumSig = StatHandler.calculate_ranksum(df, shortDD_samples, longDD_samples) # get ranksum result
    df.loc[ranksumSig["Names"].values.tolist()].to_csv(outputFile) # Writing
