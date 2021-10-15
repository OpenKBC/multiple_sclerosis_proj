#!/bin/bash

## Need to push job docker images before running this module

echo "Creating compute environment.."
aws batch create-compute-environment --compute-environment-name activation-score-env \
--type MANAGED --compute-resources type=FARGATE,maxvCpus=4,securityGroupIds=sg-08946d1b26a30d376,subnets=[subnet-46231822,subnet-5c5f8b53]

echo "Creating job queue.."
aws batch create-job-queue --job-queue-name activation-score-queueorder=1,computeEnvironment=activation-score-env --priority 100

echo "Creating job.."
aws batch register-job-definition --job-definition-name activation-score-job --platform-capabilities FARGATE \
--type container --container-properties file://container_configure.json

echo "Submit.."
aws batch submit-job --job-name activation-score-job --job-queue activation-score-queue --job-definition activation-score-job