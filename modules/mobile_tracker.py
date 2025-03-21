import phonenumbers
from phonenumbers import geocoder, carrier
import requests
import time

# Function to track mobile number location
def track_mobile():
    print("📲 Mobile Number Tracker - Find Exact Location")
    print("------------------------------------------------------------")
    
    # Get mobile number input from user
    mobile_number = input("📞 Enter Mobile Number with Country Code (e.g., +91XXXXXXXXXX): ")
    
    # Parse the mobile number
    parsed_number = phonenumbers.parse(mobile_number)

    # Get location (Country/Region)
    location = geocoder.description_for_number(parsed_number, "en")

    # Get service provider (Airtel, Jio, Vi, etc.)
    service_provider = carrier.name_for_number(parsed_number, "en")

    print("\n[✔] Phone Number Information:")
    print(f"[✔] Phone Number: {mobile_number}")
    print(f"[✔] Location: {location}")
    print(f"[✔] Service Provider: {service_provider}")

    # ------------------------------------------------
    # Truecaller / OpenCNAM Integration (Requires API Key)
    # ------------------------------------------------
    print("\n[✔] Checking Name & Details from Truecaller...")
    try:
        truecaller_url = f"https://api.opencnam.com/v3/phone/{mobile_number}?account_sid=YOUR_ACCOUNT_SID&auth_token=YOUR_AUTH_TOKEN"
        truecaller_response = requests.get(truecaller_url).json()
        owner_name = truecaller_response.get("name", "Unknown")
        print(f"[✔] Owner Name: {owner_name}")
    except:
        print("[✘] Name lookup failed (Requires API Key).")

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
        
        # Extract latitude and longitude
        if loc != 'Unknown':
            latitude, longitude = loc.split(',')
        else:
            latitude, longitude = 'Unknown', 'Unknown'
        
        print(f"[✔] Public IP Address: {public_ip}")
        print(f"[✔] ISP: {org}")
        print(f"[✔] City: {city}")
        print(f"[✔] Region: {region}")
        print(f"[✔] Country: {country}")
    except:
        print("[✘] Unable to fetch IP information.")

    # ------------------------------------------------
    # Google Maps Location Tracking
    # ------------------------------------------------
    print("\n[✔] Geolocation Information:")
    print(f"[✔] Latitude: {latitude}")
    print(f"[✔] Longitude: {longitude}")
    print(f"[✔] Google Maps Link: https://maps.google.com/?q={latitude},{longitude}")

    # ------------------------------------------------
    # Return to main menu automatically
    # ------------------------------------------------
    print("\n💀 Location fetched successfully.")
    print("💀 Returning to the main menu in 5 seconds...")
    time.sleep(5)


if __name__ == "__main__":
    track_mobile()
