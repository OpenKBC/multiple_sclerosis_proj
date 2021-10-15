#!/bin/bash

## 

echo "Creating compute environment.."
aws batch create-compute-environment --compute-environment-name activation-score-env \
--type MANAGED --compute-resources type=FARGATE,maxvCpus=4

echo "Creating job queue.."
aws batch create-job-queue --job-queue-name activation-score-queue --priority 100

echo "Creating job.."
aws batch register-job-definition --job-definition-name activation-score-job --type container \
--container-properties image=swiri021/activation_score_batch,vcpus=1,memory=5000

echo "Submit.."
aws batch submit-job --job-name activation-score-job --job-queue activation-score-queue