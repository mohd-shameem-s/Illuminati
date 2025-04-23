#!/usr/bin/python3
import os
import sys

PYTHON = sys.executable  # Automatically detects active Python interpreter

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Function to display the ASCII logo
def display_logo():
    try:
        with open("ascii_logo.txt", "r") as file:
            content = file.read()
        print(f"{GREEN}{content}{RESET}")
    except FileNotFoundError:
        print(f"{RED}[!] ASCII Logo not found. Skipping...{RESET}")

# Function to display the menu with usage instructions
def display_menu():
    print(f"""{BOLD}{CYAN}
📜 MENU - Illuminati Cyber Toolkit 📜{RESET}

{YELLOW}1.{RESET} Location Finder 📍         - Track IP geolocation details
{YELLOW}2.{RESET} IP Identifier 🌐            - Get Hostname, ISP, and Network info
{YELLOW}3.{RESET} Network Scanner 🖥         - Scan connected devices on your network
{YELLOW}4.{RESET} Network Mapper 🗺         - Generate network topology map
{YELLOW}5.{RESET} Link Scanner 🔗           - Scan a website for vulnerabilities
{YELLOW}6.{RESET} Data Capture 📡           - Capture & analyze real-time packets
{YELLOW}7.{RESET} Traffic Analyzer 📊       - Live traffic monitor + alert system
{YELLOW}8.{RESET} Track Mobile Location 📲 - Track real-time mobile GPS data
{YELLOW}9.{RESET} Metadata Extractor 🗂     - Extract hidden metadata from files
{YELLOW}10.{RESET} Subdomain & Port Scanner 🔍 - Discover open ports/subdomains
{YELLOW}11.{RESET} Password Checker 🔑      - Test your password’s strength
{YELLOW}12.{RESET} Exit 🚪                   - Quit the Illuminati Toolkit

💀 {BOLD}Use Responsibly - Illuminati Cybersecurity Tool 💀{RESET}
""")

def main():
    while True:
        os.system("clear")
        display_logo()
        display_menu()

        option = input(f"{CYAN}💀 Choose an option: {RESET}")

        if option == "1":
            os.system(f"{PYTHON} modules/location_finder.py")
        elif option == "2":
            os.system(f"{PYTHON} modules/ip_identifier.py")
        elif option == "3":
            os.system(f"{PYTHON} modules/scan_network.py")
        elif option == "4":
            os.system(f"{PYTHON} modules/network_map.py")
        elif option == "5":
            os.system(f"{PYTHON} modules/link_scanner.py")
        elif option == "6":
            os.system(f"sudo {PYTHON} modules/data_capture.py")
        elif option == "7":
            os.system(f"sudo {PYTHON} modules/network_traffic_analyzer.py")
        elif option == "8":
            os.system(f"{PYTHON} modules/mobile_tracker.py")
        elif option == "9":
            os.system(f"{PYTHON} modules/metadata_extractor.py")
        elif option == "10":
            os.system(f"{PYTHON} modules/subdomain_port_scanner.py")
        elif option == "11":
            os.system(f"{PYTHON} modules/password_strength_checker.py")
        elif option == "12":
            print(f"\n{BLUE}💀 Exiting Illuminati... Stay Secure 💀{RESET}")
            break
        else:
            print(f"\n{RED}❌ Invalid option. Please try again.{RESET}")

        print(f"\n{CYAN}" + "-" * 60 + f"{RESET}")
        input(f"{BOLD}💀 Press [ENTER] to return to the main menu...{RESET}")

if __name__ == "__main__":
    main()
