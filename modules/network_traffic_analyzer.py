#!/usr/bin/python3.13

import os
import pyshark
import time
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from threading import Thread

# ANSI Color Codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

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
        protocol = packet.highest_layer
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst
        length = int(packet.length)

        traffic_stats[(src_ip, dst_ip)] += length
        log_traffic_data(src_ip, dst_ip, length)

        print(f"{BOLD}[{protocol}]{RESET} {CYAN}{src_ip}{RESET} → {CYAN}{dst_ip}{RESET} | Size: {YELLOW}{length} bytes{RESET}")

        if length > HIGH_TRAFFIC_THRESHOLD:
            print(f"{RED}🚨 ALERT: High Traffic Detected from {src_ip} ({length} bytes){RESET}")

    except AttributeError:
        pass  # Skip packets without an IP layer

# Function to monitor network traffic
def monitor_network(interface="any"):
    print(f"\n{MAGENTA}{BOLD}[+] Starting Network Traffic Analyzer...{RESET}")
    print(f"{BLUE}[+] Monitoring live traffic on interface: {YELLOW}{interface}{RESET}")
    print(f"{BLUE}[+] Press CTRL+C to stop\n{RESET}")

    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Source IP", "Destination IP", "Packet Size"])

    try:
        capture = pyshark.LiveCapture(interface=interface)
        for packet in capture.sniff_continuously():
            analyze_packet(packet)

    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Stopping network traffic analyzer...{RESET}\n")
        display_summary()

# Function to display network traffic summary
def display_summary():
    print(f"\n{BOLD}{GREEN}[+] Network Traffic Summary:{RESET}")
    for (src, dst), size in traffic_stats.items():
        print(f"{CYAN}{src}{RESET} → {CYAN}{dst}{RESET} | Total Data: {YELLOW}{size} bytes{RESET}")
    
    print(f"\n{GREEN}[+] Analysis complete.{RESET}")
    generate_graph()

    print(f"\n📥 {BOLD}Traffic Log saved at:{RESET} {BLUE}{LOG_FILE}{RESET}")
    print(f"📊 {BOLD}Traffic Graph saved at:{RESET} {BLUE}{GRAPH_FILE}{RESET}")

# Function to generate a traffic graph
def generate_graph():
    print(f"\n{MAGENTA}[+] Generating Traffic Graph...{RESET}")

    connections = list(traffic_stats.keys())
    data_sizes = list(traffic_stats.values())

    plt.figure(figsize=(10, 5))
    plt.barh([f"{src} → {dst}" for src, dst in connections], data_sizes, color='skyblue')
    plt.xlabel("Data Transferred (bytes)")
    plt.ylabel("Connections")
    plt.title("Network Traffic Analysis")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(GRAPH_FILE)
    plt.show()

if __name__ == "__main__":
    monitor_thread = Thread(target=monitor_network, args=("any",))
    monitor_thread.start()
