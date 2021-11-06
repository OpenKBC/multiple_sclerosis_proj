#!/bin/bash

## Need to push job docker images before running this module, this module is an example for how to run single job for AWS batch.
## This is same pipeline with snakemake pipeline and it will generate DEG result for one cell type.

echo "Creating compute environment.."
aws batch create-compute-environment --compute-environment-name deg-pipeline-env \
--type MANAGED --compute-resources type=FARGATE,maxvCpus=8,securityGroupIds=sg-08946d1b26a30d376,subnets=[subnet-c6bdede9,subnet-23a0b868]

sleep 3

echo "Creating job queue.."
aws batch create-job-queue --job-queue-name deg-pipeline-queue --compute-environment-order order=1,computeEnvironment=deg-pipeline-env --priority 100

sleep 5

echo "Creating job.."
aws batch register-job-definition --job-definition-name deg-pipeline-job --platform-capabilities FARGATE \
--type container --container-properties file://container_configure.json

sleep 5

echo "Submit.."
aws batch submit-job --cli-input-json file://submit_configure.json > job.submitted

sleep 2

echo "Job has been submitted and go to console for checking further status.."