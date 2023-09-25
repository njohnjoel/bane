#!/bin/bash 

sudo yum update -y 
sudo yum install git httpd -y
sudo chmod 777 /var/www/*
cd /var/www/
sudo git clone https://github.com/njohnjoel/html
sudo systemctl start httpd
sudo systemctl enable httpd
sudo systemctl restart httpd