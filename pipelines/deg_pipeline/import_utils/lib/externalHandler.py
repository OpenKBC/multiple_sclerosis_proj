import pandas as pd
import itertools

class handlers(object):
    def get_column(filename_with_path,  ext_value, annot='gene_id', sep="\t"):
        """
        filename_with_path = filepath + basename
        ext_value = column name of file
        sep = separator
        """
        temp = pd.read_csv(filename_with_path, sep=sep).set_index(annot) # temp loading
        return temp[[ext_value]]

    def get_samplename(filelist):
        """
        filelist = list of basename
        Lambda function could be--
        _get_samplename = lambda filelist : [x.split("-")[0] for x in filelist]
        """
        sampleName = [x.split("-")[0] for x in filelist]
        return sampleName

    def get_condtionMatrix_by_category(dataframe, sampleColumn, dataColname, conditions:list):
        """
        Transform meta data to DESeq condition matrix
        Input
        dataframe: metadata input
        sampleColumn: Column name for Sample ID in metadata input
        dataColumn: Column name for category value in metadata input
        conditions: Conditions you selected, list type, and it has 2 elements

        Output
        result dataframe with 2 columns (colnames: sampleID, conditions)
        """

        assert len(conditions)==2, "Please make sure that conditions list has 2 elements"

        sampleList = [] # empty list
        conditionValues = []
        for x in conditions: 
            data = dataframe[dataframe[dataColname]==x][sampleColumn] # get sample name
            sampleList.append(data.values.tolist()) # sampleID
            conditionValues.append([x]*len(data.values.tolist())) # condition value
        
        sampleList = list(itertools.chain(*sampleList)) # flatten
        conditionValues = list(itertools.chain(*conditionValues))

        result = pd.DataFrame(data={'sampleID':sampleList, 'conditions':conditionValues}).set_index('sampleID')
        return result
