#!/bin/bash

## Purpose of this temporary bash file is to calculate large size of data for the project, 
## default data, codes and docker images will be launched on EC2 instance.
## Let members know if you want to get auth for using AWS(credentials), and personal use of EC2 is strictly prohibited.(It is monitored by admin)
## Parsing portion needs to be changed to aws tag work

securityGroupID=sg-08946d1b26a30d376 # default securityGroup for EC2(flask)
subnetID=subnet-5c5f8b53
instanceType=$1 # ml.t2.medium, ml.m5.2xlarge, ml.m5.4xlarge for normal use
VolumeSize=100 # EBS volumne Size
instanceName=$2
roleARN=arn:aws:iam::601333025120:role/service-role/AmazonSageMaker-ExecutionRole-20211004T104830
gitRepo=https://github.com/OpenKBC/multiple_sclerosis_proj_notebook
InstanceInfoFile=InstanceLaunch-Info # Instance launch information

if [ "$instanceType" == "GetURL" ]
then
    # Getting URL for notebook
    echo $(aws sagemaker create-presigned-notebook-instance-url --notebook-instance-name $instanceName)

else
    # Deploy notebook instance
    aws sagemaker create-notebook-instance --notebook-instance-name $instanceName --instance-type $instanceType --role-arn $roleARN \
    --security-group-ids $securityGroupID --subnet-id $subnetID --volume-size-in-gb $VolumeSize --default-code-repository $gitRepo> InstanceInfoFile

    # Check status
    sh utils/sagemaker_check_status.sh $instanceName

    # Getting URL for notebook
    echo $(aws sagemaker create-presigned-notebook-instance-url --notebook-instance-name $instanceName)
fi