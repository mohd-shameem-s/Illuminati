import requests
import socket
import subprocess
import re
import json

def get_public_ip_info(ip):
    """Fetch geolocation data for a public IP using ipinfo.io"""
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5).json()
        if 'error' in response:
            return {"Error": "Unable to fetch public IP details."}
        
        # Create a dictionary with only available data
        public_info = {
            "IP Address": response.get("ip"),
            "City": response.get("city"),
            "Region": response.get("region"),
            "Country": response.get("country"),
            "Latitude/Longitude": response.get("loc"),
            "ISP": response.get("org"),
            "Google Maps": f"https://www.google.com/maps?q={response.get('loc')}"
        }
        
        # Remove keys with None values
        return {k: v for k, v in public_info.items() if v is not None}
        
    except requests.RequestException:
        return {"Error": "Unable to fetch public IP details."}

def get_private_ip_info(ip):
    """Fetch details for private IPs using local network methods"""
    try:
        # Get Hostname
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = None

        # Get MAC Address from ARP table
        mac_address = None
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
        vendor = None
        if mac_address:
            try:
                vendor_lookup = requests.get(f"https://api.macvendors.com/{mac_address}", timeout=5).text.strip()
                vendor = vendor_lookup if vendor_lookup else None
            except requests.RequestException:
                pass

        private_info = {
            "Private IP Address": ip,
            "Hostname": hostname,
            "MAC Address": mac_address,
            "Vendor": vendor
        }

        # Remove keys with None values
        return {k: v for k, v in private_info.items() if v is not None}
        
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
        (172, 16, 32),        # 172.16.0.0 - 172.31.255.255
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