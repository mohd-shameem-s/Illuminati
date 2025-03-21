#!/usr/bin/python3

import os
import pyshark
import time
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from threading import Thread

# Dictionary to store traffic data
traffic_stats = defaultdict(int)

# High-Traffic Threshold (in bytes)
HIGH_TRAFFIC_THRESHOLD = 500000  # 500 KB

# Get the absolute path of the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# File to log traffic data
LOG_FILE = os.path.join(SCRIPT_DIR, "network_traffic_log.csv")
GRAPH_FILE = os.path.join(SCRIPT_DIR, "network_traffic_graph.png")

# Function to log traffic data to a file
def log_traffic_data(src, dst, size):
    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), src, dst, size])

# Function to analyze packet
def analyze_packet(packet):
    try:
        protocol = packet.highest_layer  # Get protocol (TCP, UDP, etc.)
        src_ip = packet.ip.src  # Source IP
        dst_ip = packet.ip.dst  # Destination IP
        length = int(packet.length)  # Packet size

        traffic_stats[(src_ip, dst_ip)] += length  # Update data transfer count
        log_traffic_data(src_ip, dst_ip, length)  # Log data to file

        print(f"[{protocol}] {src_ip} → {dst_ip} | Size: {length} bytes")

        # High-Traffic Alert
        if length > HIGH_TRAFFIC_THRESHOLD:
            print(f"🚨 ALERT: High Traffic Detected from {src_ip} ({length} bytes) 🚨")

    except AttributeError:
        pass  # Skip packets without an IP layer

# Function to monitor network traffic
def monitor_network(interface="any"):
    print("\n[+] Starting Network Traffic Analyzer...")
    print("[+] Monitoring live traffic on interface:", interface)
    print("[+] Press CTRL+C to stop\n")

    # Initialize log file with headers
    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Source IP", "Destination IP", "Packet Size"])

    try:
        capture = pyshark.LiveCapture(interface=interface)
        for packet in capture.sniff_continuously():
            analyze_packet(packet)

    except KeyboardInterrupt:
        print("\n[!] Stopping network traffic analyzer...\n")
        display_summary()
        
# Function to display network traffic summary
def display_summary():
    print("\n[+] Network Traffic Summary:")
    for (src, dst), size in traffic_stats.items():
        print(f"{src} → {dst} | Total Data: {size} bytes")
    print("[+] Analysis complete.\n")
    generate_graph()  # Generate the traffic graph

    # Display file paths
    print(f"\n📥 Traffic Log saved at: {LOG_FILE}")
    print(f"📊 Traffic Graph saved at: {GRAPH_FILE}")

# Function to generate a live traffic graph
def generate_graph():
    print("[+] Generating Traffic Graph...")

    # Convert traffic_stats into a format for plotting
    connections = list(traffic_stats.keys())
    data_sizes = list(traffic_stats.values())

    plt.figure(figsize=(10, 5))
    plt.barh([f"{src} → {dst}" for src, dst in connections], data_sizes, color='skyblue')
    plt.xlabel("Data Transferred (bytes)")
    plt.ylabel("Connections")
    plt.title("Network Traffic Analysis")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.savefig(GRAPH_FILE)  # Save the graph
    plt.show()

if __name__ == "__main__":
    # Run network monitoring in a separate thread
    monitor_thread = Thread(target=monitor_network, args=("any",))
    monitor_thread.start()
