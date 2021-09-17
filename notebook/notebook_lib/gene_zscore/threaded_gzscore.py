__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
EXPERIMENTAL CODE
Manual: https://github.com/swiri021/Threaded_gsZscore
Reference: https://genomebiology.biomedcentral.com/articles/10.1186/gb-2006-7-10-r93
Description: calculating activation score by using threaded z score
"""
import pandas as pd
import numpy as np
import threading
import functools
import itertools
import math

class funcThread(object):
    def __init__(self):
        print ("Loaded Threads")

    def __call__(self, func):
        @functools.wraps(func)
        def run(*args, **kwargs):
            print ("Number of Threads : %d"%(kwargs['nthread']))

            threads = [None]*kwargs['nthread']
            container = [None]*kwargs['nthread']

            ####Divide Samples by number of threads
            i_col = len(args[1].columns.tolist())
            contents_numb = i_col/kwargs['nthread']
            #contents_numb = math.ceil(contents_numb)
            contents_numb = round(contents_numb) # round for matching thread number

            split_columns = [args[1].columns.tolist()[i:i+contents_numb] for i in range(0, len(args[1].columns.tolist()), contents_numb)]
            if len(split_columns)>kwargs['nthread']:
                split_columns = split_columns[:kwargs['nthread']-1] + [list(itertools.chain(*split_columns[kwargs['nthread']-1:]))]
                #split_columns[len(split_columns)-2] = split_columns[len(split_columns)-2]+split_columns[len(split_columns)-1]
                #split_columns = split_columns[:len(split_columns)-1]

            ####Running threads
            for i, item in enumerate(split_columns):
                threads[i] = threading.Thread(target = func, args=(args[0], args[1][item], container, i), kwargs=kwargs)
                threads[i].start()
            for i in range(len(threads)):
                threads[i].join()

            return pd.concat(container, axis=0)

        return run


class calculator(object):

    def __init__(self, df):
        if df.empty:
            raise ValueError("Input Dataframe is empty, please try with different one.")
        else:
            self.df = df

    # Wrapper for controlling Threads
    def gs_zscore(self, nthread=4, gene_set=[]):
        arr1 = self.df
        container = None
        i = None

        return self._calculating(arr1, container, i, nthread=nthread, gene_set=gene_set)

    # function structure
    # args(input, container, thread_index , **kwargs)
    @funcThread()
    def _calculating(self, arr1, container, i, nthread=4, gene_set=[]):
        zscore=[]
        arr1_index = arr1.index.tolist()
        inter = list(set(arr1_index).intersection(gene_set))

        diff_mean = arr1.loc[inter].mean(axis=0).subtract(arr1.mean(axis=0))
        len_norm = arr1.std(ddof=1, axis=0).apply(lambda x: np.sqrt(len(inter))/x)
        zscore = diff_mean*len_norm
        zscore = zscore.to_frame()
        zscore.columns = ['Zscore']
        container[i] = zscore
        ##No Return