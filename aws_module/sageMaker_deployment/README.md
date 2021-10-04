## SageMaker module for running the project
* This module supports to run notebook instance by using AWS SageMaker, currently, this module generates a notebook instance in AWS by using github repo and project S3 data connection. (Limit: below ml.m5.4xlarge). The instance is launched with 100G volumes total initally(default).
* Please contact to members to have credentials
* It takes some minutes(5mins ~ 10mins) for launching the instance

### Requirements on local PC
```
apt-get install awscli
apt-get install jq
```

### Usage on local PC
```
# Launch the instance, it will provide URL at the last process
sh sagemaker_module.sh ml.t2.medium your_instance_name #with instance type(ml.t2.medium for testing, maximum : ml.m5.xlarge, ml.m5.2xlarge)
# Get URL for notebook page if you forget or your session is expired
sh sagemaker_module.sh GetURL
```

### File information
* InstanceLaunch-Info: This file contains instance arn

### How to code in SageMaker
* Please refer to [Instruction](https://github.com/OpenKBC/multiple_sclerosis_proj_notebook/blob/main/Code_Instruction_and_Example.ipynb) in the instance