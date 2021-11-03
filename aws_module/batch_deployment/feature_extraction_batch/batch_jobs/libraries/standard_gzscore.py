__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Reference: https://genomebiology.biomedcentral.com/articles/10.1186/gb-2006-7-10-r93
Description: calculating activation score by using z score
"""

import pandas as pd
import numpy as np

class calculator(object):

    def __init__(self, df):
        if df.empty:
            raise ValueError("Input Dataframe is empty, please try with different one.")
        else:
            self.df = df

    # function structure
    def gs_zscore(self, names='Zscore', gene_set=[]):
        zscore=[]
        arr1_index = self.df.index.tolist()
        inter = list(set(arr1_index).intersection(gene_set))

        diff_mean = self.df.loc[inter].mean(axis=0).subtract(self.df.mean(axis=0))
        len_norm = self.df.std(ddof=1, axis=0).apply(lambda x: np.sqrt(len(inter))/x)
        zscore = diff_mean*len_norm
        zscore = zscore.to_frame()
        zscore.columns = [names]
        return zscore