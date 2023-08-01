#!/bin/bash

# probably best to manually type this commands individually checking for problems
 
# snap list | grep -v "^Name" | awk {'print "sudo snap remove " $1'}
 
sudo snap remove snap-store
sudo snap remove gtk-common-themes
sudo snap remove gnome-3-28-1804
sudo snap remove gnome-3-34-1804
sudo snap remove core18
sudo snap remove snapd
snap list # expect: No snaps are installed yet. Try 'snap install hello-world'.
 
sudo umount /run/snap/ns
 
sudo systemctl disable snapd.service
sudo systemctl disable snapd.socket
sudo systemctl disable snapd.seeded.service
sudo systemctl disable snapd.autoimport.service
sudo systemctl disable snapd.apparmor.service
 
sudo rm -rf /etc/apparmor.d/usr.lib.snapd.snap-confine.real
 
sudo systemctl start apparmor.service
 
# df | grep snap | awk {'print "sudo umount " $6'}
sudo umount /snap/chromium/1424
sudo umount /snap/gtk-common-themes/1514
sudo umount /snap/gnome-3-28-1804/145
sudo umount /snap/core18/1944
sudo umount /snap/snapd/10492
sudo umount /var/snap
 
sudo apt purge snapd
 

# find / -type d -iname '*snap*'
# (I left the kernel entries well alone)
rm -rf ~/snap
sudo rm -rf /snap /var/snap /var/lib/snapd /var/cache/snapd /usr/lib/snapd
sudo rm -rf /root/snap /root/snap/snap-store /usr/share/doc/libsnapd-glib1 /usr/share/doc/gir1.2-snapd-1
 
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
 
#sudo add-apt-repository ppa:xalt7x/chromium-deb-vaapi 
#sudo apt update
#sudo apt-get install chromium-browser


#Remove Unwanted Apps 
sudo apt-get purge gnome-mines gnome-mahjongg remmin* rhythmbo* aisleriot deja-dup gnome-sudoku -y 

#Update System
sudo apt update -y && sudo apt upgrade -y 

#Remove System Cache and Updates 
sudo apt autoremove -y 