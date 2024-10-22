import os
import subprocess
import urllib.request
import zipfile

# Define the URL of the zip file on GitHub
url = "https://github.com/njohnjoel/bane/blob/feature/First_Commit/zips/platform-tools.zip"

# Define the target directory where you want to extract the zip
extract_dir = os.path.expanduser("~/adb-fastboot")

# Create the directory if it doesn't exist
os.makedirs(extract_dir, exist_ok=True)

# Download the zip file
zip_filename = os.path.join(extract_dir, "platform-tools.zip")
urllib.request.urlretrieve(url, zip_filename)

# Extract the zip file
with zipfile.ZipFile(zip_filename, "r") as zip_ref:
    zip_ref.extractall(extract_dir)

# Add export command to ~/.profile
profile_path = os.path.expanduser("~/.profile")
with open(profile_path, "a") as profile_file:
    profile_file.write("\nif [ -d \"$HOME/adb-fastboot/platform-tools\" ] ; then\n")
    profile_file.write(" export PATH=\"$HOME/adb-fastboot/platform-tools:$PATH\"\n")
    profile_file.write("fi\n")

# Clone the repository and perform udev rules setup if it doesn't exist
udev_rules_dir = os.path.join(os.getcwd(), "android-udev-rules")
if not os.path.exists(udev_rules_dir):
    subprocess.run(["git", "clone", "https://github.com/M0Rf30/android-udev-rules.git"])
    os.chdir(udev_rules_dir)
    subprocess.run(["sudo", "cp", "-v", "51-android.rules", "/etc/udev/rules.d/51-android.rules"])
    subprocess.run(["sudo", "ln", "-sf", "$PWD/51-android.rules", "/etc/udev/rules.d/51-android.rules"])
    subprocess.run(["sudo", "chmod", "a+r", "/etc/udev/rules.d/51-android.rules"])
    subprocess.run(["sudo", "cp", "android-udev.conf", "/usr/lib/sysusers.d/"])
    subprocess.run(["sudo", "systemd-sysusers"])
    subprocess.run(["sudo", "gpasswd", "-a", "$(whoami)", "adbusers"])
    subprocess.run(["sudo", "udevadm", "control", "--reload-rules"])
    subprocess.run(["sudo", "systemctl", "restart", "systemd-udevd.service"])
    subprocess.run(["adb", "kill-server"])

print("Platform Tools zip downloaded, extracted, PATH updated in ~/.profile, and udev rules configured.")
print("Replug your Android device and verify that USB debugging is enabled in developer options.")
