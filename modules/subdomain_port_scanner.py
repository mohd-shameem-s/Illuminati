import os
import subprocess
import shutil
import sys
import asyncio
import aiohttp
import json

# ANSI Colors
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

# Function to check if a tool is installed
def check_tool_installed(tool):
    return shutil.which(tool) is not None

# Function to install missing tools
def install_tool(tool_name, install_command):
    if not check_tool_installed(tool_name):
        print(f"{YELLOW}[⚠️] {tool_name} is not installed. Installing now...{RESET}")
        os.system(install_command)

# Async function for port scanning (Faster Execution)
async def scan_ports(target):
    """Scan open ports on the target using Nmap (fast scan)."""
    install_tool("nmap", "sudo apt install nmap -y")

    print(f"\n{BLUE}[🔍] Scanning open ports on {target} using Nmap...{RESET}")

    try:
        command = f"nmap -T4 --min-rate=5000 -Pn -p- --open {target}"
        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await process.communicate()
        result = stdout.decode().strip()

        if "Failed to resolve" in result or "0 hosts up" in result:
            print(f"{YELLOW}[⚠️] No open ports found or target is unreachable.{RESET}")
        else:
            print(result)

    except Exception as e:
        print(f"{RED}[❌] Error during port scan: {e}{RESET}")

# Async function to fetch subdomains from crt.sh
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

# Async function to scan subdomains using multiple tools
async def scan_subdomains(target):
    """Find active subdomains using efficient tools."""
    print(f"\n{BLUE}[🔍] Scanning for active subdomains of {target}...{RESET}")

    found_subdomains = set()

    # Using Subfinder (Fastest)
    if check_tool_installed("subfinder"):
        print(f"{CYAN}[🛠] Using Subfinder for subdomain enumeration...{RESET}")
        try:
            command = f"subfinder -silent -d {target}"
            process = await asyncio.create_subprocess_shell(
                command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            result = stdout.decode().strip()
            if result:
                found_subdomains.update(result.splitlines())
        except Exception:
            print(f"{YELLOW}[⚠️] Subfinder encountered an issue.{RESET}")
    else:
        print(f"{YELLOW}[⚠️] Subfinder is not installed. Skipping...{RESET}")

    # Using Amass (Alternative)
    if check_tool_installed("amass"):
        print(f"{CYAN}[🛠] Using Amass for subdomain enumeration...{RESET}")
        try:
            command = f"amass enum -passive -d {target}"
            process = await asyncio.create_subprocess_shell(
                command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            result = stdout.decode().strip()
            if result:
                found_subdomains.update(result.splitlines())
        except Exception:
            print(f"{YELLOW}[⚠️] Amass encountered an issue.{RESET}")
    else:
        print(f"{YELLOW}[⚠️] Amass is not installed. Skipping...{RESET}")

    # Fetch subdomains from Crt.sh
    crtsh_subdomains = await fetch_crtsh(target)
    found_subdomains.update(crtsh_subdomains)

    # Display Results
    if found_subdomains:
        print(f"\n{GREEN}[✔] Found Subdomains:{RESET}")
        for sub in sorted(found_subdomains):
            print(f"  - {sub}")
    else:
        print(f"{YELLOW}[⚠️] No active subdomains found.{RESET}")

# Async function to execute both scans simultaneously
async def main():
    target_domain = input(f"{CYAN}🔹 Enter the target domain (e.g., example.com): {RESET}").strip()

    if not target_domain:
        print(f"{RED}[❌] Invalid input. Please enter a valid domain.{RESET}")
        sys.exit(1)

    # Run scans in parallel
    await asyncio.gather(
        scan_ports(target_domain),
        scan_subdomains(target_domain)
    )

# Execute main function
if __name__ == "__main__":
    asyncio.run(main())
