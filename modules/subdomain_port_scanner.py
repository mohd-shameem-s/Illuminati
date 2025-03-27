import os
import subprocess
import shutil
import sys
import asyncio
import aiohttp
import json
import threading

# ANSI Colors
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

# Function to install missing tools
def install_tool(tool_name, install_command):
    """Install a tool if it's not installed."""
    if not check_tool_installed(tool_name):
        print(f"{YELLOW}[⚠️] {tool_name} is not installed. Installing now...{RESET}")
        os.system(install_command)

# Check if a command-line tool is installed
def check_tool_installed(tool):
    """Check if a command-line tool is installed."""
    return shutil.which(tool) is not None

# Function to scan open ports (Faster)
def scan_ports(target):
    """Scan open ports on the target using Nmap (fast scan)."""
    install_tool("nmap", "sudo apt install nmap -y")

    print(f"\n{BLUE}[🔍] Scanning open ports on {target} using Nmap...{RESET}")

    try:
        # Faster Nmap Scan (-T4 for speed, --min-rate for fast response)
        command = f"nmap -T4 --min-rate=5000 -Pn -p- --open {target}"
        result = subprocess.getoutput(command)

        if "Failed to resolve" in result or "0 hosts up" in result:
            print(f"{YELLOW}[⚠️] No open ports found or target is unreachable.{RESET}")
        else:
            print(result)

    except Exception:
        print(f"{RED}[❌] Error during port scan.{RESET}")

# Function to get subdomains from crt.sh (Async for faster execution)
async def fetch_crtsh(target):
    """Fetch subdomains from Crt.sh asynchronously."""
    url = f"https://crt.sh/?q={target}&output=json"
    subdomains = set()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    json_data = await response.json()
                    for entry in json_data:
                        name_value = entry.get("name_value", "")
                        subdomains.update(name_value.split("\n"))
    except Exception:
        print(f"{YELLOW}[⚠️] Crt.sh encountered an issue.{RESET}")

    return subdomains

# Function to scan subdomains using fastest tools
def scan_subdomains(target):
    """Find active subdomains using efficient tools."""
    print(f"\n{BLUE}[🔍] Scanning for active subdomains of {target}...{RESET}")

    found_subdomains = set()

    # Fastest tool: Subfinder
    if check_tool_installed("subfinder"):
        print(f"{CYAN}[🛠] Using Subfinder for subdomain enumeration...{RESET}")
        try:
            command = f"subfinder -d {target}"
            result = subprocess.getoutput(command)
            if result.strip():
                found_subdomains.update(result.splitlines())
        except Exception:
            print(f"{YELLOW}[⚠️] Subfinder encountered an issue.{RESET}")
    else:
        print(f"{YELLOW}[⚠️] Subfinder is not installed. Skipping...{RESET}")

    # Fast Alternative: Amass
    if check_tool_installed("amass"):
        print(f"{CYAN}[🛠] Using Amass for subdomain enumeration...{RESET}")
        try:
            command = f"amass enum -passive -d {target}"
            result = subprocess.getoutput(command)
            if result.strip():
                found_subdomains.update(result.splitlines())
        except Exception:
            print(f"{YELLOW}[⚠️] Amass encountered an issue.{RESET}")
    else:
        print(f"{YELLOW}[⚠️] Amass is not installed. Skipping...{RESET}")

    # Fetch Crt.sh subdomains asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    crtsh_subdomains = loop.run_until_complete(fetch_crtsh(target))
    found_subdomains.update(crtsh_subdomains)

    # Display Results
    if found_subdomains:
        print(f"\n{GREEN}[✔] Found Subdomains:{RESET}")
        for sub in sorted(found_subdomains):
            print(f"  - {sub}")
    else:
        print(f"{YELLOW}[⚠️] No active subdomains found.{RESET}")

# Main function to run scans in parallel (Faster Execution)
def main():
    target_domain = input(f"{CYAN}🔹 Enter the target domain (e.g., example.com): {RESET}").strip()

    if not target_domain:
        print(f"{RED}[❌] Invalid input. Please enter a valid domain.{RESET}")
        sys.exit(1)

    # Run scans in parallel using threads
    port_scan_thread = threading.Thread(target=scan_ports, args=(target_domain,))
    subdomain_scan_thread = threading.Thread(target=scan_subdomains, args=(target_domain,))

    port_scan_thread.start()
    subdomain_scan_thread.start()

    port_scan_thread.join()
    subdomain_scan_thread.join()

# Execute main function
if __name__ == "__main__":
    main()
