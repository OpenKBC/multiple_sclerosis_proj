import pandas as pd
import numpy as np
import os
import boto3

def gs_zscore(df, names='Zscore', gene_set=[]):
    zscore=[]
    arr1_index = df.index.tolist()
    inter = list(set(arr1_index).intersection(gene_set))

    diff_mean = df.loc[inter].mean(axis=0).subtract(df.mean(axis=0))
    len_norm = df.std(ddof=1, axis=0).apply(lambda x: np.sqrt(len(inter))/x)
    zscore = diff_mean*len_norm
    zscore = zscore.to_frame()
    zscore.columns = [names]
    return zscore

# Data search
def search_obj(bucketObj, searchList):
    """
    Search function for s3 objects
    input: s3 object in boto3, list of items
    output: s3 object key list
    """
    result=[]
    for target in searchList:
        for candidate in bucketObj.objects.all():
            if str(candidate.key).find(target) > -1: # if target finds in string
                result.append(candidate.key) # get key
    return result

# Get data from S3
def getFile(bucketName, searchList, destpath='/data/'):
    #bucketName = 'openkbc-ms-maindata-bucket'
    s3 = boto3.resource('s3') # s3 resource
    my_bucket = s3.Bucket(bucketName) # Bucket Set
    
    #searchList = ['counts_vst_CD4.converted.csv', 'counts_vst_CD8.converted.csv', 'counts_vst_CD14.converted.csv'] # filename list
    s3_list = search_obj(my_bucket, searchList)
    
    source_dir = destpath # Only writable folder in lambda
    targetFile=source_dir+searchList[0]
    s3.Bucket(bucketName).download_file(s3_list[0], targetFile)

    return targetFile

# Upload data to S3
def uploadFile(bucketName, writeFileName, data):
    s3 = boto3.resource('s3') # s3 resource
    s3.Bucket(bucketName).put_object(Key=os.path.basename(writeFileName), Body=data.to_csv()) # Streaming to S3

if __name__ == "__main__":

    ### Data prepration
    main_bucket = 'openkbc-ms-maindata-bucket'
    MSIGDB_PATH = getFile(main_bucket, ['msigdb.v7.4.entrez.gmt'])
    input_df = getFile(main_bucket, ['counts_vst_CD4.converted.csv'])

    ### Actual job
    # .gmt parsing
    count = 0
    gmt_arr = [] # gmt parsing array

    with open(MSIGDB_PATH, 'r') as infile:
       for line in infile:
            gmt_value = line.strip().split("\t") # splitting line
            sig_names = gmt_value[0] # signature name
            gene_list = gmt_value[2:] # gene list
            gmt_arr.append([sig_names]+gene_list)

    infile.close()

    # Sample loading, and some entrezIDs are duplicated in the matrix
    gexpr = pd.read_csv(input_df, index_col=0)
    gexpr.index = [x.split(".")[0] for x in gexpr.index.tolist()] # remove effect from R make.names
    gexpr = gexpr.groupby(gexpr.index).max() # keeping max for duplicated index
     
    zscore_arr = [] # result array
     
    for sig in gmt_arr:
         zscore_value = gs_zscore(gexpr, names=sig[0], gene_set=sig[1:]) # using standard, threaded version has an error
         zscore_arr.append(zscore_value)
    zscore_df = pd.concat(zscore_arr, axis=1) # make dataframe

    ### Result upload
    upload_bucket = 'openkbc-ms-casting-bucket'
    uploadFile(upload_bucket, 'output.csv', zscore_df)