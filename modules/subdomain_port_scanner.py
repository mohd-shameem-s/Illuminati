#!/usr/bin/python3.13

import os
import shutil
import asyncio
import aiohttp
import subprocess
import sys

# ANSI Colors
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

# Check if tool is installed
def check_tool_installed(tool):
    return shutil.which(tool) is not None

# Install missing tool
def install_tool(tool_name, install_command):
    if not check_tool_installed(tool_name):
        print(f"{YELLOW}[⚠] Installing {tool_name}...{RESET}")
        os.system(install_command)

# Async: Run subprocess and return stdout
async def run_command(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    return stdout.decode().strip()

# Port Scan
async def scan_ports(target):
    install_tool("nmap", "sudo apt install nmap -y")
    print(f"\n{BLUE}[🔍] Scanning open ports on {target}...{RESET}")
    cmd = f"nmap -T4 -p- --min-rate=10000 -Pn --open {target}"
    result = await run_command(cmd)
    if "Failed to resolve" in result or not result:
        print(f"{YELLOW}[⚠] Could not scan ports or no open ports found.{RESET}")
    else:
        print(result)

# Subfinder
async def run_subfinder(target):
    if not check_tool_installed("subfinder"):
        print(f"{YELLOW}[⚠] Subfinder not found. Skipping...{RESET}")
        return []
    print(f"{CYAN}[🛠] Subfinder running...{RESET}")
    result = await run_command(f"subfinder -silent -d {target}")
    return result.splitlines() if result else []

# Amass
async def run_amass(target):
    if not check_tool_installed("amass"):
        print(f"{YELLOW}[⚠] Amass not found. Skipping...{RESET}")
        return []
    print(f"{CYAN}[🛠] Amass running...{RESET}")
    result = await run_command(f"amass enum -passive -d {target}")
    return result.splitlines() if result else []

# Crt.sh
async def fetch_crtsh(target):
    url = f"https://crt.sh/?q={target}&output=json"
    subdomains = set()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    json_data = await response.json()
                    for entry in json_data:
                        subdomains.update(entry.get("name_value", "").splitlines())
    except Exception:
        print(f"{YELLOW}[⚠] crt.sh query failed.{RESET}")
    return list(subdomains)

# Main subdomain scan
async def scan_subdomains(target):
    print(f"\n{BLUE}[🔍] Searching subdomains for {target}...{RESET}")
    tasks = await asyncio.gather(
        run_subfinder(target),
        run_amass(target),
        fetch_crtsh(target),
        return_exceptions=True
    )

    combined = set()
    for task in tasks:
        if isinstance(task, list):
            combined.update(task)

    if combined:
        print(f"\n{GREEN}[✔] Subdomains Found:{RESET}")
        for sub in sorted(combined):
            print(f"  - {sub}")
    else:
        print(f"{YELLOW}[⚠] No subdomains found.{RESET}")

# Entry Point
async def main():
    target = input(f"{CYAN}🔹 Enter target domain (e.g. example.com): {RESET}").strip()
    if not target:
        print(f"{RED}[❌] Invalid input.{RESET}")
        sys.exit(1)

    await asyncio.gather(
        scan_ports(target),
        scan_subdomains(target)
    )

if __name__ == "__main__":
    asyncio.run(main())
