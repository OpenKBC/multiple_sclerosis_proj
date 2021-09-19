__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: Repeative functions in notebook
"""
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV

from scipy.stats import ranksums
import pandas as pd
import numpy as np

class StatHandler(object):
    """
    Statistics handlers

    """
    
    def calculate_ranksum(df, sampleList, controlList):
        """
        ranksum statistics wrapper by following notebook

        Input:
        df = Sample dataframe
        sampleList = short disease duration
        controlList = long disease duration

        Output:
        significant index(statistics and pvalue) by dataframe
        """
    
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

    def calculate_RFECV(df, X, y, rankthresh=10):
        ## Log function is needed here
        ## Reference: 
        ## https://scikit-learn.org/stable/auto_examples/feature_selection/plot_rfe_with_cross_validation.html

        estimator = SVC(kernel="linear") # linear
        min_features_to_select = 1
        rfecv = RFECV(estimator=estimator, step=1, cv=StratifiedKFold(2),\
            scoring='accuracy', min_features_to_select=min_features_to_select)
        rfecv.fit(X, y)

        print("Optimal number of features : %d" % rfecv.n_features_)
        return np.where(rfecv.ranking_ <= int(rankthresh))

        """
        # Muted visualization part
        # Plot number of features VS. cross-validation scores
        plt.figure()
        plt.xlabel("Number of features selected")
        plt.ylabel("Cross validation score (nb of correct classifications)")
        plt.plot(range(min_features_to_select, len(rfecv.grid_scores_) + min_features_to_select), rfecv.grid_scores_)
        plt.show()
        """