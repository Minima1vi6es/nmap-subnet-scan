#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime

# Get user input
ip_base = input("Enter the IP base (e.g. 192.168.1.0): ").strip()
subnet = f"{ip_base}/24"

# Timestamp for filenames
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
scan_name = f"scan_{ip_base.replace('.', '-')}_{timestamp}"

# Determine the correct user's home directory, even when using sudo
if os.geteuid() == 0 and 'SUDO_USER' in os.environ:
    actual_user = os.environ['SUDO_USER']
    user_home = os.path.expanduser(f"/home/{actual_user}")
else:
    user_home = os.path.expanduser("~")

# Output directory
output_dir = os.path.join(user_home, "nmap-scans")
os.makedirs(output_dir, exist_ok=True)

# Output paths
xml_output = os.path.join(output_dir, f"{scan_name}.xml")
html_output = os.path.join(output_dir, f"{scan_name}.html")

# Run the nmap scan
print(f"\n[+] Running Nmap scan on {subnet}...")
subprocess.run(["sudo", "nmap", "-A", "-T4", subnet, "-oX", xml_output])

# Convert XML to HTML using xsltproc
print(f"[+] Converting scan result to HTML...")
subprocess.run(["xsltproc", xml_output, "-o", html_output])

# Done
print(f"\n[✓] Scan complete!")
print(f"    XML saved to:  {xml_output}")
print(f"    HTML saved to: {html_output}")
