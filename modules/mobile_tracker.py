import phonenumbers
from phonenumbers import geocoder, carrier
import requests
import webbrowser
import time
import json

# Function to track mobile number location
def track_mobile():
    print("📲 Mobile Number Tracker - Find Exact Location")
    print("------------------------------------------------------------")

    # Get mobile number input from user
    mobile_number = input("📞 Enter Mobile Number with Country Code (e.g., +91XXXXXXXXXX): ")

    # Parse the mobile number
    try:
        parsed_number = phonenumbers.parse(mobile_number)
    except phonenumbers.NumberParseException:
        print("❌ Invalid phone number format! Try again.")
        return

    # Get location (Country/Region)
    location = geocoder.description_for_number(parsed_number, "en")

    # Get service provider (Airtel, Jio, Vi, etc.)
    service_provider = carrier.name_for_number(parsed_number, "en")

    print("\n[✔] Phone Number Information:")
    print(f"[✔] Phone Number: {mobile_number}")
    print(f"[✔] Location: {location}")
    print(f"[✔] Service Provider: {service_provider}")

    # ------------------------------------------------
    # 🔍 Automated Name Lookup using OSINT
    # ------------------------------------------------
    print("\n[✔] Searching for Name & Details...")

    # Open NumLookup
    numlookup_url = f"https://www.numlookup.com/?query={mobile_number}"
    webbrowser.open(numlookup_url)

    # Google Search
    google_search_url = f"https://www.google.com/search?q={mobile_number}+phone+number+owner"
    webbrowser.open(google_search_url)

    # Facebook Search (for public profiles)
    fb_search_url = f"https://www.facebook.com/search/top?q={mobile_number}"
    webbrowser.open(fb_search_url)

    # LinkedIn Search (for business profiles)
    linkedin_search_url = f"https://www.linkedin.com/search/results/all/?keywords={mobile_number}"
    webbrowser.open(linkedin_search_url)

    # Telegram Search (to find linked accounts)
    telegram_url = f"https://t.me/{mobile_number}"
    webbrowser.open(telegram_url)

    # WhatsApp Direct Message (To Check Profile Name)
    print(f"\n[✔] To check the WhatsApp profile name, open: https://wa.me/{mobile_number}")

    # ------------------------------------------------
    # IP Address Tracking (Requires Device to be Online)
    # ------------------------------------------------
    print("\n[✔] IP Address Information:")
    try:
        ip_response = requests.get("https://api64.ipify.org?format=json").json()
        public_ip = ip_response.get("ip")

        # Fetch geolocation based on IP
        location_response = requests.get(f"http://ipinfo.io/{public_ip}/json").json()

        city = location_response.get("city", "Unknown")
        region = location_response.get("region", "Unknown")
        country = location_response.get("country", "Unknown")
        org = location_response.get("org", "Unknown")
        loc = location_response.get("loc", "Unknown")

        print(f"[✔] Public IP Address: {public_ip}")
        print(f"[✔] ISP: {org}")
        print(f"[✔] City: {city}")
        print(f"[✔] Region: {region}")
        print(f"[✔] Country: {country}")

    except requests.RequestException:
        print("[✘] Unable to fetch IP information.")

    # ------------------------------------------------
    # Return to main menu automatically
    # ------------------------------------------------
    print("\n💀 Location fetched successfully.")
    print("💀 Returning to the main menu in 5 seconds...")
    time.sleep(5)


if __name__ == "__main__":
    track_mobile()
