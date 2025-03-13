import os
import re
import subprocess
import socket
import netifaces

def get_local_ip():
    """ Get the actual local IP address (Not loopback 127.x.x.x) """
    try:
        # Get hostname and resolve local IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        # Check if it accidentally got a loopback address
        if local_ip.startswith("127.") or local_ip == "localhost":
            interfaces = netifaces.interfaces()
            for interface in interfaces:
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        if not addr['addr'].startswith("127."):  # Avoid loopback
                            return addr['addr']
        return local_ip
    except Exception as e:
        print(f"❌ Error getting local IP: {e}")
        return None

def get_network_range(ip):
    """ Convert local IP to subnet (e.g., 192.168.1.1 → 192.168.1.0/24) """
    try:
        parts = ip.split(".")
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"  # Use /24 subnet
    except:
        return None

def scan_network(network_range):
    """ Perform an Nmap scan on the correct subnet """
    print(f"\n[+] Scanning network: {network_range}")
    
    try:
        # Run Nmap command and capture output
        result = subprocess.check_output(["nmap", "-sn", network_range], stderr=subprocess.DEVNULL).decode()
        
        # Extract device IPs
        active_hosts = re.findall(r"Nmap scan report for (\d+\.\d+\.\d+\.\d+)", result)

        if active_hosts:
            print("\n[+] Active Devices Found:")
            for ip in active_hosts:
                print(f"    - {ip}")
        else:
            print("\n❌ No active devices found.")
    except Exception as e:
        print(f"\n❌ Error running Nmap: {e}")

if __name__ == "__main__":
    local_ip = get_local_ip()
    
    if local_ip:
        print(f"[+] Your Device IP Address: {local_ip}")
        network_range = get_network_range(local_ip)
        
        if network_range:
            print(f"[+] Network Range Identified: {network_range}")
            scan_network(network_range)
        else:
            print("❌ Failed to determine network range.")
    else:
        print("❌ Failed to get local IP.")
