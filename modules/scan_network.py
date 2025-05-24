import os
import socket
import netifaces

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

def get_local_ip():
    """Get the actual local network IP (not 127.x.x.x)."""
    try:
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for link in addrs[netifaces.AF_INET]:
                    ip = link['addr']
                    if not ip.startswith("127."):  # Ignore loopback
                        return ip
    except Exception as e:
        print(f"{RED}[-] Error getting local IP: {e}{RESET}")
        return "Unknown"

# Get the correct local IP
ip = get_local_ip()
if ip == "Unknown":
    print(f"{RED}❌ Unable to determine local IP address.{RESET}")
    exit(1)

# Calculate network range
network_range = ip.rsplit('.', 1)[0] + '.0/24'

# Display Information
print(f"\n{BOLD}{CYAN}📡 Network Scanner Utility{RESET}")
print(f"{GREEN}[+] Your Device IP Address: {YELLOW}{ip}{RESET}")
print(f"{GREEN}[+] Network Range Identified: {YELLOW}{network_range}{RESET}")
print(f"{BLUE}[+] Scanning for Active Hosts...{RESET}\n")

# Run nmap to scan for active devices
os.system(f'nmap -sn {network_range}')
