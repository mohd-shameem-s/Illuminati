import requests
import socket
import whois
import urllib.parse
import re
import json

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

# List of phishing & malware blacklists
BLACKLIST_URLS = [
    "https://openphish.com/feed.txt",
    "https://urlhaus.abuse.ch/downloads/text_online/"
]

# Suspicious keywords in URLs
SUSPICIOUS_KEYWORDS = [
    "login", "bank", "paypal", "secure", "verify",
    "update", "account", "confirm", "free", "win"
]

# VirusTotal API URL (public scan mode)
VIRUSTOTAL_SCAN_URL = "https://www.virustotal.com/api/v3/urls"

# Expand shortened URLs
def expand_short_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except requests.RequestException:
        return url

# Get domain info
def get_domain_info(url):
    try:
        domain = urllib.parse.urlparse(url).netloc
        ip_address = socket.gethostbyname(domain)
        domain_info = whois.whois(domain)

        return {
            "Domain": domain,
            "IP Address": ip_address,
            "Registrar": domain_info.registrar or "Unknown",
            "Creation Date": domain_info.creation_date[0] if isinstance(domain_info.creation_date, list) else domain_info.creation_date,
            "Expiration Date": domain_info.expiration_date[0] if isinstance(domain_info.expiration_date, list) else domain_info.expiration_date
        }
    except Exception as e:
        return {"Error": f"Unable to fetch domain details: {e}"}

# Check blacklists
def check_blacklist(url):
    domain = urllib.parse.urlparse(url).netloc
    for bl_url in BLACKLIST_URLS:
        try:
            response = requests.get(bl_url, timeout=5)
            if domain in response.text:
                return f"{RED}❌ UNSAFE: URL is Blacklisted!{RESET}"
        except requests.RequestException:
            continue
    return f"{GREEN}✅ SAFE: URL is not in Blacklists.{RESET}"

# Extract hidden links
def extract_links(url):
    try:
        response = requests.get(url, timeout=5)
        links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
        valid_links = [urllib.parse.urljoin(url, link) for link in links if link.startswith(("http", "/"))]
        return valid_links[:5] if valid_links else [f"{GREEN}✅ No hidden links found.{RESET}"]
    except requests.RequestException:
        return [f"{RED}❌ Could not retrieve links.{RESET}"]

# Check for suspicious keywords
def check_suspicious_keywords(url):
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in url.lower():
            return f"{YELLOW}⚠️ WARNING: URL contains suspicious word: '{keyword}'!{RESET}"
    return f"{GREEN}✅ No suspicious words detected.{RESET}"

# VirusTotal check
def check_virustotal(url):
    headers = {"x-apikey": "public"}  # Replace with your API key if needed
    data = {"url": url}
    try:
        response = requests.post(VIRUSTOTAL_SCAN_URL, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            vt_id = result["data"]["id"]
            vt_url = f"https://www.virustotal.com/gui/url/{vt_id}"
            return f"{CYAN}🔍 Check VirusTotal Report: {vt_url}{RESET}"
        else:
            return f"{YELLOW}⚠️ VirusTotal Scan Failed. Try again later.{RESET}"
    except Exception:
        return f"{RED}⚠️ Could not connect to VirusTotal.{RESET}"

# Scanner logic
def scan_url():
    print(f"{MAGENTA}{BOLD}🌐 URL Security Analyzer - Illuminati Toolkit{RESET}")
    url = input(f"{CYAN}🔗 Enter the URL to scan: {RESET}").strip()

    print(f"\n{YELLOW}🔍 Expanding URL...{RESET}")
    expanded_url = expand_short_url(url)
    print(f"{GREEN}✅ Final URL: {expanded_url}{RESET}")

    print(f"\n{YELLOW}🌍 Checking Domain Information...{RESET}")
    domain_info = get_domain_info(expanded_url)
    for key, value in domain_info.items():
        print(f"  {BOLD}{key}:{RESET} {CYAN}{value}{RESET}")

    print(f"\n{YELLOW}🛡️ Checking Blacklists...{RESET}")
    print(check_blacklist(expanded_url))

    print(f"\n{YELLOW}🔗 Extracting Hidden Links...{RESET}")
    links = extract_links(expanded_url)
    for link in links:
        print(f"   ➤ {link}")

    print(f"\n{YELLOW}🔎 Checking for Suspicious Keywords...{RESET}")
    print(check_suspicious_keywords(expanded_url))

    print(f"\n{YELLOW}🦠 Checking VirusTotal Database...{RESET}")
    print(check_virustotal(expanded_url))

    print(f"\n{BOLD}🚀 Final Verdict:{RESET}")
    if "UNSAFE" in check_blacklist(expanded_url) or "WARNING" in check_suspicious_keywords(expanded_url):
        print(f"{RED}❌ This URL is considered UNSAFE! Avoid visiting it.{RESET}")
    else:
        print(f"{GREEN}✅ This URL appears to be SAFE.{RESET}")

    print(f"\n{GREEN}✅ Scan Completed! Stay safe online.{RESET}")

if __name__ == "__main__":
    scan_url()
