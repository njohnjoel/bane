import os
import subprocess
import sys
import getpass

# Settings
outdir = "/usr/share"  # where to save files of tools
optdir = "/opt"        # where commonly used tools will go to
user = getpass.getuser()

# Colors
RED = "\033[01;31m"
GREEN = "\033[01;32m"
YELLOW = "\033[01;33m"
BLUE = "\033[01;34m"
BOLD = "\033[01;01m"
RESET = "\033[00m"

# Running as root check
def check_root():
    if os.geteuid() != 0:
        print(f"{RED}[!] This script must be run as root. Quitting...{RESET}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"{BLUE}[*]{RESET} {BOLD}Parrot tools post fresh install{RESET}")

# Update and upgrade system
def update_system():
    print(f"\n\n{GREEN}[+]{RESET} {GREEN}Updating system...{RESET}")
    subprocess.run(["apt-get", "-y", "-qq", "update"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(["apt-get", "-y", "-qq", "dist-upgrade"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

# Check internet access
def check_internet():
    print(f"\n{GREEN}[+]{RESET} Checking {GREEN}Internet access{RESET}")
    for _ in range(10):
        result = subprocess.run(["ping", "-c", "1", "-W", "1", "www.google.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            break
    else:
        print(f"{RED}[!] No Internet access. Manually fix the issue & re-run the script{RESET}", file=sys.stderr)
        if getpass.getuser() == "vagrant":
            print(f"{YELLOW}[i]{RESET} VM Detected. {YELLOW}Try switching network adapter mode{RESET} (NAT/Bridged)")
        print(f"{RED}[!] Quitting...{RESET}", file=sys.stderr)
        sys.exit(1)

# Add Parrot repository
def add_parrot_repository():
    parrot_list_file = "/etc/apt/sources.list.d/parrot.list"
    with open(parrot_list_file, "w") as f:
        f.write("deb https://deb.parrotlinux.org/parrot/ rolling main contrib non-free\n")
        f.write("#deb-src https://deb.parrotlinux.org/parrot/ rolling main contrib non-free\n")
        f.write("deb https://deb.parrotlinux.org/parrot/ rolling-security main contrib non-free\n")
        f.write("#deb-src https://deb.parrotlinux.org/parrot/ rolling-security main contrib non-free\n")

    print(f"\n\n{GREEN}[+]{RESET} Installing {GREEN}Parrot gpg and keyring{RESET}")
    subprocess.run(["wget", "-qO", "-", "http://archive.parrotsec.org/parrot/misc/parrotsec.gpg"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True, input=None)
    subprocess.run(["apt-key", "add", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(["apt-get", "-y", "-qq", "update"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(["apt-get", "-y", "-qq", "install", "apt-parrot", "parrot-archive-keyring", "--no-install-recommends"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

# Clean the system
def clean_system():
    print(f"\n{GREEN}[+]{RESET} {GREEN}Cleaning{RESET} the system")
    for cmd in ["clean", "autoremove"]:
        subprocess.run(["apt-get", "-y", "-qq", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    # Purged packages
    subprocess.run(["apt-get", "-y", "-qq", "purge"] + [pkg for pkg in subprocess.check_output(["dpkg", "-l"]).decode().split('\n')[5:] if not pkg.startswith(('ii', 'hi'))], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    # Update slocate database
    subprocess.run(["updatedb"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

# Install dependencies and tools
def install_tools():
    subprocess.run(["mkdir", "-p", outdir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(["mkdir", "-p", "/usr/share/wordlists/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(["cd", outdir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    deps = [
        "curl", "git", "apt-transport-https", "build-essential", "gdb", "libpcap-dev", "golang", "p7zip-full", "unzip", "zip", "unrar",
        "snap", "ruby-dev", "gzip", "ruby", "python3", "python3-pip", "python3-dev", "libssl-dev", "libffi-dev", "binutils", "patch", "ruby-dev",
        "zlib1g-dev", "liblzma-dev", "gpgv2", "autoconf", "bison", "git-core", "libapr1", "libaprutil1", "libgmp3-dev", "libpcap-dev",
        "libpq-dev", "libreadline6-dev", "libsqlite3-dev", "libssl-dev", "libsvn1", "libtool", "libxml2", "libxml2-dev", "libxslt-dev",
        "libyaml-dev", "locate", "ncurses-dev", "openssl", "postgresql", "postgresql-contrib", "wget", "xsel", "zlib1g", "zlib1g-dev"
    ]
    for dep in deps:
        print(f"\n\n{GREEN}[+]{RESET} Installing {GREEN}{dep}{RESET}")
        subprocess.run(["apt-get", "-y", "-qq", "install", dep], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    tools = [
        "vim", "tmux", "zsh", "nmap", "masscan", "onesixtyone", "htop", "ca-certificates", "network-manager-openvpn",
        "network-manager-pptp", "network-manager-vpnc", "network-manager-openconnect", "gobuster", "network-manager-iodine",
        "hashid", "cewl", "bsdgames", "proxychains", "sshuttle", "apt-file", "apt-show-versions", "sqlmap", "sqlite3",
        "ssldump", "fcrackzip", "john", "hydra", "cewl", "crunch", "hashid", "flasm", "nasm", "wfuzz", "dmitry",
        "nfs-common", "hping3", "ncat", "dnsenum", "binwalk", "smbmap", "gparted", "enum4linux", "wireshark", "joomscan",
        "rubygems", "commix", "nikto", "exploitdb", "wfuzz", "hashcat", "smtp-user-enum", "websploit", "amap", "ssldump",
        "whois", "socat", "nishang", "traceroute", "dnsutils", "dnsrecon", "mysql-server"
    ]
    for tool in tools:
        print(f"\n\n{GREEN}[+]{RESET} Installing {GREEN}{tool}{RESET}")
        subprocess.run(["apt-get", "-y", "-qq", "install", tool], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    gems = ["evil-winrm", "wpscan"]
    for gem in gems:
        print(f"\n\n{GREEN}[+]{RESET} Installing {GREEN}{gem}{RESET}")
        subprocess.run(["gem", "install", gem], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Update package manager cache
    subprocess.run(["apt-file", "update"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Install vulscan script for nmap
    print(f"\n\n{GREEN}[+]{RESET} Installing {GREEN}vulscan script for nmap{RESET} ~ vulnerability scanner add-On")
    if not os.path.exists("/usr/share/nmap/vulnscan"):
        subprocess.run(["git", "clone", "https://github.com/scipag/vulscan", "/usr/share/nmap/scripts/vulscan"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Clone webshells
    print(f"\n\n{GREEN}[+]{RESET} Cloning {GREEN}webshells{RESET}")
    if not os.path.exists("/usr/share/webshells"):
        subprocess.run(["git", "clone", "https://github.com/BlackArch/webshells", "/usr/share/webshells"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Clone reGeorg
    print(f"\n\n{GREEN}[+]{RESET} Installing {GREEN}reGeorg{RESET} ~ pivot via web shells")
    if not os.path.exists("/usr/share/webshells/reGeorg"):
        subprocess.run(["git", "clone", "https://github.com/sensepost/reGeorg.git", "/usr/share/webshells/reGeorg"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    print(f"\n\n{GREEN}[+]{RESET} Cloning a bunch of {GREEN}wordlists{RESET}")
    # Clone seclists
    if not os.path.exists("/usr/share/wordlists/SecLists"):
        subprocess.run(["wget", "-cq", "https://github.com/danielmiessler/SecLists/archive/master.zip", "-O", "/usr/share/wordlists/SecList.zip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["unzip", "-o", "/usr/share/wordlists/SecList.zip", "-d", "/usr/share/wordlists/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["mv", "/usr/share/wordlists/SecLists-master", "/usr/share/wordlists/SecLists"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["rm", "-f", "/usr/share/wordlists/SecList.zip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Clone dirbuster wordlists
    if not os.path.exists("/usr/share/wordlists/dirbuster"):
        subprocess.run(["mkdir", "-p", "/usr/share/wordlists/dirbuster"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["git", "clone", "https://github.com/daviddias/node-dirbuster", "/usr/share/wordlists/dirbuster-git"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["mv", "/usr/share/wordlists/dirbuster-git/lists/*", "/usr/share/wordlists/dirbuster/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["rm", "-rf", "/usr/share/wordlists/dirbuster-git"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Download usernames.txt
    if not os.path.exists("/usr/share/wordlists/usernames.txt"):
        subprocess.run(["wget", "-c", "https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt", "-O", "/usr/share/wordlists/usernames.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["sed", "-ie", "s/\\r//g", "/usr/share/wordlists/usernames.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Clone more dirbuster wordlists
    if not os.path.exists("/usr/share/wordlists/dirbuster/big.txt"):
        subprocess.run(["git", "clone", "https://github.com/digination/dirbuster-ng", "/usr/share/wordlists/dirbuster-git"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["mkdir", "-p", "/usr/share/wordlists/dirbuster"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["mv", "/usr/share/wordlists/dirbuster-git/wordlists/*", "/usr/share/wordlists/dirbuster/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["rm", "-rf", "/usr/share/wordlists/dirbuster-git"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Extract rockyou wordlist
    if not os.path.exists("/usr/share/wordlists/rockyou.txt"):
        subprocess.run(["wget", "-qc", "https://github.com/praetorian-code/Hob0Rules/raw/master/wordlists/rockyou.txt.gz", "-O", "/usr/share/wordlists/rockyou.txt.gz"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["gzip", "-dc", "<", "/usr/share/wordlists/rockyou.txt.gz", ">", "/usr/share/wordlists/rockyou.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["rm", "-rf", "/usr/share/wordlists/rockyou.txt.gz"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Install pwn tools and upgrade pip
    subprocess.run(["apt-get", "update"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(["sudo", "-u", user, "python3", "-m", "pip", "install", "-q", "--upgrade", "pip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(["sudo", "-u", user, "python3", "-m", "pip", "install", "-q", "--upgrade", "git+https://github.com/Gallopsled/pwntools.git@dev"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Install impacket
    print(f"\n\n{GREEN}[+]{RESET} Installing {GREEN}impacket{RESET} ~ tools")
    if not os.path.exists(os.path.join(optdir, "impacket")):
        # Dependency for ldap3
        subprocess.run(["sudo", "-u", user, "pip3", "install", "pyasn1==0.4.6"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["git", "clone", "https://github.com/SecureAuthCorp/impacket", os.path.join(optdir, "impacket")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["sudo", "-u", user, "pip3", "install", "-q", os.path.join(optdir, "impacket")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Install peda
    if not os.path.exists(os.path.join(outdir, "peda")):
        subprocess.run(["git", "clone", "https://github.com/longld/peda.git", os.path.join(outdir, "peda")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        if os.path.exists(os.path.expanduser("~/.gdbinit")):
            with open(os.path.expanduser("~/.gdbinit"), "a") as gdbinit_file:
                gdbinit_file.write('source ' + os.path.join(outdir, 'peda', 'peda.py') + '\n')
        if os.path.exists(os.path.expanduser(f"~{user}/.gdbinit")):
            with open(os.path.expanduser(f"~{user}/.gdbinit"), "a") as gdbinit_file:
                gdbinit_file.write('source ' + os.path.join(outdir, 'peda', 'peda.py') + '\n')

    # Clone p0wny-shell
    print(f"\n\n{GREEN}[+]{RESET} Cloning {GREEN}p0wny-shell{RESET} ~ cool PHP shell")
    if not os.path.exists("/usr/share/webshells/p0wny-shell"):
        subprocess.run(["git", "clone", "https://github.com/flozz/p0wny-shell", "/usr/share/webshells/p0wny-shell"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Clone pspy
    print(f"\n\n{GREEN}[+]{RESET} Cloning {GREEN}pspy{RESET} ~ Monitor Linux processes without root permissions")
    if not os.path.exists(os.path.join(optdir, "pspy")):
        subprocess.run(["mkdir", "-p", os.path.join(optdir, "pspy")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["wget", "-qc", "https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy32", "-O", os.path.join(optdir, "pspy", "pspy32")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["wget", "-qc", "https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy64", "-O", os.path.join(optdir, "pspy", "pspy64")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Clone theHarvester
    print(f"\n\n{GREEN}[+]{RESET} Cloning {GREEN}theHarvester{RESET} ~ E-mails, subdomains, and names Harvester - OSINT")
    if not os.path.exists("/etc/theHarvester"):
        subprocess.run(["git", "clone", "https://github.com/laramies/theHarvester"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["cd", "theHarvester"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["python3", "-m", "pip", "install", "-r", "requirements/base.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["cd", ".."], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["mv", "theHarvester", "/etc/theHarvester"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        with open(os.path.expanduser("~/.bashrc"), "a") as bashrc_file:
            bashrc_file.write('export PATH=$PATH:/etc/theHarvester\n')

    # Install Metasploit-framework
    print(f"\n{YELLOW} [i]{RESET} Installing {GREEN}Metasploit-framework{RESET}")
    subprocess.run(["curl", "https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb", ">", "msfinstall"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(["chmod", "755", "msfinstall"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(["./msfinstall"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Remove some stuff
    rm_pkgs = ["wireshark", "burpsuite", "hydra-gtk", "rdesktop", "nmap"]
    for pkg in rm_pkgs:
        subprocess.run(["apt-get", "-y", "-qq", "purge", pkg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Configure
    print(f"\n\n{GREEN}[+]{RESET} Configure {GREEN}Nginx{RESET}")
    if not os.path.exists("/etc/nginx/sites-available/default"):
        subprocess.run(["mv", "/etc/nginx/sites-available/default", "/etc/nginx/sites-available/default.old"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        with open("/etc/nginx/sites-available/default", "w") as default_nginx:
            default_nginx.write("""server {
    listen 80 default_server;
    server_name _;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
""")
        subprocess.run(["systemctl", "restart", "nginx"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    print(f"\n\n{GREEN}[+]{RESET} Configure {GREEN}Sqlite3{RESET}")
    #if not os.path.exists("/etc/sqlite3/sqlite3.conf"):
    #    subprocess.run(["echo", ".system /bin/sh", "|", "sudo", "-u", "postgres", "sqlite3", "3.16.2-1", "/etc/sqlite3/sqlite3.db"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    print(f"\n\n{GREEN}[+]{RESET} Configure {GREEN}Metasploit-framework{RESET}")
    if not os.path.exists("/usr/local/bin/msfconsole"):
        subprocess.run(["echo", "alias msfconsole='/opt/metasploit-framework/bin/msfconsole'", ">>", os.path.expanduser("~/.zshrc")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["echo", "alias msfconsole='/opt/metasploit-framework/bin/msfconsole'", ">>", os.path.expanduser("~/.bashrc")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["echo", "alias msfconsole='/opt/metasploit-framework/bin/msfconsole'", ">>", os.path.expanduser("~/.bash_aliases")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    print(f"\n\n{GREEN}[+]{RESET} Cleaning {GREEN}up{RESET}")
    subprocess.run(["apt-get", "-y", "-qq", "autoremove"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(["apt-get", "-y", "-qq", "clean"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    print(f"\n{BLUE}[*]{RESET} {BOLD}All Done{RESET} ~ Keep {BOLD}hacking{RESET}\n")

def main():
    check_root()
    check_internet()
    update_system()
    add_parrot_repository()
    clean_system()
    install_tools()

if __name__ == "__main__":
    main()