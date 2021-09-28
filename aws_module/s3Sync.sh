cd /home/ubuntu/MSProject/multiple_sclerosis_proj # default project directory
sudo mkdir data/
sudo chown ubuntu:ubuntu data/
aws s3 sync s3://openkbc-ms-bucket/ data/ # sync to ec2