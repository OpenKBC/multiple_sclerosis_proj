import json
import boto3
import os
import math

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

def parse_data(datapath):
    """
    Parsing function instead of pandas
    input: raw data path
    output: header, index, value lists
    """
    header = [] # header
    index = [] # index
    value = [] # value
    
    counter = 0 # Indicator and stopper
    with open(datapath, 'r') as f:
        for line in f.readlines():
            line=line.strip()
            data = line.split(',')
            if counter==0: # header location
                data = [ x.replace('"','')for x in data ] # cleanup sample name
                header = data
            else:
                index.append(data[0].replace('"',''))
                data = data[1:]
                value.append(data)
            counter+=1
            #if counter ==5:
            #    break;
    f.close()
    os.remove(datapath) # release space for tmp
    
    return header, index, value
    
def samplespliter(header,index,value,cut_element):
    """
    Sample splitter by using upstream lists
    input: header list, index list, value nested list, cut interval
    output: list of outputfile(string format)
    """
    result = []
    for i in range(0, len(header), cut_element):
        block_result = []
        block_result.append(","+",".join(header[i:i+cut_element])) # attach header
        for idx, val in zip(index, value):
            block_result.append(",".join([idx]+val[i:i+cut_element])) # attach header
        
        block_result = "\n".join(block_result)
        result.append(block_result)
    
    return result
    

def lambda_handler(event, context):
    """
    Main function with event and context(trigger and destination)
    """

    bucketName = 'openkbc-ms-maindata-bucket'
    s3 = boto3.resource('s3') # s3 resource
    my_bucket = s3.Bucket(bucketName) # Bucket Set
    
    searchList = ['counts_vst_CD4.converted.csv', 'counts_vst_CD8.converted.csv', 'counts_vst_CD14.converted.csv'] # filename list
    s3_list = search_obj(my_bucket, searchList)
    
    source_dir = '/tmp/' # Only writable folder in lambda
    targetFile=source_dir+searchList[0]
    s3.Bucket(bucketName).download_file(s3_list[0], targetFile)
    
    header, index, value = parse_data(targetFile) # get header, index and value
    block = 5 # sample blocks, could be user input
    cutInterval = math.ceil(len(header)/block) # Get how many elements add on a block
    
    outputList = samplespliter(header, index, value, cutInterval) # Make file data
    uploadBucket = 'openkbc-ms-casting-bucket' # Target bucket
    
    for i in range(0, len(outputList)):
        writeFileName = targetFile.replace('.csv','.'+str(i)+'.csv') # Output Naming
        s3.Bucket(uploadBucket).put_object(Key=os.path.basename(writeFileName), Body=outputList[i]) # Streaming to S3

    return {
        'statusCode': 200,
        'body': json.dumps("Success")
    }
