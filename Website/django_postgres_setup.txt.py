import subprocess
import platform
import sys
import os
from datetime import datetime

log_dir = "/proj/logs/"
web_dir = "/proj/django"
db_dir = "/proj/database"
log_file = f"{log_dir}/install_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"


def run_with_sudo(command, sudo_password, log_file):
    command_with_sudo = ['sudo', '-S'] + command
    with open(log_file, 'a') as log:
        log.write(f"Running command: {' '.join(command)}\n")
        process = subprocess.Popen(command_with_sudo, stdin=subprocess.PIPE, stdout=log, stderr=log)
        process.communicate(input=(sudo_password + '\n').encode())


def install_package(package, sudo_password, log_file):
    result = subprocess.run(['which', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        run_with_sudo(['sudo', 'yum', 'install', '-y', package], sudo_password, log_file)


def install_packages_ubuntu():
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'install', 'python3-pip', 'python3-dev', 'postgresql', 'libpq-dev'])


def install_packages_centos(sudo_password):
    install_required_packages(sudo_password, log_file)
    subprocess.run(['sudo', 'yum', 'install', 'python3-pip', 'python3-devel', 'postgresql', 'postgresql-devel'])


def install_required_packages(sudo_password, log_file):
    packages = ['git', 'curl', 'wget', 'openjdk-17', 'epel-release']
    for package in packages:
        install_package(package, sudo_password, log_file)


def create_postgres_user_database(sudo_password):
    run_with_sudo(['sudo', '-u', 'postgres', 'createuser', '--interactive', '--username=joelj'], sudo_password,
                  log_file)
    run_with_sudo(['sudo', '-u', 'postgres', 'createdb', 'mysite', '--owner=joelj'], sudo_password, log_file)


def install_django(sudo_password, log_file):
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'django'], check=True)
    print("Django installation completed.")


def configure_django(log_file):
    os.makedirs("/proj/django/myproject", exist_ok=True)
    os.chdir("/proj/django/myproject")

    # Create virtual environment
    subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)

    # Activate virtual environment
    activate_venv_command = 'source venv/bin/activate' if 'posix' in os.name else 'venv\\Scripts\\activate'
    subprocess.run(activate_venv_command, shell=True, check=True)

    # Install Django inside the virtual environment
    install_django(None, log_file)

    # Configure Django project
    subprocess.run([sys.executable, '-m', 'django', 'startproject', 'myproject'])
    print("Django project configured.")


def configure_postgresql():
    os.chdir(db_dir)
    subprocess.run(['sudo', '-u', 'postgres', 'initdb', 'data'])
    subprocess.run(['sudo', '-u', 'postgres', 'pg_ctl', '-D', 'data', '-l', 'logfile', 'start'])


def start_django_server():
    os.chdir(os.path.join(web_dir, 'myproject'))
    subprocess.run(['python3', 'manage.py', 'runserver', '0.0.0.0:8003'])


def check_and_unblock_firewall(sudo_password):
    firewall_status = subprocess.run(['sudo', 'ufw', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if "inactive" not in firewall_status.stdout.decode('utf-8'):
        run_with_sudo(['sudo', 'ufw', 'allow', '8000:8003/tcp'], sudo_password, log_file)
        run_with_sudo(['sudo', 'ufw', 'reload'], sudo_password, log_file)


def ask_sudo_password():
    return getpass.getpass(prompt='Enter your sudo password: ')


def main():
    sudo_password = ask_sudo_password()

    install_required_packages(sudo_password, log_file)
    check_and_unblock_firewall(sudo_password)

    create_postgres_user_database(sudo_password)
    configure_postgresql()
    install_django(sudo_password, log_file)
    configure_django(log_file)
    start_django_server()

    print(f"Script completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Django and PostgreSQL installation completed. Server started at http://localhost:8003/")


if __name__ == "__main__":
    main()
