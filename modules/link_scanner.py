import requests
import socket
import whois
import urllib.parse
import re

# List of known phishing keywords in URLs
SUSPICIOUS_KEYWORDS = ["login", "bank", "paypal", "secure", "verify", "update", "account", "confirm", "free", "win"]

# List of phishing & malware blacklists
BLACKLIST_URLS = [
    "https://openphish.com/feed.txt",
    "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links/output/domains.txt",
    "https://urlhaus.abuse.ch/downloads/text_online/"
]

# Expand Shortened URLs
def expand_short_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except requests.RequestException:
        return url

# Get Domain Information
def get_domain_info(url):
    try:
        domain = urllib.parse.urlparse(url).netloc
        ip_address = socket.gethostbyname(domain)
        domain_info = whois.whois(domain)

        return {
            "Domain": domain,
            "IP Address": ip_address,
            "Registrar": domain_info.registrar if domain_info.registrar else "Unknown",
            "Creation Date": domain_info.creation_date[0] if isinstance(domain_info.creation_date, list) else domain_info.creation_date,
            "Expiration Date": domain_info.expiration_date[0] if isinstance(domain_info.expiration_date, list) else domain_info.expiration_date
        }
    except Exception as e:
        return {"Error": f"Unable to fetch domain details: {e}"}

# Check if URL is in Blacklists
def check_blacklist(url):
    domain = urllib.parse.urlparse(url).netloc
    for bl_url in BLACKLIST_URLS:
        try:
            response = requests.get(bl_url, timeout=5)
            blacklist_domains = response.text.splitlines()
            if domain in blacklist_domains:
                return "❌ UNSAFE: URL is Blacklisted!"
        except requests.RequestException:
            continue  # Ignore errors and proceed
    return "✅ SAFE: URL is not in Blacklists."

# Extract Hidden Links from the Page
def extract_links(url):
    try:
        response = requests.get(url, timeout=5)
        links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
        valid_links = [urllib.parse.urljoin(url, link) for link in links if link.startswith(("http", "/"))]
        return valid_links[:5] if valid_links else ["✅ No hidden links found."]
    except requests.RequestException:
        return ["❌ Could not retrieve links."]

# Check for Suspicious Keywords
def check_suspicious_keywords(url):
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in url.lower():
            return "⚠️ WARNING: URL contains suspicious words!"
    return "✅ No suspicious words detected."

# Main Scanner Function
def scan_url():
    url = input("🔗 Enter the URL to scan: ").strip()

    print("\n🔍 Expanding URL...")
    expanded_url = expand_short_url(url)
    print(f"✅ Final URL: {expanded_url}")

    print("\n🌍 Checking Domain Information...")
    domain_info = get_domain_info(expanded_url)
    for key, value in domain_info.items():
        print(f"   {key}: {value}")

    print("\n🛡️ Checking Blacklists...")
    blacklist_result = check_blacklist(expanded_url)
    print(blacklist_result)

    print("\n🔗 Extracting Hidden Links...")
    links = extract_links(expanded_url)
    for link in links:
        print(f"   ➤ {link}")

    print("\n🔎 Checking for Suspicious Keywords...")
    keyword_result = check_suspicious_keywords(expanded_url)
    print(keyword_result)

    # Final Verdict
    print("\n🚀 Final Verdict:")
    if "UNSAFE" in blacklist_result or "WARNING" in keyword_result:
        print("❌ This URL is **UNSAFE**! Do not visit.")
    else:
        print("✅ This URL is **SAFE**!")

    print("\n✅ Scan Completed!")

if __name__ == "__main__":
    scan_url()
