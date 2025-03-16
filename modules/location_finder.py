import requests
import socket
import subprocess
import re
import json

def get_public_ip_info(ip):
    """Fetch geolocation data for a public IP using ipinfo.io"""
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json").json()
        return {
            "IP Address": response.get("ip", "Unknown"),
            "City": response.get("city", "Unknown"),
            "Region": response.get("region", "Unknown"),
            "Country": response.get("country", "Unknown"),
            "Latitude/Longitude": response.get("loc", "Unknown"),
            "ISP": response.get("org", "Unknown"),
            "Google Maps": f"https://www.google.com/maps?q={response.get('loc', 'Unknown')}"
        }
    except:
        return {"Error": "Unable to fetch public IP details."}

def get_private_ip_info(ip):
    """Fetch details for private IPs using local network methods"""
    try:
        # Get Hostname
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = "Unknown"

        # Get MAC Address from ARP
        arp_output = subprocess.check_output(["arp", "-a"]).decode()
        mac_address = re.search(rf"{ip} .*?(([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})", arp_output)
        mac_address = mac_address.group(1) if mac_address else "Unknown"

        # Get Vendor Name (if possible)
        vendor = "Unknown"
        if mac_address != "Unknown":
            try:
                vendor_lookup = requests.get(f"https://api.macvendors.com/{mac_address}").text
                vendor = vendor_lookup if vendor_lookup else "Unknown"
            except:
                vendor = "Unknown"

        return {
            "Private IP Address": ip,
            "Hostname": hostname,
            "MAC Address": mac_address,
            "Vendor": vendor
        }
    except:
        return {"Error": "Unable to fetch private IP details."}

def location_finder():
    print("\n🌍 Location Finder - Track IP Geolocation")
    print("------------------------------------------------------------")
    
    ip = input("🔹 Enter an IP Address: ").strip()

    # Check if it's a private or public IP
    first_octet = int(ip.split('.')[0])
    private_ip_ranges = [(10,), (172, 16, 31), (192, 168)]

    is_private = any(
        first_octet == r[0] and (len(r) == 1 or int(ip.split('.')[1]) in range(r[1], r[2] + 1))
        for r in private_ip_ranges
    )

    if is_private:
        info = get_private_ip_info(ip)
    else:
        info = get_public_ip_info(ip)

    print("\n🔍 IP Details:")
    print(json.dumps(info, indent=4))

if __name__ == "__main__":
    location_finder()
