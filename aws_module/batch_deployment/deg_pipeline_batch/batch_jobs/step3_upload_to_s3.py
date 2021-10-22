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

## argparse setting
parser = argparse.ArgumentParser(prog='step3_upload_to_s3.py')

parser.add_argument('-c','--ctype', type=str, dest='celltype', required=True,\
     choices=['CD4','CD8','CD14'],help='Cell type for extraction, default = CD8')

args = parser.parse_args()

if __name__ == "__main__":
    uploadDataBucket = os.environ['uploadbucket'] # openkbc-ms-casting-bucket
    outputPath = os.environ['efspoint'] # /output/

    ### Data prepration
    s3 = botoHandler(uploadDataBucket) # Call boto3
    outputFile = outputPath+'DEG_'+args.celltype+'.result'
    f = open(outputFile, 'r').read()
    s3.uploadFile(outputFile, f, datatype='txt')