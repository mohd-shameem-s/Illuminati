import os
import socket
import subprocess
import json
from scapy.all import ARP, Ether, srp

def get_local_ip():
    """Retrieve the local device's IP address."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return "Unknown"

def get_network_range():
    """Determine the network range based on the local IP address."""
    local_ip = get_local_ip()
    if local_ip == "Unknown":
        return "Unknown"

    ip_parts = local_ip.split(".")
    network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    return network_range

def scan_network():
    """Perform an ARP scan to discover devices on the network."""
    network_range = get_network_range()

    if network_range == "Unknown":
        print("❌ Unable to determine network range.")
        return

    print(f"\n🌍 Scanning Network: {network_range}")
    print("------------------------------------------------------------")

    # Creating ARP request
    arp_request = ARP(pdst=network_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC Address
    packet = ether / arp_request

    # Sending ARP request
    result = srp(packet, timeout=3, verbose=False)[0]

    devices = []
    for sent, received in result:
        devices.append({"IP Address": received.psrc, "MAC Address": received.hwsrc})

    # Display results
    if devices:
        print("\n🔍 Detected Devices on the Network:")
        for device in devices:
            print(f"📍 IP: {device['IP Address']} | 🔗 MAC: {device['MAC Address']}")
        
        # Save to JSON
        with open("network_scan_results.json", "w") as file:
            json.dump(devices, file, indent=4)

        print("\n✅ Scan complete. Results saved to `network_scan_results.json`")
    else:
        print("❌ No devices found on the network.")

def generate_network_map():
    """Use Nmap to generate a network topology map."""
    network_range = get_network_range()

    if network_range == "Unknown":
        print("❌ Unable to determine network range.")
        return

    print(f"\n🗺 Generating Network Topology for {network_range}")
    print("------------------------------------------------------------")

    try:
        # Run Nmap with OS detection and host discovery
        result = subprocess.check_output(["nmap", "-sn", network_range]).decode()

        # Extract detected hosts
        hosts = []
        for line in result.split("\n"):
            if "Nmap scan report for" in line:
                ip = line.split(" ")[-1]
                hosts.append(ip)

        if hosts:
            print("\n📍 Mapped Devices:")
            for host in hosts:
                print(f"🔹 {host}")

            # Save results
            with open("network_map.json", "w") as file:
                json.dump({"Mapped Devices": hosts}, file, indent=4)

            print("\n✅ Network Map Generated. Results saved to `network_map.json`")
        else:
            print("❌ No devices detected in the network.")
    except Exception as e:
        print(f"❌ Error running Nmap: {str(e)}")

def main():
    print("\n📡 Network Scanner & Mapper")
    print("------------------------------------------------------------")
    print("1️⃣ Scan Network for Connected Devices")
    print("2️⃣ Generate Network Topology Map")
    print("3️⃣ Exit")
    print("------------------------------------------------------------")

    choice = input("💀 Choose an option: ").strip()

    if choice == "1":
        scan_network()
    elif choice == "2":
        generate_network_map()
    elif choice == "3":
        print("🚪 Exiting...")
    else:
        print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
