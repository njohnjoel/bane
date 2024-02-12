import subprocess


def run_command(command):
    subprocess.run(command, shell=True, check=True)


# Update system packages
run_command("sudo dnf update -y")

# Install required packages under /proj/joelj/
install_path = "/proj/joelj/"
packages = ["curl", "git", "wget", "httpd", "java-17-openjdk", "docker-ce", "docker-ce-cli", "containerd.io",
            "postgresql-server", "python3-pip"]
for package in packages:
    run_command(f"sudo dnf install -y {package} --installroot={install_path}")

# Start and enable services
services = ["httpd", "jenkins", "docker", "postgresql"]
for service in services:
    run_command(f"sudo chroot {install_path} systemctl start {service}")
    run_command(f"sudo chroot {install_path} systemctl enable {service}")

# Configure Jenkins to run on port 8091
run_command(f"sudo sed -i 's/JENKINS_PORT=\"8080\"/JENKINS_PORT=\"8091\"/' {install_path}/etc/sysconfig/jenkins")

# Install Django using pip
run_command(f"sudo chroot {install_path} pip3 install django")

print("Installation completed successfully!")
