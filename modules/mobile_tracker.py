import phonenumbers
from phonenumbers import geocoder, carrier
import requests
import json

# Function to get mobile number details
def track_mobile():
    print("📍 Mobile Number Tracker - Get SIM Registration Location")
    print("------------------------------------------------------------")

    # Get mobile number input from user
    mobile_number = input("Enter Mobile Number with Country Code (e.g., +91XXXXXXXXXX): ")

    # Parse the mobile number
    parsed_number = phonenumbers.parse(mobile_number)

    # Get registered location
    location = geocoder.description_for_number(parsed_number, "en")

    # Get carrier (Jio, Airtel, AT&T, etc.)
    service_provider = carrier.name_for_number(parsed_number, "en")

    # Display phone number details
    print("\n[+] Phone Number Details:")
    print(f"[+] Phone Number: {mobile_number}")
    print(f"[+] Registered Location: {location} (Not Real-Time)")
    print(f"[+] Service Provider: {service_provider}")

    # Try IP-based location tracking
    print("\n🌎 Attempting to Fetch Approximate Location via IP...")
    try:
        # Get public IP address of the device
        ip_response = requests.get("https://api64.ipify.org?format=json").json()
        public_ip = ip_response.get("ip")

        # Fetch location based on IP address
        location_response = requests.get(f"https://ipinfo.io/{public_ip}/json").json()

        city = location_response.get("city", "Unknown")
        region = location_response.get("region", "Unknown")
        country = location_response.get("country", "Unknown")
        org = location_response.get("org", "Unknown")
        loc = location_response.get("loc", "Unknown")

        latitude, longitude = loc.split(",") if loc != "Unknown" else ("Unknown", "Unknown")

        print("\n[+] Approximate Location Based on IP:")
        print(f"[+] Public IP: {public_ip}")
        print(f"[+] ISP: {org}")
        print(f"[+] City: {city}")
        print(f"[+] Region: {region}")
        print(f"[+] Country: {country}")
        print(f"[+] Google Maps Link: https://maps.google.com/?q={latitude},{longitude}")
    except:
        print("❌ Unable to fetch IP-based location.")

    print("\n✅ Location Fetch Completed.")


# Run the function
if __name__ == "__main__":
    track_mobile()
