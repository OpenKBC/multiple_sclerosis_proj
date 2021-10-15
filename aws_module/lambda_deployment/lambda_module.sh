#!/bin/bash

##

lambdaRole=arn:aws:iam::601333025120:role/lambda-s3-access-role

## zipping lambda code
#zip -r lambda_functions/spliceColumns.py.zip lambda_functions/spliceColumns.py

## Lambda function create
aws lambda create-function --role $lambdaRole --memory-size 2000 \
--timeout 120 --runtime python3.8 --handler spliceColumns.lambda_handler \
--zip-file fileb://lambda_functions/spliceColumns.py.zip --function-name SpliceColumnFunction > lambda_functions/initial_lambda.log

## Invoke Lambda
aws lambda invoke --function-name SpliceColumnFunction lambda_functions/response.json

# check response 200 here

