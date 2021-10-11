cd /home/ubuntu/MSProject/multiple_sclerosis_proj # default project directory
sudo mkdir data/
sudo chown ubuntu:ubuntu data/
aws s3 sync openkbc-ms-maindata-bucket data/ # sync to ec2