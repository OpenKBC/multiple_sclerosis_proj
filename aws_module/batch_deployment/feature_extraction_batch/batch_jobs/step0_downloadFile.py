__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

"""
Description: File prepration for AWS batch, Downloading target files in EFS
"""
import os
from libraries.botoClass import botoHandler
from libraries.externalHandler import handlers as dataHandler
import argparse


if __name__ == "__main__":

    ### Get ENV variables
    mainDataBucket = os.environ['mainbucket'] # openkbc-ms-maindata-bucket
    outputPath = os.environ['efspoint'] # /output/
    inputFile = os.environ['startFile'] # counts_vst_CD4.csv
    metaName = os.environ['metafile'] # EPIC_HCvB_metadata_baseline_updated-share.csv
    msigFile = os.environ['msigDBPATH'] # msigdb.v7.4.entrez.gmt

    ### Data prepration
    s3 = botoHandler(mainDataBucket) # Call boto3

    print("Download Path: "+outputPath)
    s3.getFile([metaName], destpath=outputPath) ## This is FIXED parameter
    s3.getFile([msigFile], destpath=outputPath) ## This is FIXED parameter
    s3.getFile([inputFile], destpath=outputPath) ## This is FIXED parameter
    print("Finished donwloading files")