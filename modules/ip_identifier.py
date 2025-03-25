import socket
import requests
import json
import re

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

    # Private IP ranges (Fixed logic)
    private_ip_ranges = [
        (10,),                # 10.0.0.0 - 10.255.255.255
        (172, 16, 32),        # 172.16.0.0 - 172.31.255.255
        (192, 168)            # 192.168.0.0 - 192.168.255.255
    ]

    first_octet = int(ip.split('.')[0])
    second_octet = int(ip.split('.')[1]) if '.' in ip else 0  # Ensure second octet exists

    is_private = any(
        first_octet == r[0] and (
            len(r) == 1 or (len(r) > 1 and second_octet in range(r[1], r[2] + 1))
        ) for r in private_ip_ranges
    )

    if is_private:
        info["Network Type"] = "Private Network (Local)"
    else:
        # Get ISP and Network info for Public IPs
        try:
            response = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5).json()
            if 'error' not in response:
                info["ISP"] = response.get("org")
                info["Location"] = f"{response.get('city')}, {response.get('country')}"
                info["ASN"] = response.get("asn")
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