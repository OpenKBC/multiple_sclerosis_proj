## AWS module for running the project
* This module supports to run the project codes, pipelines and analysis by launching AWS Batch. Currently, it is on development phase and this module can run with limited code (Activation Score Calculation).
* Parallel jobs execution is needed lambda function input, please use lambda_deployment section first

### Requirements on local PC
```
apt-get install awscli
apt-get install jq
```

### Usage on local PC
* To change cell type(CD4, CD8, CD14) or category, please replace JSON file to run them separately
```json
    "command":[ "sh", "pipeline_controller.sh", "CD4", "Sex", "M", "F"], # change here
    "mountPoints": [
        {
            "sourceVolume": "efsVolume",
            "containerPath": "/output",
            "readOnly": false
        }
    ],
```
* And run module
```
sh batch_module_singleJob.sh # For CD4 only
```

### Multiple Jobs Flow
![flow1](../../README_resource/batch_detail.png)