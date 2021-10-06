## Instruction
* The project supports AWS deployment and it needs credentials approval by admin. Currently the module provides EC2 and SageMaker. 

### Requirements on local PC
```
apt-get install awscli
apt-get install jq
```

## Modules List
| Name | Description | Main exec file |
|---------|---------|---------|
| ec2_deployment | Module for EC2 auto-deployment | aws_module.sh |
| sageMaker_deployment | Module for sageMaker auto-deployment | sagemaker_module.sh |

#### Detail Map
![overview1](../README_resource/aws_detail.png)
