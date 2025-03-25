import socket
import requests
import json
import re

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
            if (ip_parts[0] == r[0] and ip_parts[1] >= r[1] and ip_parts[1] <= r[5]):
                return True

        return False
    except ValueError:
        return False


def get_ip_info(ip):
    """Fetch hostname, ISP, and network details for a given IP"""
    info = {}

    # Validate IP format
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        print("❌ Invalid IP Address format!")
        return

    # Get hostname
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        hostname = None

    info["IP Address"] = ip
    info["Hostname"] = hostname

    if is_private_ip(ip):
        info["Network Type"] = "Private Network (Local)"
    else:
        # Get ISP and Network info for Public IPs
        try:
            response = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5).json()
            if 'error' not in response:
                info["ISP"] = response.get("org")
                info["Location"] = f"{response.get('city')}, {response.get('country')}"
                info["ASN"] = response.get("org").split()[0] if response.get("org") else None
            else:
                info["ISP"] = None
                info["Location"] = None
                info["ASN"] = None
        except requests.RequestException:
            info["ISP"] = None
            info["Location"] = None
            info["ASN"] = None

    # Remove keys with None values
    info = {k: v for k, v in info.items() if v is not None}

    print("\n🌐 IP Identifier - Network & ISP Info")
    print("------------------------------------------------------------")
    print(json.dumps(info, indent=4))

if __name__ == "__main__":
    ip = input("🔹 Enter an IP Address: ").strip()
    get_ip_info(ip)
