#!/bin/bash
echo "!!!!!!!!!!!!!!!!!!!"
echo "shell script started!"
echo "!!!!!!!!!!!!!!!!!!!"
sudo apt update
sudo apt upgrade
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
torify python3 -m pip install -r requirements.txt 
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
sudo apt-get install libasound2-dev
sudo apt update && sudo apt upgrade
sudo apt-get install wget software-properties-common dirmngr ca-certificates apt-transport-https -y
sudo apt install mariadb-server mariadb-client
sudo mysql_secure_installation
echo "!!!!!!!!!!!!!!!!!!!"
echo "shell script ended!"
echo "!!!!!!!!!!!!!!!!!!!"
