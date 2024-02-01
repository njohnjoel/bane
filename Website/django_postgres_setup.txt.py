import subprocess
import platform
import sys
import getpass
import os
from datetime import datetime


def ask_sudo_password():
    sudo_password = getpass.getpass(prompt='Enter your sudo password: ')
    return sudo_password


def run_with_sudo(command, sudo_password, log_file):
    command_with_sudo = ['sudo', '-S'] + command
    with open(log_file, 'a') as log:
        log.write(f"Running command: {' '.join(command)}\n")
        subprocess.run(command_with_sudo, input=(sudo_password + '\n').encode('utf-8'), stdout=log, stderr=log)


def create_directories():
    sudo_password = ask_sudo_password()
    run_with_sudo(['mkdir', '-p', '/proj/'], sudo_password, 'install_django_postgres.log')
    run_with_sudo(['mkdir', '-p', '/proj/logs/'], sudo_password, 'install_django_postgres.log')
    run_with_sudo(['mkdir', '-p', '/proj/django'], sudo_password, 'install_django_postgres.log')
    run_with_sudo(['mkdir', '-p', '/proj/database'], sudo_password, 'install_django_postgres.log')
    run_with_sudo(['mkdir', '-p', '/proj/logs/'], sudo_password, 'install_django_postgres.log')


def install_packages_ubuntu():
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'install', 'python3-pip', 'python3-dev', 'postgresql', 'libpq-dev'])


def install_packages_centos():
    install_required_packages()
    subprocess.run(['sudo', 'yum', 'install', 'python3-pip', 'python3-devel', 'postgresql', 'postgresql-devel'])


def install_required_packages():
    sudo_password = ask_sudo_password()
    packages = ['git', 'curl', 'wget', 'openjdk-17', 'epel-release']

    for package in packages:
        result = subprocess.run(['which', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            log_file = f'/proj/logs/install_django_postgres_{datetime.now().strftime("%Y%m%d%H%M%S")}.log'
            run_with_sudo(['sudo', 'yum', 'install', '-y', package], sudo_password, log_file)


def create_postgres_user_database():
    sudo_password = ask_sudo_password()
    run_with_sudo(['sudo', '-u', 'postgres', 'createuser', '--interactive', '--username=joelj'], sudo_password,
                  'install_django_postgres.log')
    run_with_sudo(['sudo', '-u', 'postgres', 'createdb', 'mysite', '--owner=joelj'], sudo_password,
                  'install_django_postgres.log')


def install_django():
    subprocess.run(['pip3', 'install', 'django'])


def configure_django():
    os.chdir('/proj/django')
    subprocess.run(['django-admin', 'startproject', 'myproject'])


def configure_postgresql():
    os.chdir('/proj/database')
    subprocess.run(['sudo', '-u', 'postgres', 'initdb', 'data'])
    subprocess.run(['sudo', '-u', 'postgres', 'pg_ctl', '-D', 'data', '-l', 'logfile', 'start'])


def start_django_server():
    os.chdir('/proj/django/myproject')
    subprocess.run(['python3', 'manage.py', 'runserver', '0.0.0.0:8003'])  # Updated to use port 8003


def print_start_time():
    print(f"Script started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def print_end_time():
    print(f"Script completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def check_and_unblock_firewall():
    sudo_password = ask_sudo_password()
    firewall_status = subprocess.run(['sudo', 'ufw', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if "inactive" in firewall_status.stdout.decode('utf-8'):
        print("Firewall is inactive. No action required.")
    else:
        print("Firewall is active. Unblocking ports 8000-8003...")
        run_with_sudo(['sudo', 'ufw', 'allow', '8000:8003/tcp'], sudo_password, 'install_django_postgres.log')
        run_with_sudo(['sudo', 'ufw', 'reload'], sudo_password, 'install_django_postgres.log')
        print("Ports unblocked.")


def main():
    print_start_time()
    create_directories()
    install_required_packages()
    check_and_unblock_firewall()

    if platform.system() == 'Linux':
        if platform.dist()[0] == 'Ubuntu':
            install_packages_ubuntu()
        elif platform.dist()[0] == 'CentOS':
            install_packages_centos()
        else:
            print("Unsupported Linux distribution")
            sys.exit(1)
    else:
        print("Unsupported operating system")
        sys.exit(1)

    create_postgres_user_database()
    install_django()
    configure_django()
    configure_postgresql()
    start_django_server()

    print_end_time()
    print("Django and PostgreSQL installation completed. Server started at http://localhost:8003/")


if __name__ == "__main__":
    main()
