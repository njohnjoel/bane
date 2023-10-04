import os
import subprocess

# Function to install packages and track un-installable ones
def install_package(package_name):
    try:
        subprocess.run(['sudo', 'apt', 'install', '-y', package_name], check=True)
        print(f"Installed {package_name}")
    except subprocess.CalledProcessError:
        print(f"Unable to install {package_name}")
        uninstallable_packages.append(package_name)

# Function to check Brother printer driver version
def check_printer_version(desired_version):
    installed_version = ""
    try:
        completed_process = subprocess.run(['dpkg-query', '-W', '-f=${Version}', 'brprinter*'], capture_output=True, text=True, check=True)
        installed_version = completed_process.stdout.strip()
    except subprocess.CalledProcessError:
        pass

    if installed_version == desired_version:
        print(f"Identical printer driver version ({installed_version}) already installed.")
        return True
    else:
        return False

# Initialize a list to track un-installable packages
uninstallable_packages = []

# Update and upgrade system
subprocess.run(['sudo', 'apt', 'update', '-y'], check=True)
subprocess.run(['sudo', 'apt', 'upgrade', '-y'], check=True)

# Install necessary packages
install_package("cups")
install_package("software-properties-common")
install_package("gnome-disk-utility")
install_package("curl")
install_package("wget")
install_package("git")
install_package("snapd")

# Install Google Chrome Browser
subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'], check=True)
subprocess.run(['sudo', 'dpkg', '-i', 'google-chrome-stable_current_amd64.deb'], check=True)
subprocess.run(['sudo', 'apt-get', 'install', '-f', '-y'], check=True)

# Install Brave Browser
subprocess.run(['sudo', 'curl', '-fsSLo', '/usr/share/keyrings/brave-browser-archive-keyring.gpg', 'https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg'], check=True)
with open('/tmp/brave-browser-release.list', 'w') as sources_list_file:
    sources_list_file.write("deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main\n")
subprocess.run(['sudo', 'mv', '/tmp/brave-browser-release.list', '/etc/apt/sources.list.d/brave-browser-release.list'], check=True)

# Install Brother Printer Driver (if older version or not installed)
if check_printer_version("2.2.3"):
    subprocess.run(['cd', '~/Downloads'], check=True)
    # Use DEBIAN_FRONTEND to automatically answer "yes" to prompts
    os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
    subprocess.run(['gunzip', '-f', 'linux-brprinter-installer-*.gz'], check=True)
    try:
        subprocess.run(['sudo', 'dpkg', '-i', 'dcpl2520dlpr-3.2.0-1.i386.deb', 'dcpl2520dcupswrapper-3.2.0-1.i386.deb', 'brscan4-0.4.11-1.amd64.deb', 'brscan-skey-0.3.2-0.amd64.deb'], check=True)
        print("Brother printer driver installed.")
    except subprocess.CalledProcessError:
        print("Failed to install the Brother printer driver.")
    # Reset DEBIAN_FRONTEND to its default value
    del os.environ['DEBIAN_FRONTEND']

# Start and enable CUPS service for the printer
subprocess.run(['sudo', 'systemctl', 'start', 'cups'], check=True)
subprocess.run(['sudo', 'systemctl', 'enable', 'cups'], check=True)
subprocess.run(['sudo', 'lpadmin', '-p', 'DCPL2520D', '-E', '-v', 'usb://dev/usb/lp0', '-P', '/usr/share/ppd/brother/brother-DCPL2520D-cups-en.ppd'], check=True)

# Install IntelliJ IDEA Community via Snap
subprocess.run(['sudo', 'snap', 'install', 'intellij-idea-community', '--classic', '--edge'], check=True)

# Autoremove unnecessary packages
subprocess.run(['sudo', 'apt', 'autoremove', '-y'], check=True)

# Display details of un-installable packages
if uninstallable_packages:
    print("The following packages were unable to be installed:")
    for package in uninstallable_packages:
        print(package)
else:
    print("All packages installed successfully.")

# End of script
print("Setup completed.")
