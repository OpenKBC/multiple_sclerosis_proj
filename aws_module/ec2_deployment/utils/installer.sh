storageType=$1 #storage type

# Make usable disk
sudo mkdir /home/ubuntu/MSProject
sudo apt update && sudo apt install -y git
sudo apt install -y awscli

sudo mkfs -t ext4 /dev/nvme1n1 # format attached volume, attempt nvme format
sudo mkfs -t ext4 /dev/xvdf # format attached volume(/dev/sdf), attempt nvme format

sudo mount /dev/nvme1n1 /home/ubuntu/MSProject # Mount to project directory, attempt nvme mount
sudo mount /dev/xvdf /home/ubuntu/MSProject # Mount to project directory, attempt standard mount
#sudo chown -R ubuntu:ubuntu /home/ubuntu/MSProject

# Download all codes
cd /home/ubuntu/MSProject # go to working directory
sudo git clone https://github.com/OpenKBC/multiple_sclerosis_proj.git # git clone the code

# For AWS S3 credential
cd /home/ubuntu
sudo mkdir .aws
sudo chown -R ubuntu:ubuntu /home/ubuntu/.aws/
sudo chown -R ubuntu:ubuntu /home/ubuntu/MSProject/