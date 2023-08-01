#!/usr/bin/env python3

import subprocess

# Check if package is installed
def is_installed(package):
    result = subprocess.run(['snap', 'list', package], capture_output=True, text=True)
    return result.returncode == 0

# Uninstall package if it's installed
def uninstall(package):
    if is_installed(package):
        subprocess.run(['sudo', 'snap', 'remove', package], check=True)

# Uninstall snapd if it's installed
if is_installed('snapd'):
    uninstall('snapd')

# Rest of the script...
# Remove Unwanted Apps
unwanted_apps = ['gnome-mines', 'gnome-mahjongg', 'remmin*', 'rhythmbo*', 'aisleriot', 'deja-dup', 'gnome-sudoku']
subprocess.run(['sudo', 'apt-get', 'purge'] + unwanted_apps + ['-y'], check=True)

# Update System
subprocess.run(['sudo', 'apt', 'update', '-y'], check=True)
subprocess.run(['sudo', 'apt', 'upgrade', '-y'], check=True)

# Remove System Cache and Updates
subprocess.run(['sudo', 'apt', 'autoremove', '-y'], check=True)

# Disable TouchPad
xinput_output = subprocess.run(['xinput'], capture_output=True, text=True).stdout
mouse_id = None
for line in xinput_output.splitlines():
    if 'PS/2 Generic Mouse' in line:
        mouse_id = line.split('=')[1].strip()
        break
if mouse_id:
    subprocess.run(['xinput', 'disable', mouse_id], check=True)

#################################################################
# Install System Apps
#################################################################

# Install specified packages
packages_to_install = ['ssh', 'net-tools', 'git', 'vim', 'curl', 'wget']
for package in packages_to_install:
    subprocess.run(['sudo', 'apt', 'install', package, '-y'], check=True)

#################################################################
# Install Sublime
#################################################################

subprocess.run(['wget', '-qO', '-', 'https://download.sublimetext.com/sublimehq-pub.gpg'], check=True)
sublime_repo_entry = "deb https://download.sublimetext.com/ apt/stable/"
subprocess.run(['echo', sublime_repo_entry, '|', 'sudo', 'tee', '/etc/apt/sources.list.d/sublime-text.list'], shell=True, check=True)
subprocess.run(['sudo', 'apt', 'update', '-y'], check=True)
subprocess.run(['sudo', 'apt', 'install', 'sublime-text', '-y'], check=True)

# Remove System Cache and Updates
subprocess.run(['sudo', 'apt', 'autoremove', '-y'], check=True)
