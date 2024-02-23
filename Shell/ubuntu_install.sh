#!/bin/bash

# Update system
echo "updating system"
sudo apt update && sudo apt upgrade -y

# Install Python3

sudo apt install python3 -y

# Install Git
sudo apt install git -y

# Install wget
sudo apt install wget -y

# Install curl
sudo apt install curl -y

# Install DBeaver
sudo snap install dbeaver-ce

# Install Notepadqq
sudo snap install notepadqq

# Install Visual Studio Code
sudo snap install code --classic

# Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt install -f

# Install AnyDesk
wget -qO - https://keys.anydesk.com/repos/DEB-GPG-KEY | sudo apt-key add -
echo "deb http://deb.anydesk.com/ all main" | sudo tee /etc/apt/sources.list.d/anydesk-stable.list
sudo apt update
sudo apt install anydesk

# Install draw.io
sudo snap install drawio

# Install Zoom
wget https://zoom.us/client/latest/zoom_amd64.deb
sudo dpkg -i zoom_amd64.deb
sudo apt install -f

# Install IntelliJ Community Edition
sudo snap install intellij-idea-community --classic

# Autoremove unused packages
sudo apt autoremove -y
