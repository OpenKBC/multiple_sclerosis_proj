__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: Repeative functions in notebook
"""

from scipy.stats import ranksums
import pandas as pd

class StatHandler(object):
    """
    Statistics handlers

    """
    
    def calculate_ranksum(self, df, sampleList, controlList):
        significant_list = []
        for x in df.index.tolist():
            long_data = df[controlList].loc[x] # Long expr list
            short_data = df[sampleList].loc[x] # Short expr list

            s, p = ranksums(long_data.values.tolist(), short_data.values.tolist()) # ranksum
            fc = short_data.mean(skipna=True) - long_data.mean(skipna=True) # FC

            if p<0.05:
                significant_list.append([x,fc, p]) # sig list

        sig_df = pd.DataFrame(significant_list, columns=["Names", "fc", "pval"])
        return sig_df
