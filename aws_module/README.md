## AWS module for running the project
* This module supports to run the project codes, pipelines and analysis by launching AWS EC2 instance, currently, this module generates an EC2 instance in AWS by using github code and project S3 data. (Limit: below m5.4xlarge). The EC2 is launched with 200G volumes total initally(default).
* Please contact to members to have credentials to use this service.
* It contains AMI mapping.json for modifying initial storage size

### AWS AMI description
```
aws ec2 describe-images --image-ids ami-0f6304b1dde9413d6 #ubuntu 18.04 LTS with Docker
```

### Requirements on local PC
```
apt-get install awscli
apt-get install jq
```

### Usage on local PC
```
sh aws_module.sh t2.micro #with instance type(t2.micro for testing, maximum : m5.xlarge, m5.2xlarge)
```

### Requirements for docker
* This version has a problem with docker installment in AWS, and docker needs to be installed manually
```
ssh -i MSplatform-key.pem ubuntu@IP_ADDRESS
```

### File information
* InstanceLaunch-Info: This file contains standard EC2 information you launched (IP addr, AZ and etc)
* InstanceVolume-Info: This file contains volume information you launched
* PublicIP: This file contains public IP address of EC2 you launched
* MSplatform-key.pem: This is the key for ssh'ing to EC2

### Services
```
http://yourEC2URL/ # Pipeline Controller
http://yourEC2URL:8888/?token= # Pipeline Controller
```