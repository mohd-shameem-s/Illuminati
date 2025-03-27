import os
import subprocess
import shutil
import re
import sys

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

# Ensure Sublist3r is installed
try:
    import sublist3r
    SUBLIST3R_AVAILABLE = True
except ImportError:
    SUBLIST3R_AVAILABLE = False
    install_tool("sublist3r", "pip install git+https://github.com/aboul3la/Sublist3r.git@master")
    try:
        import sublist3r
        SUBLIST3R_AVAILABLE = True
    except ImportError:
        print("\033[91m[❌] Failed to install Sublist3r. Please install it manually.\033[0m")
        sys.exit(1)

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
    """Find active subdomains using Sublist3r or fallback to Amass."""

    if SUBLIST3R_AVAILABLE:
        print(f"\n\033[94m[🔍] Scanning for active subdomains of {target} using Sublist3r...\033[0m\n")

        try:
            subdomains = sublist3r.main(
                domain=target,
                threads=40,
                savefile=None,
                ports=None,
                silent=True,
                verbose=False,
                enable_bruteforce=False,
                engines=None
            )

            if subdomains:
                print("\n\033[92m[✔] Found Subdomains:\033[0m")
                for sub in subdomains:
                    print(f"  - {sub}")
            else:
                print("\033[93m[⚠️] No active subdomains found.\033[0m")

        except (IndexError, Exception):
            print("\033[93m[⚠️] Sublist3r encountered an issue. Trying Amass instead...\033[0m")
            use_amass(target)

    else:
        print("\n\033[93m[⚠️] Sublist3r is not installed. Using Amass instead...\033[0m\n")
        use_amass(target)

# Function to use Amass if Sublist3r fails
def use_amass(target):
    """Use Amass to find subdomains if Sublist3r fails."""
    install_tool("amass", "sudo apt install amass -y")

    print(f"\n\033[94m[🔍] Scanning for active subdomains of {target} using Amass...\033[0m\n")
    
    try:
        command = f"amass enum -d {target}"
        result = subprocess.getoutput(command)

        if not result.strip():
            print("\033[93m[⚠️] No active subdomains found.\033[0m")
        else:
            print(result)

    except Exception:
        print("\033[93m[⚠️] No active subdomains found.\033[0m")

# Main script execution
if __name__ == "__main__":
    target_domain = input("\033[96m🔹 Enter the target domain (e.g., example.com): \033[0m").strip()

    if not target_domain:
        print("\033[91m[❌] Invalid input. Please enter a valid domain.\033[0m")
        sys.exit(1)

    scan_ports(target_domain)
    scan_subdomains(target_domain)
