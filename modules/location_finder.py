import requests
import time

# Function to find geolocation of an IP Address
def location_finder():
    print("💀 Location Finder - Track IP Geolocation")
    print("------------------------------------------------------------")
    
    # Get the target IP address from user input
    target_ip = input("Enter IP Address: ")
    
    # API URL
    api_url = f"http://ipinfo.io/{target_ip}/json"
    
    # Send a request to the API
    response = requests.get(api_url).json()
    
    # Handle response if IP is Private/CGNAT or does not exist
    if 'bogon' in response:
        print("\n💀 Error: This is a private/local IP address or reserved IP.")
        print("💻 Example: 192.168.x.x / 10.x.x.x / 100.64.x.x (CGNAT)")
        print("------------------------------------------------------------")
        print("💀 Returning to the main menu in 5 seconds...")
        time.sleep(5)
        return
    
    # Handle IPs that have no geolocation data
    if response.get('country') is None:
        print("\n💀 Error: No geolocation data found for this IP Address.")
        print("💻 This may be a Private IP or an unknown IP Range.")
        print("------------------------------------------------------------")
        print("💀 Returning to the main menu in 5 seconds...")
        time.sleep(5)
        return
    
    # Extract IP details from response
    ip = response.get('ip', 'Unknown')
    country = response.get('country', 'Unknown')
    region = response.get('region', 'Unknown')
    city = response.get('city', 'Unknown')
    loc = response.get('loc', 'Unknown')
    org = response.get('org', 'Unknown')
    timezone = response.get('timezone', 'Unknown')
    
    # Split latitude and longitude if available
    if loc != 'Unknown':
        latitude, longitude = loc.split(',')
    else:
        latitude, longitude = 'Unknown', 'Unknown'
    
    # Display Results
    print("------------------------------------------------------------")
    print(f"💀 IP Address: {ip}")
    print(f"🌍 Country: {country}")
    print(f"🏙️  Region: {region}")
    print(f"🏠 City: {city}")
    print(f"📍 Latitude: {latitude}")
    print(f"📍 Longitude: {longitude}")
    print(f"🔧 ISP/Organization: {org}")
    print(f"⏱️  Timezone: {timezone}")
    print("------------------------------------------------------------")
    
    # Additional Note if IP is private or untraceable
    if country == 'Unknown':
        print("💀 This IP Address may belong to a Private Network, Carrier Grade NAT, or an internal system.")
    
    # Auto return to the main menu after 5 seconds
    print("💀 Returning to the main menu in 5 seconds...")
    time.sleep(5)


if __name__ == "__main__":
    location_finder()
