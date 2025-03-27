import scapy.all as scapy
import socket
import netifaces
import os
import sys

# Ensure the script runs with sudo
if os.geteuid() != 0:
    print("\n❌ Permission Denied! Run the script with sudo:\n")
    print("   sudo python3 " + sys.argv[0] + "\n")
    sys.exit(1)

# Function to get the user's current IP and network range
def get_network_range():
    try:
        iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        ip_info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
        ip = ip_info['addr']
        subnet_mask = ip_info['netmask']

        # Calculate CIDR notation for the network range
        subnet_bits = sum(bin(int(x)).count('1') for x in subnet_mask.split('.'))
        network_range = f"{ip.rsplit('.', 1)[0]}.0/{subnet_bits}"

        return ip, network_range
    except Exception as e:
        print(f"❌ Error detecting network: {e}")
        return None, None

# Function to scan the network using ARP
def scan_network():
    print("\n📡 Scanning Network for Connected Devices...")
    print("------------------------------------------------------------")

    # Get current IP and network range
    my_ip, network_range = get_network_range()
    if not my_ip:
        print("❌ Failed to detect network.")
        return []

    print(f"🌍 Scanning Network: {network_range}")

    # Create ARP request packet
    arp_request = scapy.ARP(pdst=network_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    try:
        result = scapy.srp(packet, timeout=3, verbose=False)[0]
    except PermissionError:
        print("\n❌ Permission Denied! Run the script with sudo:")
        print("   sudo python3 network_scan.py")
        return []
    
    devices = []
    for sent, received in result:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})

    # Display Results
    print("\n💻 Connected Devices:")
    print("------------------------------------------------------------")
    print("IP Address\t\tMAC Address")
    print("------------------------------------------------------------")
    for device in devices:
        print(f"{device['ip']}\t{device['mac']}")

    return devices

# Main Menu
def main():
    while True:
        print("\n📡 Network Scanner")
        print("------------------------------------------------------------")
        print("1 Scan Network for Connected Devices")
        print("2 Exit")
        print("------------------------------------------------------------")
        choice = input("💀 Choose an option: ")

        if choice == "1":
            devices = scan_network()
            if devices:
                input("\n💀 Press [ENTER] to return to the main menu...")
        elif choice == "2":
            print("💀 Exiting...")
            break
        else:
            print("❌ Invalid option! Try again.")

if __name__ == "__main__":
    main()
