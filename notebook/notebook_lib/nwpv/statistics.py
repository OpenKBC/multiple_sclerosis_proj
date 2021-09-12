import pandas as pd
import numpy as np
import random
from scipy import stats
import itertools


class STAT:

	#######Storey FDR
	def storey_fdr(self, df, p_name):
		neg_ps = float(df.loc[df[p_name] > 0.5].count()[p_name])# Setting absolute negative value
		total_ps = float(df[p_name].count()) # Size normalization

		q_cal = lambda x : x/(neg_ps/total_ps)
		df[p_name+'_adj'] = df[p_name]
		df[p_name+'_adj'] = df[p_name+'_adj'].apply(q_cal)
		df.loc[df[p_name+'_adj'] >= 1.0,p_name+'_adj'] = 0.999999

		return df

	#######NULL distribution creator
	def _md_test_null_dist_creator(self, control, test, perm=2):

		c_index = control.columns.tolist()
		t_index = test.columns.tolist()

		if len(c_index)==1:
			null_samples = [[c_index[0], t_index[0]], [c_index[0], t_index[1]], [t_index[0], t_index[1]]]
		else:
			null_samples = [random.sample(c_index+t_index, len(c_index+t_index)) for x in range(perm)]
		null_values = []
		total_df = pd.concat([control, test], axis=1)

		for s in null_samples:
			n1 = s[:len(control.columns.tolist())]
			n2 = s[len(control.columns.tolist()):]

			n1_median = [total_df[n1].loc[g].median(skipna=True) for g in total_df.index.tolist()]
			n2_median = [total_df[n2].loc[g].median(skipna=True) for g in total_df.index.tolist()]
			result = [n2_median[a]-n1_median[a] for a in range(len(n1_median))]
			null_values.append(result)



		null_values = list(itertools.chain(*null_values))
		null_values = pd.DataFrame(data=null_values, columns=['values'])
		return null_values

	#######Median-test(Pvalue from null distribution)
	def _get_pvalue(self, test_value, null_dist):

		high_v = len(null_dist[null_dist['values']>test_value].index.tolist())
		low_v = len(null_dist[null_dist['values']<test_value].index.tolist())

		if test_value>0:
			result = float(high_v)/float(len(null_dist.index.tolist()))
		else:
			result = float(low_v)/float(len(null_dist.index.tolist()))
		return result

	#######T-test
	def _ttest_ind_df(self, control, test):
		pv_arr = []
		for x in test.index.tolist():
			t, pv = stats.ttest_ind(test.loc[x].values.tolist(), control.loc[x].values.tolist(), nan_policy='omit')
			pv_arr.append(pv)
		result = pd.DataFrame(data=pv_arr, index=test.index, columns=['ttest_pvalue'])
		return result

	#######One Sample T-test
	def _ttest_1samp_df(self, control, test):
		pv_arr = []
		for x in test.index.tolist():
			t, pv = stats.ttest_1samp(test.loc[x].values.tolist(), control.loc[x].values.tolist(), nan_policy='omit')
			pv_arr.append(pv[0])
		result = pd.DataFrame(data=pv_arr, index=test.index, columns=['ttest_pvalue'])
		return result

	#######Ranksums test
	def _ranksums_df(self, control, test):
		pv_arr = []
		for x in test.index.tolist():
			t, pv = stats.ranksums(test.loc[x].dropna().values.tolist(), control.loc[x].dropna().values.tolist())
			pv_arr.append(pv)
		result = pd.DataFrame(data=pv_arr, index=test.index, columns=['ranksums_pvalue'])
		return result

	#######DataFrame Result
	def statistics_result(self, type):
		# Make null dist for median test
		null_values = self._md_test_null_dist_creator(self.control, self.test1)
		test_df_ar = self.test1.median(axis=1, skipna=True)-self.control.median(axis=1, skipna=True)
		test_df_ar = test_df_ar.to_frame()
		test_df_ar.columns = ['Med']

		# Fold Change
		test_df_ar['FC'] = self.test1.mean(axis=1, skipna=True)-self.control.mean(axis=1, skipna=True)


		# Normal Case
		if len(type)==3:
			# Median test
			test_df_ar['mtest_pvalue'] = test_df_ar['Med'].apply(lambda x : self._get_pvalue(x, null_values))
			# T-test
			test_df_ar['ttest_pvalue'] = self._ttest_ind_df(self.control, self.test1)
			# Ranksums test
			test_df_ar['ranksums_pvalue'] = self._ranksums_df(self.control, self.test1)

		# In case of small samples
		elif len(type)==2:
			# Median test
			test_df_ar['mtest_pvalue'] = test_df_ar['Med'].apply(lambda x : self._get_pvalue(x, null_values))
			# T-test
			test_df_ar['ttest_pvalue'] = self._ttest_ind_df(self.control, self.test1)

		return test_df_ar


	def __init__(self, df, test1, control):
		######Make control and test dataframe
		self.test1 = df[test1]
		self.control = df[control]
