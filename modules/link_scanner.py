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

# Public blacklist feeds
BLACKLIST_URLS = [
    "https://openphish.com/feed.txt",
    "https://urlhaus.abuse.ch/downloads/text_online/"
]

# Suspicious domain name keywords
SUSPICIOUS_KEYWORDS = [
    "login", "bank", "paypal", "secure", "verify",
    "update", "account", "confirm", "free", "win"
]

# VirusTotal API URL
VIRUSTOTAL_SCAN_URL = "https://www.virustotal.com/api/v3/urls"

# (Optional) Replace with your actual VirusTotal API Key
VIRUSTOTAL_API_KEY = None  # e.g. "your_api_key_here"


# Expand shortened URL
def expand_short_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except requests.RequestException:
        return url


# WHOIS & DNS info
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


# Check against phishing/malware blacklists
def check_blacklist(url):
    domain = urllib.parse.urlparse(url).netloc.strip().lower()
    for bl_url in BLACKLIST_URLS:
        try:
            response = requests.get(bl_url, timeout=10)
            blacklisted_domains = set(line.strip().lower() for line in response.text.splitlines())
            if domain in blacklisted_domains:
                return f"{RED}❌ UNSAFE: Domain is Blacklisted!{RESET}"
        except requests.RequestException:
            continue
    return f"{GREEN}✅ SAFE: Not found in public blacklists.{RESET}"


# Extract hidden/embedded links from page
def extract_links(url):
    try:
        response = requests.get(url, timeout=8)
        links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
        valid_links = [urllib.parse.urljoin(url, link) for link in links if link.startswith(("http", "/"))]
        return valid_links[:5] if valid_links else [f"{GREEN}✅ No suspicious links found.{RESET}"]
    except requests.RequestException:
        return [f"{RED}❌ Failed to retrieve page or extract links.{RESET}"]


# Detect suspicious words in domain only
def check_suspicious_keywords(url):
    domain = urllib.parse.urlparse(url).netloc.lower()
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in domain:
            return f"{YELLOW}⚠️ WARNING: Domain contains suspicious keyword: '{keyword}'!{RESET}"
    return f"{GREEN}✅ No suspicious domain keywords detected.{RESET}"


# Optional VirusTotal check (public scan only)
def check_virustotal(url):
    if not VIRUSTOTAL_API_KEY:
        return f"{YELLOW}⚠️ Skipping VirusTotal scan (no API key).{RESET}"

    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    data = {"url": url}
    try:
        response = requests.post(VIRUSTOTAL_SCAN_URL, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            vt_id = result["data"]["id"]
            vt_url = f"https://www.virustotal.com/gui/url/{vt_id}"
            return f"{CYAN}🔍 Check full VirusTotal Report: {vt_url}{RESET}"
        else:
            return f"{YELLOW}⚠️ VirusTotal scan failed or throttled. Status: {response.status_code}{RESET}"
    except Exception:
        return f"{RED}❌ Could not connect to VirusTotal.{RESET}"


# Main scan function
def scan_url():
    print(f"{MAGENTA}{BOLD}🌐 Illuminati Link Scanner - Advanced URL Analyzer{RESET}")
    url = input(f"{CYAN}🔗 Enter the URL to scan: {RESET}").strip()

    print(f"\n{YELLOW}🔄 Expanding URL...{RESET}")
    expanded_url = expand_short_url(url)
    print(f"{GREEN}✅ Final URL: {expanded_url}{RESET}")

    print(f"\n{YELLOW}🌍 Fetching Domain Information...{RESET}")
    domain_info = get_domain_info(expanded_url)
    for key, value in domain_info.items():
        print(f"{BOLD}  {key}:{RESET} {CYAN}{value}{RESET}")

    print(f"\n{YELLOW}🛡️ Blacklist Check...{RESET}")
    print(check_blacklist(expanded_url))

    print(f"\n{YELLOW}🔗 Hidden Link Extraction...{RESET}")
    links = extract_links(expanded_url)
    for link in links:
        print(f"   ➤ {link}")

    print(f"\n{YELLOW}🕵️ Suspicious Keyword Detection...{RESET}")
    print(check_suspicious_keywords(expanded_url))

    print(f"\n{YELLOW}🦠 VirusTotal Check (Optional)...{RESET}")
    print(check_virustotal(expanded_url))

    print(f"\n{BOLD}🧾 Final Verdict:{RESET}")
    verdict = []
    if "UNSAFE" in check_blacklist(expanded_url):
        verdict.append("blacklist")
    if "WARNING" in check_suspicious_keywords(expanded_url):
        verdict.append("keyword")
    
    if verdict:
        print(f"{RED}❌ The URL is considered potentially UNSAFE! Avoid using it.{RESET}")
    else:
        print(f"{GREEN}✅ This URL appears to be safe and trustworthy.{RESET}")

    print(f"\n{GREEN}✅ Scan Complete. Stay secure!{RESET}")


if __name__ == "__main__":
    scan_url()
