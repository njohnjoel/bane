#!/bin/bash

# probably best to manually type this commands individually checking for problems
 
# snap list | grep -v "^Name" | awk {'print "sudo snap remove " $1'}
 
sudo snap remove snap-store gtk-common-themes gnome-3-28-1804 gnome-3-34-1804 core18 snapd
snap list # expect: No snaps are installed yet. Try 'snap install hello-world'.
 
sudo umount /run/snap/ns
sudo systemctl disable snapd.service snapd.socket snapd.seeded.service snapd.autoimport.service snapd.apparmor.service

 
sudo rm -rf /etc/apparmor.d/usr.lib.snapd.snap-confine.real
 
sudo systemctl start apparmor.service
 
# df | grep snap | awk {'print "sudo umount " $6'}
sudo umount /snap/chromium/1424 /snap/gtk-common-themes/1514 /snap/gnome-3-28-1804/145 /snap/core18/1944 /snap/snapd/10492 /var/snap
sudo apt purge snapd
 

# find / -type d -iname '*snap*'
# (I left the kernel entries well alone)
rm -rf ~/snap
sudo rm -rf /snap /var/snap /var/lib/snapd /var/cache/snapd /usr/lib/snapd /root/snap /root/snap/snap-store /usr/share/doc/libsnapd-glib1 /usr/share/doc/gir1.2-snapd-1
 
cat <<EOF | sudo tee /etc/apt/preferences.d/snapd
Package: snapd
Pin: origin *
Pin-Priority: -1
EOF
 
cat <<EOF | sudo tee /etc/apt/preferences.d/pin-xalt7x-chromium-deb-vaapi
Package: *
Pin: release o=LP-PPA-xalt7x-chromium-deb-vaapi
Pin-Priority: 1337
EOF

#Remove Unwanted Apps 
sudo apt-get purge gnome-mines gnome-mahjongg remmin* rhythmbo* aisleriot deja-dup gnome-sudoku -y 

#Update System
sudo apt update -y && sudo apt upgrade -y 

#Remove System Cache and Updates 
sudo apt autoremove -y 

#Disable TouchPad
xinput disable `xinput | grep "PS/2 Generic Mouse" | awk '{print $6}' | cut -d'=' -f2`

#################################################################
#Install System Apps
#################################################################

#Install SSH, NetTools and devops
sudo apt install ssh net-tools git vim curl wget -y
sudo systemctl start ssh && sudo systemctl enable ssh
#################################################################
#Install Sublime
#################################################################

wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt update -y
sudo apt install sublime-text -y


#Remove System Cache and Updates 
sudo apt autoremove -y 