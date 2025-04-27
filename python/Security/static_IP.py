#!/usr/bin/env python3

import sys
import subprocess

def main():
    if len(sys.argv) != 2:
        print("Usage: sudo python3 set_static_ip.py <STATIC_IP>")
        sys.exit(1)

    static_ip = sys.argv[1]
    gateway_ip = "192.168.1.1"  # You can modify if needed
    netplan_file = "/etc/netplan/01-netcfg.yaml"

    netplan_config = f"""network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
        - {static_ip}/24
      gateway4: {gateway_ip}
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
"""

    try:
        # Write the configuration to the file
        print(f"Writing configuration to {netplan_file}...")
        with open(netplan_file, "w") as f:
            f.write(netplan_config)

        # Apply the changes
        print("Applying netplan changes...")
        subprocess.run(["sudo", "netplan", "apply"], check=True)

        # Verify the IP address
        print("Checking new IP address...")
        subprocess.run(["ip", "addr", "show"], check=True)

        print("\n✅ Static IP successfully configured!")

    except PermissionError:
        print("❌ Permission denied! Please run the script with sudo.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error applying netplan: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()