import os

# Function to display the ASCII logo
def display_logo():
    with open("ascii_logo.txt", "r") as file:
        print(file.read())

# Function to display the menu with usage instructions
def display_menu():
    print("""
    📜 MENU - Illuminati Cyber Toolkit 📜

    1. Location Finder 📍 - Track IP geolocation details (Country, City, ISP, etc.)

    2. IP Identifier 🌐 - Get Hostname, ISP, and Network Details of any IP.

    3. Network Scanner 🖥️ - Scan all connected devices in your network.

    4. Network Mapper 🗺️ - Generate a full Network Topology Map.

    5. Link Scanner 🔗 - Scan any website link for vulnerabilities.

    6. Data Capture 📡 - Capture and Analyze Real-Time Network Traffic.

    7. Network Traffic Analyzer 📊 - Monitor & Analyze live network traffic with alerts.

    8. Track Mobile Location 📲 - Track live location of any mobile number.

    9. Metadata Extractor 🗂️ - Extract metadata from images, PDFs, and documents.

    10. Wi-Fi Deauthentication Attack ⚠️ - Disconnect devices from a Wi-Fi network.

    11. Exit 🚪 - Quit the Illuminati Cyber Toolkit.

    💀 Use Responsibly - Illuminati Cybersecurity Tool 💀
    """)

def main():
    while True:
        # Display the logo and menu
        display_logo()
        display_menu()
        
        # User input
        option = input("💀 Choose an option: ")
        
        if option == "1":
            os.system("python3 modules/location_finder.py")
        elif option == "2":
            os.system("python3 modules/ip_identifier.py")
        elif option == "3":
            os.system("python3 modules/scan_network.py")
        elif option == "4":
            os.system("python3 modules/network_map.py")
        elif option == "5":
            os.system("python3 modules/link_scanner.py")
        elif option == "6":
            os.system("sudo python3 modules/data_capture.py")
        elif option == "7":
            os.system("sudo python3 modules/network_traffic_analyzer.py")
        elif option == "8":
            os.system("python3 modules/mobile_tracker.py")
        elif option == "9":
            os.system("python3 modules/metadata_extractor.py")
        elif option == "10":
            os.system("sudo python3 modules/wifi_deauth.py")
        elif option == "11":
            print("\n💀 Exiting Illuminati... Stay Secure 💀")
            break
        else:
            print("\n❌ Invalid option. Try again.")
        
        # ✅ Separator after each module execution
        print("\n" + "-"*60)
        input("💀 Press [ENTER] to return to the main menu...")

if __name__ == "__main__":
    main()
