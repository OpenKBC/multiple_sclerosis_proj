import pandas as pd
import itertools

class handlers(object):
    def get_column(filename_with_path,  ext_value, annot='gene_id', header_line=0, sep="\t"):
        """
        filename_with_path = filepath + basename
        ext_value = column name of file
        sep = separator
        """

        # Don't use pandas.read_csv because of memory usage
        index_list = []
        value_list = []
        with open(filename_with_path, 'r') as infile:
            for i, line in enumerate(infile):
                line = line.strip()
                if i==header_line: # found header
                    header_info = line.split(sep)
                    value_ext_location = header_info.index(ext_value) # location of value extraction point
                    index_ext_location = header_info.index(annot) # location of value extraction point

                elif i!=header_line:
                    line_list = line.split(sep)
                    index_list.append(str(line_list[index_ext_location])) # Value list
                    value_list.append(float(line_list[value_ext_location])) # Index list

        result_df = pd.DataFrame(data={ext_value: value_list}, index=index_list)
        return result_df

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
