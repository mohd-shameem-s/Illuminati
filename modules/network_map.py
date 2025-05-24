import scapy.all as scapy
import socket
import netifaces
import os
import sys

# ANSI Color Codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Ensure the script runs with sudo
if os.geteuid() != 0:
    print(f"\n{RED}❌ Permission Denied! Run the script with sudo:{RESET}\n")
    print(f"   {YELLOW}sudo python3 {sys.argv[0]}{RESET}\n")
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
        print(f"{RED}❌ Error detecting network: {e}{RESET}")
        return None, None

# Function to scan the network using ARP
def scan_network():
    print(f"\n{MAGENTA}📡 Scanning Network for Connected Devices...{RESET}")
    print(f"{BLUE}" + "-" * 60 + f"{RESET}")

    my_ip, network_range = get_network_range()
    if not my_ip:
        print(f"{RED}❌ Failed to detect network.{RESET}")
        return []

    print(f"{YELLOW}🌍 Scanning Network Range: {RESET}{CYAN}{network_range}{RESET}")

    # Create ARP request packet
    arp_request = scapy.ARP(pdst=network_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    try:
        result = scapy.srp(packet, timeout=3, verbose=False)[0]
    except PermissionError:
        print(f"\n{RED}❌ Permission Denied! Run the script with sudo:{RESET}")
        print(f"   {YELLOW}sudo python3 network_scan.py{RESET}")
        return []

    devices = []
    for sent, received in result:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})

    # Display Results
    print(f"\n{GREEN}💻 Connected Devices:{RESET}")
    print(f"{BLUE}" + "-" * 60 + f"{RESET}")
    print(f"{BOLD}IP Address\t\tMAC Address{RESET}")
    print(f"{BLUE}" + "-" * 60 + f"{RESET}")
    for device in devices:
        print(f"{CYAN}{device['ip']}\t{device['mac']}{RESET}")

    return devices

# Main Menu
def main():
    while True:
        print(f"\n{BOLD}{MAGENTA}📡 Network Scanner{RESET}")
        print(f"{BLUE}" + "-" * 60 + f"{RESET}")
        print(f"{YELLOW}1{RESET} Scan Network for Connected Devices")
        print(f"{YELLOW}2{RESET} Exit")
        print(f"{BLUE}" + "-" * 60 + f"{RESET}")
        choice = input(f"{CYAN}💀 Choose an option: {RESET}")

        if choice == "1":
            devices = scan_network()
            if devices:
                input(f"\n{GREEN}💀 Press [ENTER] to return to the main menu...{RESET}")
        elif choice == "2":
            print(f"{RED}💀 Exiting...{RESET}")
            break
        else:
            print(f"{RED}❌ Invalid option! Try again.{RESET}")

if __name__ == "__main__":
    main()
