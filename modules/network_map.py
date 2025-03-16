import scapy.all as scapy
import socket
import netifaces
import time
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

# Function to get the user's current IP and network range
def get_network_range():
    try:
        iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        ip = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
        subnet_mask = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['netmask']
        
        # Calculate network CIDR
        subnet_bits = sum(bin(int(x)).count('1') for x in subnet_mask.split('.'))
        network_range = f"{ip}/{subnet_bits}"

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
        return
    
    print(f"🌍 Scanning Network: {network_range}")

    # Create ARP request packet
    arp_request = scapy.ARP(pdst=network_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    # Send ARP request and capture responses
    try:
        result = scapy.srp(packet, timeout=3, verbose=False)[0]
    except PermissionError:
        print("\n❌ Permission Denied! Run the script with sudo:")
        print("   sudo python3 network_map.py")
        return
    
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

# Function to generate a network topology map
def generate_network_topology(devices):
    print("\n📡 Generating Network Topology Map...")
    G = nx.Graph()
    central_router = "Router/Gateway"

    G.add_node(central_router)

    for device in devices:
        ip, mac = device["ip"], device["mac"]
        G.add_node(ip, label=mac)
        G.add_edge(central_router, ip)

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G)
    labels = {node: node for node in G.nodes()}
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", edge_color="gray", font_size=10)
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color="black")
    
    plt.title("Network Topology Map")
    plt.show()

# Main Menu
def main():
    while True:
        print("\n📡 Network Scanner & Mapper")
        print("------------------------------------------------------------")
        print("1 Scan Network for Connected Devices")
        print("2 Generate Network Topology Map")
        print("3 Exit")
        print("------------------------------------------------------------")
        choice = input("💀 Choose an option: ")

        if choice == "1":
            devices = scan_network()
            if devices:
                input("\n💀 Press [ENTER] to return to the main menu...")
        elif choice == "2":
            devices = scan_network()
            if devices:
                generate_network_topology(devices)
            input("\n💀 Press [ENTER] to return to the main menu...")
        elif choice == "3":
            print("💀 Exiting...")
            break
        else:
            print("❌ Invalid option! Try again.")

if __name__ == "__main__":
    main()
