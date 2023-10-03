import subprocess

# Update and upgrade packages
subprocess.run(['sudo', 'apt', 'update', '-y'])
subprocess.run(['sudo', 'apt', 'upgrade', '-y'])

# Install required packages
subprocess.run(['sudo', 'apt', 'install', 'cups', 'software-properties-common', 'gnome-disk-utility', 'curl', 'wget', 'git', 'photorec', 'ddrescue-gui', 'snapd', '-y'])
subprocess.run(['sudo', 'apt', 'install', 'snap-store', '-y'])

# Install Google Chrome Browser
subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'])
subprocess.run(['sudo', 'dpkg', '-i', 'google-chrome-stable_current_amd64.deb'])
subprocess.run(['sudo', 'apt-get', 'install', '-f', '-y'])

# Install Brave Browser
subprocess.run(['sudo', 'curl', '-fsSLo', '/usr/share/keyrings/brave-browser-archive-keyring.gpg', 'https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg'])
subprocess.run(['echo', 'deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main', '|', 'sudo', 'tee', '/etc/apt/sources.list.d/brave-browser-release.list'])
subprocess.run(['sudo', 'apt', 'update'])
subprocess.run(['sudo', 'apt', 'install', 'brave-browser', '-y'])

# Installing Brother Printer Driver
subprocess.run(['cd', '~/Downloads'])
subprocess.run(['wget', 'https://download.brother.com/welcome/dlf006893/linux-brprinter-installer-2.2.3-1.gz'])
subprocess.run(['gunzip', 'linux-brprinter-installer-*.gz'])
subprocess.run(['sudo', 'bash', 'linux-brprinter-installer-2.2.3-1', 'DCP-L2520D'])

# Start and enable CUPS service
subprocess.run(['sudo', 'systemctl', 'start', 'cups'])
subprocess.run(['sudo', 'systemctl', 'enable', 'cups'])

# Configure Brother Printer
subprocess.run(['sudo', 'lpadmin', '-p', 'DCPL2520D', '-E', '-v', 'usb://dev/usb/lp0', '-P', '/usr/share/ppd/brother/brother-DCPL2520D-cups-en.ppd'])

# Install IntelliJ IDEA Community Edition via Snap
subprocess.run(['sudo', 'snap', 'install', 'intellij-idea-community', '--classic', '--edge'])

# Clean up unused packages
subprocess.run(['sudo', 'apt', 'autoremove', '-y'])
