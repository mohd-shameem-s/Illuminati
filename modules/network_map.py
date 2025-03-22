import scapy.all as scapy
import socket
import netifaces
import os
import sys
import time
import matplotlib.pyplot as plt
import networkx as nx

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
        print("   sudo python3 network_map.py")
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

# Function to generate a stylish network topology map
def generate_network_topology(devices):
    print("\n📡 Generating Network Topology Map...")
    G = nx.Graph()
    central_router = "🌐 Router/Gateway"

    G.add_node(central_router, type="router")

    for device in devices:
        ip, mac = device["ip"], device["mac"]
        G.add_node(ip, type="device", mac=mac)
        G.add_edge(central_router, ip)

    # Set up plot
    plt.figure(figsize=(12, 8))
    pos = nx.kamada_kawai_layout(G)  # Better layout for visualization

    # Define colors and sizes
    node_colors = ["red" if node == central_router else "green" for node in G.nodes()]
    node_sizes = [2000 if node == central_router else 1200 for node in G.nodes()]

    # Draw the network graph
    nx.draw(
        G, pos, with_labels=True, 
        node_size=node_sizes, node_color=node_colors, 
        edge_color="blue", font_size=10, font_color="white", 
        font_weight="bold", linewidths=2, edgecolors="black"
    )

    # Label nodes with MAC addresses
    labels = {node: node if node == central_router else f"{node}\n{G.nodes[node]['mac']}" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color="yellow")

    plt.title("🌍 Network Topology Map", fontsize=14, fontweight="bold")
    plt.savefig("network_topology.png")  # Save the graph as an image
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
                print("\n✅ Network topology saved as 'network_topology.png'")
            input("\n💀 Press [ENTER] to return to the main menu...")
        elif choice == "3":
            print("💀 Exiting...")
            break
        else:
            print("❌ Invalid option! Try again.")

if __name__ == "__main__":
    main()
