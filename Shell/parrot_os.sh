#!/bin/bash

# Update and upgrade system
sudo apt update -y && sudo apt upgrade -y

# Initialize a list to track un-installable packages
uninstallable_packages=""

# Function to install packages and track un-installable ones
install_package() {
    package_name="$1"
    # Check if the package is available for installation
    if sudo apt install -y "$package_name"; then
        echo "Installed $package_name"
    else
        echo "Unable to install $package_name"
        uninstallable_packages="$uninstallable_packages $package_name"
    fi
}

# Function to check Brother printer driver version
check_printer_version() {
    installed_version=$(dpkg-query -W -f='${Version}' "brprinter*")
    if [ "$installed_version" == "$1" ]; then
        echo "Identical printer driver version ($installed_version) already installed."
        return 1
    else
        return 0
    fi
}

# Install necessary packages
install_package "cups"
install_package "software-properties-common"
install_package "gnome-disk-utility"
install_package "curl"
install_package "wget"
install_package "git"
install_package "snapd"

# Install Google Chrome Browser
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y

# Install Brave Browser
sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list
sudo apt update -y
install_package "brave-browser"

# Install Brother Printer Driver (if older version or not installed)
if check_printer_version "2.2.3"; then
    cd ~/Downloads
    # Use DEBIAN_FRONTEND to automatically answer "yes" to prompts
    export DEBIAN_FRONTEND=noninteractive
    gunzip -f linux-brprinter-installer-*.gz
    if sudo dpkg -i dcpl2520dlpr-3.2.0-1.i386.deb dcpl2520dcupswrapper-3.2.0-1.i386.deb brscan4-0.4.11-1.amd64.deb brscan-skey-0.3.2-0.amd64.deb; then
        echo "Brother printer driver installed."
    else
        echo "Failed to install the Brother printer driver."
    fi
    # Reset DEBIAN_FRONTEND to its default value
    unset DEBIAN_FRONTEND
fi

# Start and enable CUPS service for the printer
sudo systemctl start cups && sudo systemctl enable cups
sudo lpadmin -p DCPL2520D -E -v usb://dev/usb/lp0 -P /usr/share/ppd/brother/brother-DCPL2520D-cups-en.ppd

# Install IntelliJ IDEA Community via Snap
sudo snap install intellij-idea-community --classic --edge

# Autoremove unnecessary packages
sudo apt autoremove -y

# Display details of un-installable packages
if [ -n "$uninstallable_packages" ]; then
    echo "The following packages were unable to be installed:"
    echo "$uninstallable_packages"
else
    echo "All packages installed successfully."
fi

# End of script
echo "Initial Setup is Complete , Enjoy Parrot Security"