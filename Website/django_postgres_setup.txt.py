import subprocess
import platform
import sys
import os


def install_packages_ubuntu():
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'install', 'python3-pip', 'python3-dev', 'postgresql', 'libpq-dev'])


def install_packages_centos():
    subprocess.run(['sudo', 'yum', 'install', 'epel-release'])
    subprocess.run(['sudo', 'yum', 'install', 'python3-pip', 'python3-devel', 'postgresql', 'postgresql-devel'])


def create_postgres_user_database():
    subprocess.run(['sudo', '-u', 'postgres', 'createuser', '--interactive', '--username=joelj'])
    subprocess.run(['sudo', '-u', 'postgres', 'createdb', 'mysite', '--owner=joelj'])


def install_django():
    subprocess.run(['pip3', 'install', 'django'])


def start_django_server():
    os.chdir('your_project_directory')  # Replace 'your_project_directory' with the path to your Django project
    subprocess.run(['python3', 'manage.py', 'runserver'])


def main():
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
    start_django_server()

    print("Django and PostgreSQL installation completed. Server started at http://localhost:8000/")


if __name__ == "__main__":
    main()
