#!/bin/bash

## Purpose of this bash file is to launch a stack for ec2 module by using cloudformation 
instanceType=$1 # Please refer to possible instance
stackName=$2
aws cloudformation deploy --stack-name $stackName --template-file cloudformation_ec2.yaml --parameter-overrides InstanceType=$instanceType 
echo "Please, ssh to instance and compose up containers manually.."