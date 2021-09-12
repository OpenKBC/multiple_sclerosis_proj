from .statistics import STAT
from scipy import stats
import numpy as np
"""
Manual: https://github.com/swiri021/NWPV2
Reference: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3135688/
Description: Method of combined p-values for getting DEG in dataset
"""



class nwpv_calculation(object):
	def _preprocessing(self, min_adj=1e-16, max_adj=0.9999999999999999):

		for t in self.testtype:
			#####Minvalue adjustment
			self.st_df[t] = self.st_df[t].apply(lambda x: min_adj if x<min_adj else x)

			#####Maxvalue adjustment
			self.st_df[t] = self.st_df[t].apply(lambda x: max_adj if x==1 else x)

			#####Z transform
			self.st_df['%s_z'%(t)] = self.st_df[t].apply(lambda x : stats.norm.ppf(1-x))

	def _combined(self, st):

		for t in self.testtype:
			#####Scaling (StandardScaler)
			self.st_df['%s_scaled'%(t)] = (self.st_df['%s_z'%(t)] - self.st_df['%s_z'%(t)].mean()) / self.st_df['%s_z'%(t)].std()

		# Normal Case
		if len(self.testtype)==3:
			#####Combined zvalue by mean
			self.st_df['combined_pvalue'] = self.st_df['mtest_pvalue_scaled']+self.st_df['ttest_pvalue_scaled']+self.st_df['ranksums_pvalue_scaled']
			self.st_df['combined_pvalue'] = self.st_df['combined_pvalue'].apply(lambda x : float(x)/float(np.sqrt(3.0)))

		# In case of small samples
		elif len(self.testtype)==2:
			self.st_df['combined_pvalue'] = self.st_df['mtest_pvalue_scaled']+self.st_df['ttest_pvalue_scaled']
			self.st_df['combined_pvalue'] = self.st_df['combined_pvalue'].apply(lambda x : float(x)/float(np.sqrt(2.0)))

		#####Transform to P-value
		self.st_df['combined_pvalue'] = self.st_df['combined_pvalue'].apply(lambda x : stats.norm.sf(x)*2)
		self.st_df['combined_pvalue'] = self.st_df['combined_pvalue'].apply(lambda x : float("{:.5f}".format(x)))
		self.st_df = st.storey_fdr(self.st_df, p_name='combined_pvalue')


	def get_result(self):
		result_columns = ['FC']+self.testtype+['combined_pvalue', 'combined_pvalue_adj']
		return self.st_df[result_columns]

	def __init__(self, df, test1, control):
		st = STAT(df, test1, control)
		assert np.prod([x in df.columns.tolist() for x in test1]) and np.prod([x in df.columns.tolist() for x in control]), "Some samples do not exist in DataFrame"
		assert len(test1)>1 and len(control)>1, "Too small size of samples(Control or Test)"

		if len(test1) < 3 or len(control) < 3:
			self.testtype = ['mtest_pvalue', 'ttest_pvalue']
		else:
			self.testtype = ['mtest_pvalue', 'ttest_pvalue', 'ranksums_pvalue']

		self.st_df = st.statistics_result(self.testtype)
		self._preprocessing()
		self._combined(st)
