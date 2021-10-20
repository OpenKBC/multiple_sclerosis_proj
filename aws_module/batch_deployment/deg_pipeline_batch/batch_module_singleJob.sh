#!/bin/bash

## Need to push job docker images before running this module, this module is an example for how to run single job for AWS batch.
## It generate zscore by using gene matrix in main bucket, it is not parallelized.

echo "Creating compute environment.."
aws batch create-compute-environment --compute-environment-name deg-pipeline-env \
--type MANAGED --compute-resources type=FARGATE,maxvCpus=8,securityGroupIds=sg-08946d1b26a30d376,subnets=[subnet-46231822,subnet-5c5f8b53]

sleep 3

echo "Creating job queue.."
aws batch create-job-queue --job-queue-name deg-pipeline-queue --compute-environment-order order=1,computeEnvironment=deg-pipeline-env --priority 100

echo "Creating job.."
aws batch register-job-definition --job-definition-name deg-pipeline-job --platform-capabilities FARGATE \
--type container --container-properties file://container_configure.json

echo "Submit.."
aws batch submit-job --cli-input-json file://submit_configure.json > job.submitted

sleep 2

jobID=$(jq '.jobId' job.submitted)
jobID="${jobID%\"}" # Remove double quotes from string
jobID="${jobID#\"}" # Remove double quotes from string

## Purpose of this bash file is running while EC2 is ready. When it is ready, automatically it will be out
while [ "$objectState" != "SUCCEEDED" ];do # EC2 running checking
    sleep 1
    objStatuses=$(aws batch describe-jobs --jobs $jobID)
    objectState=$( jq --jsonargs '.jobs | .[] | .status' <<< "${objStatuses}" )
    objectState="${objectState%\"}" # Remove double quotes from string
    objectState="${objectState#\"}" # Remove double quotes from string
    echo "Job status: $objectState "
done
echo "Job has been completed.."