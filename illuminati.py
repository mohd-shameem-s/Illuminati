#!/usr/bin/python3
import os
import sys
import subprocess

PYTHON = sys.executable

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def display_logo():
    try:
        with open("ascii_logo.txt", "r") as file:
            content = file.read()
        print(f"{GREEN}{content}{RESET}")
    except FileNotFoundError:
        print(f"{RED}[!] ASCII Logo not found. Skipping...{RESET}")

def display_menu():
    print(f"""{BOLD}{CYAN}
📜 MENU - Illuminati Cyber Toolkit 📜{RESET}

{YELLOW} 1.{RESET} Location Finder 📍            - Track IP geolocation
{YELLOW} 2.{RESET} IP Identifier 🌐             - Hostname, ISP & network info
{YELLOW} 3.{RESET} Network Scanner 🖥          - Scan devices on your LAN
{YELLOW} 4.{RESET} Network Mapper 🗺          - Visualize network topology
{YELLOW} 5.{RESET} Link Scanner 🔗            - Check site for threats
{YELLOW} 6.{RESET} Data Capture 📡            - Packet sniffer & analyzer
{YELLOW} 7.{RESET} Traffic Analyzer 📊        - Monitor live network data
{YELLOW} 8.{RESET} Track Mobile Location 📲  - GPS-based phone tracking
{YELLOW} 9.{RESET} Metadata Extractor 🗂      - Reveal hidden file data
{YELLOW}10.{RESET} Subdomain & Port Scanner 🔍 - Enumerate ports/subdomains
{YELLOW}11.{RESET} Password Checker 🔑         - Analyze password strength
{YELLOW}12.{RESET} Exit 🚪                    - Quit Illuminati Toolkit

💀 {BOLD}Use Responsibly - Illuminati Cybersecurity Tool 💀{RESET}
""")

def run_module(command, use_sudo=False):
    try:
        cmd = [PYTHON, command]
        if use_sudo:
            cmd.insert(0, "sudo")
        subprocess.call(cmd)
    except Exception as e:
        print(f"{RED}[!] Error running {command}: {e}{RESET}")

def main():
    while True:
        os.system("clear")
        display_logo()
        display_menu()

        option = input(f"{CYAN}💀 Choose an option [1-12]: {RESET}").strip()

        if option == "1":
            run_module("modules/location_finder.py")
        elif option == "2":
            run_module("modules/ip_identifier.py")
        elif option == "3":
            run_module("modules/scan_network.py")
        elif option == "4":
            run_module("modules/network_map.py")
        elif option == "5":
            run_module("modules/link_scanner.py")
        elif option == "6":
            run_module("modules/data_capture.py", use_sudo=True)
        elif option == "7":
            run_module("modules/network_traffic_analyzer.py", use_sudo=True)
        elif option == "8":
            run_module("modules/mobile_tracker.py")
        elif option == "9":
            run_module("modules/metadata_extractor.py")
        elif option == "10":
            run_module("modules/subdomain_port_scanner.py")
        elif option == "11":
            run_module("modules/password_strength_checker.py")
        elif option == "12":
            print(f"\n{BLUE}💀 Exiting Illuminati... Stay Secure! 💀{RESET}")
            break
        else:
            print(f"\n{RED}❌ Invalid option. Please enter a number between 1 and 12.{RESET}")
            input(f"{BOLD}🔁 Press [ENTER] to try again...{RESET}")
            continue

        print(f"\n{CYAN}" + "-" * 60 + f"{RESET}")
        input(f"{BOLD}💀 Press [ENTER] to return to the main menu...{RESET}")

if __name__ == "__main__":
    main()
