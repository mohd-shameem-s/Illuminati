import socket
import requests
import json

def get_ip_info(ip):
    """Fetch hostname, ISP, and network details for a given IP"""
    info = {}

    # Get hostname
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except:
        hostname = "Unknown"

    info["IP Address"] = ip
    info["Hostname"] = hostname

    # Check if it's a private or public IP
    first_octet = int(ip.split('.')[0])
    private_ip_ranges = [(10,), (172, 16, 31), (192, 168)]

    is_private = any(
        first_octet == r[0] and (len(r) == 1 or int(ip.split('.')[1]) in range(r[1], r[2] + 1))
        for r in private_ip_ranges
    )

    if is_private:
        info["Network Type"] = "Private Network (Local)"
    else:
        # Get ISP and Network info for Public IPs
        try:
            response = requests.get(f"http://ipinfo.io/{ip}/json").json()
            info["ISP"] = response.get("org", "Unknown")
            info["Location"] = f"{response.get('city', 'Unknown')}, {response.get('country', 'Unknown')}"
            info["ASN"] = response.get("asn", "Unknown")
        except:
            info["ISP"] = "Unknown"
            info["Location"] = "Unknown"
            info["ASN"] = "Unknown"

    print("\n🌐 IP Identifier - Network & ISP Info")
    print("------------------------------------------------------------")
    print(json.dumps(info, indent=4))

if __name__ == "__main__":
    ip = input("🔹 Enter an IP Address: ").strip()
    get_ip_info(ip)
