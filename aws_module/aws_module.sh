#!/bin/bash

## Purpose of this temporary bash file is to calculate large size of data for the project, 
## default data, codes and docker images will be launched on EC2 instance.
## Let members know if you want to get auth for using AWS(credentials), and personal use of EC2 is strictly prohibited.(It is monitored by admin)
## Parsing portion needs to be changed to aws tag work

securityGroupID=sg-08946d1b26a30d376 # default securityGroup for EC2(flask)
instanceType=$1 # t2.micro, m5.4xlarge for normal use
VolumeSize=100 # EBS volumne Size
InstanceInfoFile=InstanceLaunch-Info # Instance launch information
VolumeInfoFile=InstanceVolume-Info # Volume create information
PublicIPFile=PublicIP # Public IP information
PemKeyName=MSplatform-key

## Key gen for EC2. if new key is needed, please use this command lines
#aws ec2 create-key-pair --key-name $PemKeyName --query 'KeyMaterial' --output text > MSplatform-key.pem
## Change auth for pem key
#chmod -R 400 MSplatform-key.pem

## EC2 Instance launch with modifying block-device-mapping, ami-030cd17b75425e48d(plain ubuntu)
aws ec2 run-instances --image-id ami-0f6304b1dde9413d6 --block-device-mappings file://mapping_dockerAMI.json \
--instance-type $instanceType --security-group-ids $securityGroupID --key-name $PemKeyName > $InstanceInfoFile

InstanceIDLine=$(cat $InstanceInfoFile | grep 'InstanceId' | xargs) # Instance ID from info, stripping line
IFS=': ' read -r -a array <<< "$InstanceIDLine" # Split string
element=${array[1]} # extract ID
InstanceID=$(echo ${element/,/} | xargs) # Last cleanup of Instance ID string
echo "Instance ID: $InstanceID"

AZLine=$(cat $InstanceInfoFile | grep 'AvailabilityZone' | xargs) # Get Availability Zone
IFS=': ' read -r -a array <<< "$AZLine" # Split string
element=${array[1]} # extract ID
AvailabilityZone=$(echo ${element/,/} | xargs) # Last cleanup of Instance ID string
echo "Instance AZ: $AvailabilityZone"

#echo "Check ec2 status before create volume"
sh utils/aws_check_status.sh $InstanceID ec2 # Check EC2 running

ip_addr=$(aws ec2 describe-instances --instance-ids $InstanceID --query 'Reservations[0].Instances[0].PublicIpAddress') # get public IP for EC2
ip_addr="${ip_addr%\"}" # Remove double quotes from string
ip_addr="${ip_addr#\"}" # Remove double quotes from string
echo "PublicIP: $ip_addr"
echo "PublicIP: $ip_addr" > $PublicIPFile 

## Volume create (same AZ with EC2)
aws ec2 create-volume --availability-zone $AvailabilityZone --volume-type gp2 --size $VolumeSize > $VolumeInfoFile

VolumeIDLine=$(cat $VolumeInfoFile | grep 'VolumeId' | xargs) # Volume ID from info, stripping line
IFS=': ' read -r -a array <<< "$VolumeIDLine" # Split string
element=${array[1]} # extract ID
VolumeID=$(echo ${element/,/} | xargs) # Last cleanup of Instance ID string
echo "Volume ID: $VolumeID"

## Volume attach
echo "Check ebs status before attach-volume"
sh utils/aws_check_status.sh $VolumeID ebs # Check EBS availability
if [ "$2" == "m5."* ];
then
    echo "NVME volume"
    aws ec2 attach-volume --volume-id $VolumeID --instance-id $InstanceID --device /dev/nvme1n1
    storageType=nvme
else
    aws ec2 attach-volume --volume-id $VolumeID --instance-id $InstanceID --device /dev/sdf
fi

echo "Cooling down starts. It takes more than 8 minutes.."

## 7m, cooling down while AWS is loading and preparing resources
sleep 500

## Running installer
ssh -i MSplatform-key.pem -o StrictHostKeyChecking=no ubuntu@$ip_addr 'bash -s' < utils/installer.sh

## Moving credentials to ec2 for s3 connection
scp -i MSplatform-key.pem -o StrictHostKeyChecking=no credentials ubuntu@$ip_addr:/home/ubuntu/.aws

## S3 sync from S3 project bucket
ssh -i MSplatform-key.pem -o StrictHostKeyChecking=no ubuntu@$ip_addr 'bash -s' < utils/s3Sync.sh

## docker-compose setup
ssh -i MSplatform-key.pem -o StrictHostKeyChecking=no ubuntu@$ip_addr 'bash -s' < utils/docker_setup.sh

echo "AWS module processed.."

#### Running something here
#### Running something here

#### Copy to S3 for resultFiles
#### Copy to S3 for resultFiles

#### Terminateing EC2 here
#aws ec2 stop-instances --instance-ids $InstanceID
#aws ec2 detach-volume --volume-id $VolumeID
#aws ec2 delete-volume --volume-id $VolumeID
#aws ec2 terminate-instances --instance-ids $InstanceID