__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: This is batch job for uploading result file to S3.
"""
import os
import argparse
from libraries.botoClass import botoHandler

if __name__ == "__main__":
    uploadDataBucket = os.environ['uploadbucket'] # openkbc-ms-casting-bucket
    SharedFilePath = os.environ['efspoint'] # Main data path here, goes to EFS volume, /output/
    step1Input = os.environ['startFile'] # counts_vst_CD4.csv

    ### Data prepration
    outputFile = SharedFilePath+os.path.basename(step1Input).replace('.csv', '.step7.csv') # replace to step6 output
    s3 = botoHandler(uploadDataBucket) # Call boto3
    f = open(outputFile, 'r').read()
    s3.uploadFile(outputFile, f, datatype='txt')