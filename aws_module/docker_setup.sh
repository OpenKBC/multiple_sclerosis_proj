# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# docker-compose up for containers
cd /home/ubuntu/MSProject/multiple_sclerosis_proj
sudo docker-compose -f docker-compose.AWS.yaml up --detach