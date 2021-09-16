from notebook_lib.nwpv.nwpv import nwpv_calculation
from notebook_lib.gene_zscore.threaded_gzscore import calculator as gzscore_class

class AdvancedCalculators(object):
    def nwpv_calculator(self, test : list, contol : list, data, save : bool = True):
        """
        NWPV calculator
        Input
        test : test sample list
        control : control sample list
        data : actual input data
        save : saving output or not ?
        
        """
        #NWPV calculation
        nwpv_class = nwpv_calculation(data, test, contol)
        result = nwpv_class.get_result()
        
        if save==True:
            result.to_csv("resultFiles/nwpv_result.csv")
        
        return result

    def activation_score(self, data, gene_set : list):
        
        """
        gene zscore calculator
        Input
        data : actual input data
        gene set : gene set input for calculating activate score
        save : saving output or not ?
        
        """

        #### Init Class and check input file
        zscore_calculator = gzscore_class(data)

        #### Input list should be EntrezIDs(Pathways)
        result = zscore_calculator.gs_zscore(nthread=4, gene_set=gene_set)
        return result