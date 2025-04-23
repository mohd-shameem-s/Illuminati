import phonenumbers
from phonenumbers import geocoder, carrier
import requests
import webbrowser
import time
import json

# ANSI Color Codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

def track_mobile():
    print(f"\n{BOLD}{MAGENTA}📲 Mobile Number Tracker - Find Exact Location{RESET}")
    print(f"{BLUE}" + "-" * 60 + f"{RESET}")

    # Get mobile number input from user
    mobile_number = input(f"{GREEN}📞 Enter Mobile Number with Country Code (e.g., +91XXXXXXXXXX): {RESET}").strip()

    # Parse the mobile number
    try:
        parsed_number = phonenumbers.parse(mobile_number)
    except phonenumbers.NumberParseException:
        print(f"{RED}❌ Invalid phone number format! Try again.{RESET}")
        return

    # Get location (Country/Region)
    location = geocoder.description_for_number(parsed_number, "en")

    # Get service provider (Airtel, Jio, Vi, etc.)
    service_provider = carrier.name_for_number(parsed_number, "en")

    print(f"\n{BOLD}{CYAN}[✔] Phone Number Information:{RESET}")
    print(f"{YELLOW}📱 Phone Number: {RESET}{CYAN}{mobile_number}{RESET}")
    print(f"{YELLOW}🌐 Location: {RESET}{CYAN}{location or 'N/A'}{RESET}")
    print(f"{YELLOW}🏢 Service Provider: {RESET}{CYAN}{service_provider or 'N/A'}{RESET}")

    # WhatsApp Direct Link
    print(f"\n{GREEN}[✔] To check the WhatsApp profile name, open:{RESET} {BLUE}https://wa.me/{mobile_number}{RESET}")

    # IP Address Tracking (Assumes tracking system device is online)
    print(f"\n{BOLD}{CYAN}[✔] IP Address Information:{RESET}")
    try:
        ip_response = requests.get("https://api64.ipify.org?format=json").json()
        public_ip = ip_response.get("ip")

        location_response = requests.get(f"http://ipinfo.io/{public_ip}/json").json()
        city = location_response.get("city", "Unknown")
        region = location_response.get("region", "Unknown")
        country = location_response.get("country", "Unknown")
        org = location_response.get("org", "Unknown")
        loc = location_response.get("loc", "Unknown")

        print(f"{YELLOW}🌐 Public IP Address: {RESET}{CYAN}{public_ip}{RESET}")
        print(f"{YELLOW}🏢 ISP: {RESET}{CYAN}{org}{RESET}")
        print(f"{YELLOW}🏙️  City: {RESET}{CYAN}{city}{RESET}")
        print(f"{YELLOW}🗺️  Region: {RESET}{CYAN}{region}{RESET}")
        print(f"{YELLOW}🌍 Country: {RESET}{CYAN}{country}{RESET}")
        print(f"{YELLOW}📌 Google Maps: {RESET}{BLUE}https://www.google.com/maps?q={loc}{RESET}")

    except requests.RequestException:
        print(f"{RED}[✘] Unable to fetch IP information.{RESET}")

    # Return to main menu automatically
    print(f"\n{MAGENTA}💀 Location fetched successfully.{RESET}")
    print(f"{YELLOW}💀 Returning to the main menu in 5 seconds...{RESET}")
    time.sleep(5)

if __name__ == "__main__":
    track_mobile()
