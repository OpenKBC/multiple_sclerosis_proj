import boto3
import os


class botoHandler(object):

    def __init__(self, bucketName):
        s3 = boto3.resource('s3') # s3 resource
        my_bucket = s3.Bucket(bucketName) # Bucket Set
        self.s3 = s3
        self.my_bucket = my_bucket


    def getDirFiles(self, dirname, destpath='/data/'):
        """
        Get all ojects in specific folder
        input: folder name, output destination in container
        output: Downloading objects
        """

        for object_summary in self.my_bucket.objects.filter(Prefix=dirname):
            targetFile=destpath+os.path.basename(object_summary.key)
            self.my_bucket.download_file(object_summary.key, targetFile)

    # Data search
    def search_obj(self, bucketObj, searchList):
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
    def getFile(self, searchList, destpath='/data/'):
        """
        Download file from S3
        input: bucketname, input name, container path for samples
        output: output path string
        """
        s3_list = self.search_obj(self.my_bucket, searchList) # Search file object
        targetFile=destpath+searchList[0]
        self.my_bucket.download_file(s3_list[0], targetFile)

        return targetFile

    # Upload data to S3
    def uploadFile(self, writeFileName, data, datatype='pandas'):
        if datatype=='pandas':
            self.my_bucket.put_object(Key=os.path.basename(writeFileName), Body=data.to_csv()) # Streaming to S3
        elif datatype=='txt':
            self.my_bucket.put_object(Key=os.path.basename(writeFileName), Body=data) # Streaming to S3
        else:
            raise ValueError('Error for upload data type definition')
