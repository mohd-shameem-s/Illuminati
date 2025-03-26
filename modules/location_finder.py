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


def is_private_ip(ip):
    """Check if the IP belongs to a private IP range"""
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


def location_finder():
    print("\n🌍 Location Finder - Track IP Geolocation")
    print("------------------------------------------------------------")

    ip = input("🔹 Enter an IP Address: ").strip()

    # Validate IP format
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        print("❌ Invalid IP Address format!")
        return

    # Determine if IP is Private or Public
    info = get_private_ip_info(ip) if is_private_ip(ip) else get_public_ip_info(ip)

    print("\n🔍 IP Details:")
    print(json.dumps(info, indent=4))

if __name__ == "__main__":
    location_finder()
