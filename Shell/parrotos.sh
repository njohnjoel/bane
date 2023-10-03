#!/bin/bash

# Update and upgrade packages
sudo apt update -y && sudo apt upgrade -y

# Install required packages
sudo apt install cups software-properties-common gnome-disk-utility curl wget git photorec ddrescue-gui snapd -y
sudo apt install snap-store -y

# Install Google Chrome Browser
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y

# Install Brave Browser
sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list
sudo apt update
sudo apt install brave-browser -y

# Installing Brother Printer Driver
cd ~/Downloads
wget https://download.brother.com/welcome/dlf006893/linux-brprinter-installer-2.2.3-1.gz
gunzip linux-brprinter-installer-*.gz
sudo bash linux-brprinter-installer-2.2.3-1 DCP-L2520D

# Start and enable CUPS service
sudo systemctl start cups
sudo systemctl enable cups

# Configure Brother Printer
sudo lpadmin -p DCPL2520D -E -v usb://dev/usb/lp0 -P /usr/share/ppd/brother/brother-DCPL2520D-cups-en.ppd

# Install IntelliJ IDEA Community Edition via Snap
sudo snap install intellij-idea-community --classic --edge

# Clean up unused packages
sudo apt autoremove -y