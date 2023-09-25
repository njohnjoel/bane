#!/bin/bash
cd ~/Downloads/
sudo yum -y update
sudo yum install -y vim curl wget python3 unzip epel-release java-1.8.0-openjdk httpd 

#Open Ports 
sudo firewall-cmd --permanent --zone=public --add-port=8080-8095/tcp
sudo firewall-cmd --reload

#Install vlc
sudo yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo yum -y install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
sudo yum -y install vlc
sudo yum -y install vlc-core #(for minimal headless/server install)
sudo yum -y install python-vlc npapi-vlc #(optionals)


#Install Docker, Docker Compose 
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh -y 
sudo usermod -aG docker `whoami`

sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

sudo systemctl start docker
sudo systemctl enable docker

#Install Jenkins & Start httpd
sudo yum -y install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo yum -y install jenkins
sudo sed -i s/8080/8095/g /etc/sysconfig/jenkins

sudo systemctl start jenkins httpd
sudo systemctl enable jenkins httpd

#Install Virtual Box
mkdir ~/Downloads
cd ~/Downloads/
wget https://download.virtualbox.org/virtualbox/6.1.12/VirtualBox-6.1-6.1.12_139181_el7-1.x86_64.rpm
sudo yum localinstall VirtualBox*.rpm
cd -
sudo yum update -y

rm 
sudo init 6 


#Install vscode
#sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
#sudo mv ~/Downloads/devops/vscode.repo /etc/yum.repos.d/
#sudo yum -y install code
