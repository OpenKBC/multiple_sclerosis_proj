class ExtractionToolkit(object):
    def get_sample_name_by_category(dataframe, sampleColumn, dataColname):
        """
        Description:
        This function is for getting sample name by category column
        Don't use this function with continuous values
        
        Input:
        dataframe = Dataframe for extraction
        sampleColumn = Sample name column
        dataColumn = Data value column

        Output:
        Nested list with sample name, ordered sample category
        """
        sample_category = dataframe[dataColname].unique() # get unique value for category
        result = [] # empty list
        for x in sample_category: 
            data = dataframe[dataframe[dataColname]==x][sampleColumn] # get sample name
            result.append(data.values.tolist())
        
        return (result, sample_category)

    def get_sample_expr_in_matrix(dataframe, sampleList : list):
        """
        Description:
        This function is for getting expression subset by using extracted sample set

        Input:
        dataframe = input dataframe
        sampleList = Sample name list to extact, should be list format

        Output:
        Dataframe subset
        """
        intersected_samples = list(set(dataframe.columns.tolist()).intersection(sampleList))
        print("Sample List Count : "+str(len(sampleList)))
        print("Intersected Count : "+str(len(intersected_samples)))
        return dataframe[[intersected_samples]]
