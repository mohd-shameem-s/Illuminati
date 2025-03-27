import os
import subprocess
import shutil
import sys
import requests

# Function to install missing tools
def install_tool(tool_name, install_command):
    """Install a tool if it's not installed."""
    if not check_tool_installed(tool_name):
        print(f"\033[93m[⚠️] {tool_name} is not installed. Installing it now...\033[0m")
        os.system(install_command)

# Check if a command-line tool is installed
def check_tool_installed(tool):
    """Check if a command-line tool is installed."""
    return shutil.which(tool) is not None

# Function to scan open ports
def scan_ports(target):
    """Scan open ports on the target domain/IP using Nmap."""
    install_tool("nmap", "sudo apt install nmap -y")

    print(f"\n\033[94m[🔍] Scanning open ports on {target} using Nmap...\033[0m\n")

    try:
        command = f"nmap -Pn -p- --open {target}"
        result = subprocess.getoutput(command)

        if "Failed to resolve" in result or "0 hosts up" in result:
            print("\033[93m[⚠️] No open ports found or target is unreachable.\033[0m")
        else:
            print(result)

    except Exception:
        print("\033[91m[❌] Error during port scan.\033[0m")

# Function to scan subdomains
def scan_subdomains(target):
    """Find active subdomains using multiple alternative methods."""
    print(f"\n\033[94m[🔍] Scanning for active subdomains of {target}...\033[0m\n")

    found_subdomains = set()

    # Method 1: Amass
    if check_tool_installed("amass"):
        print("\033[94m[🛠] Using Amass for subdomain enumeration...\033[0m")
        try:
            command = f"amass enum -d {target}"
            result = subprocess.getoutput(command)
            if result.strip():
                found_subdomains.update(result.splitlines())
        except Exception:
            print("\033[93m[⚠️] Amass encountered an issue.\033[0m")
    else:
        print("\033[93m[⚠️] Amass is not installed. Skipping...\033[0m")

    # Method 2: Assetfinder
    if check_tool_installed("assetfinder"):
        print("\033[94m[🛠] Using Assetfinder for subdomain enumeration...\033[0m")
        try:
            command = f"assetfinder --subs-only {target}"
            result = subprocess.getoutput(command)
            if result.strip():
                found_subdomains.update(result.splitlines())
        except Exception:
            print("\033[93m[⚠️] Assetfinder encountered an issue.\033[0m")
    else:
        print("\033[93m[⚠️] Assetfinder is not installed. Skipping...\033[0m")

    # Method 3: Crt.sh (Certificate Transparency logs)
    print("\033[94m[🛠] Using Crt.sh for subdomain enumeration...\033[0m")
    try:
        url = f"https://crt.sh/?q={target}&output=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            json_data = response.json()
            for entry in json_data:
                name_value = entry.get("name_value", "")
                subdomains = name_value.split("\n")
                found_subdomains.update(subdomains)
        else:
            print("\033[93m[⚠️] Crt.sh request failed.\033[0m")
    except Exception:
        print("\033[93m[⚠️] Crt.sh encountered an issue.\033[0m")

    # Display Results
    if found_subdomains:
        print("\n\033[92m[✔] Found Subdomains:\033[0m")
        for sub in sorted(found_subdomains):
            print(f"  - {sub}")
    else:
        print("\033[93m[⚠️] No active subdomains found.\033[0m")

# Main script execution
if __name__ == "__main__":
    target_domain = input("\033[96m🔹 Enter the target domain (e.g., example.com): \033[0m").strip()

    if not target_domain:
        print("\033[91m[❌] Invalid input. Please enter a valid domain.\033[0m")
        sys.exit(1)

    scan_ports(target_domain)
    scan_subdomains(target_domain)
