import requests
import socket
import subprocess
import re
import json

def get_public_ip_info(ip):
    """Fetch geolocation data for a public IP using ipinfo.io"""
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5).json()
        return {
            "IP Address": response.get("ip", "Unknown"),
            "City": response.get("city", "Unknown"),
            "Region": response.get("region", "Unknown"),
            "Country": response.get("country", "Unknown"),
            "Latitude/Longitude": response.get("loc", "Unknown"),
            "ISP": response.get("org", "Unknown"),
            "Google Maps": f"https://www.google.com/maps?q={response.get('loc', 'Unknown')}"
        }
    except requests.RequestException:
        return {"Error": "Unable to fetch public IP details."}

def get_private_ip_info(ip):
    """Fetch details for private IPs using local network methods"""
    try:
        # Get Hostname
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = "Unknown"

        # Get MAC Address from ARP table
        mac_address = "Unknown"
        try:
            arp_output = subprocess.check_output(["arp", "-a"], text=True)
            match = re.search(rf"{ip} .*?(([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})", arp_output)
            if match:
                mac_address = match.group(1)
        except subprocess.CalledProcessError:
            try:
                ip_neigh_output = subprocess.check_output(["ip", "neigh", "show"], text=True)
                match = re.search(rf"{ip} .*?(([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})", ip_neigh_output)
                if match:
                    mac_address = match.group(1)
            except subprocess.CalledProcessError:
                pass

        # Get Vendor Name (if possible)
        vendor = "Unknown"
        if mac_address != "Unknown":
            try:
                vendor_lookup = requests.get(f"https://api.macvendors.com/{mac_address}", timeout=5).text.strip()
                vendor = vendor_lookup if vendor_lookup else "Unknown"
            except requests.RequestException:
                pass

        return {
            "Private IP Address": ip,
            "Hostname": hostname,
            "MAC Address": mac_address,
            "Vendor": vendor
        }
    except Exception:
        return {"Error": "Unable to fetch private IP details."}

def location_finder():
    print("\n🌍 Location Finder - Track IP Geolocation")
    print("------------------------------------------------------------")

    ip = input("🔹 Enter an IP Address: ").strip()

    # Validate IP format
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        print("❌ Invalid IP Address format!")
        return

    first_octet = int(ip.split('.')[0])
    second_octet = int(ip.split('.')[1]) if '.' in ip else 0  # Ensure second octet exists

    # Private IP ranges (Fixed logic)
    private_ip_ranges = [
        (10,),                # 10.0.0.0 - 10.255.255.255
        (172, 16, 31),        # 172.16.0.0 - 172.31.255.255
        (192, 168)            # 192.168.0.0 - 192.168.255.255
    ]

    is_private = any(
        first_octet == r[0] and (
            len(r) == 1 or (len(r) > 1 and second_octet in range(r[1], r[2] + 1))
        ) for r in private_ip_ranges
    )

    # Determine if IP is Private or Public
    info = get_private_ip_info(ip) if is_private else get_public_ip_info(ip)

    print("\n🔍 IP Details:")
    print(json.dumps(info, indent=4))

if __name__ == "__main__":
    location_finder()
