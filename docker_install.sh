#!/usr/bin/env bash
#Installation for 16.04
apt install curl
apt-get install gnupg2
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt-get update --fix-missing
sudo apt-get install software-properties-common
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce
sudo apt-get install docker-compose -y
sudo usermod -aG docker "${USER}"
su - "${USER}"