#!/bin/bash

## Need to push job docker images before running this module. This is an example parallelized AWS batch by using lambda function.
## Lambda function generates sliced expression matrix in casting bucket and batch grabs those casting results as input.
## This could be replaced to array job, and current version is controlled by env varibles and created single jobs for each input variable

dataBucket='openkbc-ms-casting-bucket'

mkdir logs/
mkdir json_setfiles/

echo "Creating compute environment.."
aws batch create-compute-environment --compute-environment-name activation-score-env \
--type MANAGED --compute-resources type=FARGATE,maxvCpus=4,securityGroupIds=sg-08946d1b26a30d376,subnets=[subnet-46231822,subnet-5c5f8b53]

sleep 5

echo "Creating job queue.."
aws batch create-job-queue --job-queue-name activation-score-queue --compute-environment-order order=1,computeEnvironment=activation-score-env --priority 100

# Get AWS s3 input list
inputList=($(aws s3 ls $dataBucket | awk '{print $4}'))

COUNTER=0 # counter
for filename in "${inputList[@]}"
do
    ## JSON create for job registering (Change input name and input bucket name)
    sed "/counts_vst_CD4.converted.csv/s/:".*"/: \"${filename}\"/" container_configure.json | sed "/openkbc-ms-maindata-bucket/s/:".*"/: \"${dataBucket}\"/" > json_setfiles/container_configure_${COUNTER}.json

    ## Job registering
    echo "Creating $COUNTER -job.."
    aws batch register-job-definition --job-definition-name activation-score-job_${COUNTER} --platform-capabilities FARGATE \
    --type container --container-properties file://json_setfiles/container_configure_${COUNTER}.json

    sleep 3

    ## Job submit
    echo "$COUNTER -job Submit.."
    aws batch submit-job --job-name activation-score-job_${COUNTER} --job-queue activation-score-queue --job-definition activation-score-job_${COUNTER} > logs/job.submitted_${COUNTER}
    COUNTER=$[$COUNTER +1]
done
echo "Job submission has been completed.."