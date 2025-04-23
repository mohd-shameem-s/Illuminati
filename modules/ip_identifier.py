import socket
import requests
import json
import re

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

def is_private_ip(ip):
    """Check if an IP belongs to a private network range"""
    private_ip_ranges = [
        (10, 0, 0, 0, 10, 255, 255, 255),      # 10.0.0.0 - 10.255.255.255
        (172, 16, 0, 0, 172, 31, 255, 255),    # 172.16.0.0 - 172.31.255.255
        (192, 168, 0, 0, 192, 168, 255, 255)   # 192.168.0.0 - 192.168.255.255
    ]

    try:
        ip_parts = list(map(int, ip.split('.')))
        if len(ip_parts) != 4:
            return False

        for r in private_ip_ranges:
            if (ip_parts[0] == r[0] and r[1] <= ip_parts[1] <= r[5]):
                return True

        return False
    except ValueError:
        return False


def get_ip_info(ip):
    """Fetch hostname, ISP, and network details for a given IP"""
    info = {}

    # Validate IP format
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        print(f"{RED}❌ Invalid IP Address format!{RESET}")
        return

    # Get hostname
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        hostname = None

    info["IP Address"] = ip
    info["Hostname"] = hostname if hostname else "Unavailable"

    if is_private_ip(ip):
        info["Network Type"] = "Private Network (Local)"
    else:
        # Get ISP and Network info for Public IPs
        try:
            response = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5).json()
            if 'error' not in response:
                info["ISP"] = response.get("org") or "Unavailable"
                info["Location"] = f"{response.get('city')}, {response.get('country')}" if response.get("city") else "Unavailable"
                info["ASN"] = response.get("org").split()[0] if response.get("org") else "Unavailable"
            else:
                info["ISP"] = "Unavailable"
                info["Location"] = "Unavailable"
                info["ASN"] = "Unavailable"
        except requests.RequestException:
            info["ISP"] = "Unavailable"
            info["Location"] = "Unavailable"
            info["ASN"] = "Unavailable"

    # Display results
    print(f"\n{CYAN}{BOLD}🌐 Illuminati - IP Identifier 🔍{RESET}")
    print(f"{YELLOW}{'-'*60}{RESET}")
    for key, value in info.items():
        print(f"{GREEN}✔ {key}:{RESET} {CYAN}{value}{RESET}")
    print(f"{YELLOW}{'-'*60}{RESET}")


if __name__ == "__main__":
    print(f"{MAGENTA}{BOLD}📡 Enter an IP to analyze its identity and network info!{RESET}")
    ip = input(f"{YELLOW}🔹 Enter an IP Address: {RESET}").strip()
    get_ip_info(ip)
