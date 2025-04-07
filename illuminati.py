#!/usr/bin/python3.13
import os
import sys

# Function to display the ASCII logo
def display_logo():
    with open("ascii_logo.txt", "r") as file:
        content = file.read()
    print("\033[32m" + content + "\033[0m")  


# Function to display the menu with usage instructions
def display_menu():
    print("""
    📜 MENU - Illuminati Cyber Toolkit 📜

    1. Location Finder 📍 - Track IP geolocation details (Country, City, ISP, etc.)

    2. IP Identifier 🌐 - Get Hostname, ISP, and Network Details of any IP.

    3. Network Scanner 🖥 - Scan all connected devices in your network.

    4. Network Mapper 🗺 - Generate a full Network Topology Map.

    5. Link Scanner 🔗 - Scan any website link for vulnerabilities.

    6. Data Capture 📡 - Capture and Analyze Real-Time Network Traffic.

    7. Network Traffic Analyzer 📊 - Monitor & Analyze live network traffic with alerts.

    8. Track Mobile Location 📲 - Track live location of any mobile number.

    9. Metadata Extractor 🗂 - Extract metadata from images, PDFs, and documents.

    10. Subdomain & Port Scanner 🔍 - Discover Open Ports & Active Subdomains.

    11. Password Strength Checker 🔑 - Test Your Password Security.

    12. Exit 🚪 - Quit the Illuminati Cyber Toolkit.

    💀 Use Responsibly - Illuminati Cybersecurity Tool 💀
    """)

def main():
    PY = "/usr/bin/python3.13"

    while True:
        display_logo()
        display_menu()

        option = input("💀 Choose an option: ")
    
        if option == "1":
            os.system(f"{PY} modules/location_finder.py")
        elif option == "2":
            os.system(f"{PY} modules/ip_identifier.py")
        elif option == "3":
            os.system(f"{PY} modules/scan_network.py")
        elif option == "4":
            os.system(f"{PY} modules/network_map.py")
        elif option == "5":
            os.system(f"{PY} modules/link_scanner.py")
        elif option == "6":
            os.system(f"sudo {PY} modules/data_capture.py")
        elif option == "7":
            os.system(f"sudo {PY} modules/network_traffic_analyzer.py")
        elif option == "8":
            os.system(f"{PY} modules/mobile_tracker.py")
        elif option == "9":
            os.system(f"{PY} modules/metadata_extractor.py")
        elif option == "10":
            os.system(f"{PY} modules/subdomain_port_scanner.py")
        elif option == "11":
            os.system(f"{PY} modules/password_strength_checker.py")
        elif option == "12":
            print("\n\033[94m💀 Exiting Illuminati... Stay Secure 💀\033[0m")
            break
        else:
            print("\n\033[91m❌ Invalid option. Try again.\033[0m")
        
        print("\n" + "-"*60)
        input("💀 Press [ENTER] to return to the main menu...")


if __name__ == "__main__":
    main()
