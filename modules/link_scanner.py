import requests
import socket
import whois
import urllib.parse
import re
import time

# Function to expand shortened URLs
def expand_short_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except:
        return url

# Function to get domain information
def get_domain_info(url):
    try:
        domain = urllib.parse.urlparse(url).netloc
        ip_address = socket.gethostbyname(domain)
        domain_info = whois.whois(domain)

        return {
            "Domain": domain,
            "IP Address": ip_address,
            "Registrar": domain_info.registrar,
            "Creation Date": domain_info.creation_date,
            "Expiration Date": domain_info.expiration_date
        }
    except:
        return {"Error": "Unable to fetch domain details"}

# Function to check if the URL is in known blacklists
def check_blacklist(url):
    blacklists = [
        "https://openphish.com/feed.txt",
        "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links/output/domains.txt"
    ]
    domain = urllib.parse.urlparse(url).netloc

    for bl in blacklists:
        try:
            response = requests.get(bl, timeout=5)
            if domain in response.text:
                return f"⚠️ WARNING: {domain} is blacklisted!"
        except:
            pass

    return "✅ URL not found in public blacklists."

# Function to extract hidden links from the page
def extract_links(url):
    try:
        response = requests.get(url, timeout=5)
        links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
        return links[:5]  # Show first 5 links
    except:
        return ["❌ Could not retrieve links."]

# Main Function
def scan_link():
    url = input("🔗 Enter the URL to scan: ")

    print("\n🔍 Expanding URL...")
    expanded_url = expand_short_url(url)
    print(f"✅ Final URL: {expanded_url}")

    print("\n🌍 Checking Domain Information...")
    domain_info = get_domain_info(expanded_url)
    for key, value in domain_info.items():
        print(f"   {key}: {value}")

    print("\n🛡️ Checking Blacklists...")
    print(check_blacklist(expanded_url))

    print("\n🔗 Extracting Hidden Links...")
    links = extract_links(expanded_url)
    for link in links:
        print(f"   ➤ {link}")

    print("\n✅ Scan Completed!")

if __name__ == "__main__":
    scan_link()
