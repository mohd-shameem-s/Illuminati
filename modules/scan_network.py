import os
import socket
import netifaces

def get_local_ip():
    """Get the actual local network IP (not 127.x.x.x)."""
    try:
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for link in addrs[netifaces.AF_INET]:
                    ip = link['addr']
                    if not ip.startswith("127."):  # Ignore loopback addresses
                        return ip
    except Exception as e:
        print(f"[-] Error getting local IP: {e}")
        return "Unknown"

# Get the correct local IP
ip = get_local_ip()
if ip == "Unknown":
    print("❌ Unable to determine local IP.")
    exit(1)

# Calculate network range
network_range = ip.rsplit('.', 1)[0] + '.0/24'

print(f"[+] Your Device IP Address: {ip}")
print(f"[+] Network Range Identified: {network_range}")
print("[+] Scanning Network...")

# Run nmap to scan for active devices
os.system(f'nmap -sn {network_range}')
