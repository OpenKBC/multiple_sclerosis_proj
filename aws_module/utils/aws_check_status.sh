#!/bin/bash

## Purpose of this bash file is running while EC2 is ready. When it is ready, automatically it will be out
objectID=$1
objectState=dummy

if [ "$2" == "ec2" ]
then
    while [ "$objectState" != "running" ];do # EC2 running checking
        sleep 1
        objStatuses=$(aws ec2 describe-instance-status --instance-id $objectID)
        objectState=$( jq --jsonargs '.InstanceStatuses | .[] | .InstanceState.Name' <<< "${objStatuses}" )
        objectState="${objectState%\"}" # Remove double quotes from string
        objectState="${objectState#\"}" # Remove double quotes from string
    done
elif [ "$2" == "ebs" ]
then
    while [ "$objectState" != "available" ];do # EBS available checking
        sleep 1
        objStatuses=$(aws ec2 describe-volumes --volume-ids $objectID)
        objectState=$( jq --jsonargs '.Volumes | .[] | .State' <<< "${objStatuses}" )
        objectState="${objectState%\"}" # Remove double quotes from string
        objectState="${objectState#\"}" # Remove double quotes from string
    done
fi