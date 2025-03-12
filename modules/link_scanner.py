import os
import time
import re

# Function to scan the URL using Nikto
def scan_link():
    print("💀 Link Scanner - Scanning for vulnerabilities...")
    print("------------------------------------------------------------")
    
    # Get the target URL from user input
    target_url = input("Enter URL to scan (e.g., example.com or http://example.com): ")

    # Check if the URL has http/https or not
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        print("⚠️ Warning: You did not specify HTTP or HTTPS")
        print("💣 Proceeding with the URL as given...")
        time.sleep(2)
    
    # Run Nikto Scanner with the exact URL without appending anything
    nikto_command = f"nikto -host {target_url}"
    os.system(nikto_command)
    
    # Extract Domain/IP from URL for better results
    domain = re.sub(r"https?://", "", target_url)
    
    # Auto-judge security based on common vulnerability results
    secure_status = "✅ Secure"
    vulnerable = False
    
    # Open the Nikto output file if it exists
    nikto_log_path = f"/var/log/nikto.log"
    
    # Read the file if it exists
    if os.path.exists(nikto_log_path):
        with open(nikto_log_path, "r") as log_file:
            content = log_file.read()
            
            # Check for X-Content-Type-Options vulnerability
            if "X-Content-Type-Options header is not set" in content:
                secure_status = "❌ Unsecure"
                vulnerable = True
            
            # Check for Uncommon Headers
            if "uncommon header" in content.lower():
                secure_status = "❌ Unsecure"
                vulnerable = True
            
            # Check for Missing Secure Headers
            if "Missing Strict-Transport-Security header" in content:
                secure_status = "❌ Unsecure"
                vulnerable = True
    
    # Display the result
    print("------------------------------------------------------------")
    print(f"💀 Scanning Completed for: {target_url}")
    print(f"🌐 Domain/IP: {domain}")
    
    # Final security status
    if vulnerable:
        print("💀 Final Status: ❌ Unsecure (Vulnerabilities Found)")
    else:
        print("💀 Final Status: ✅ Secure (No Major Vulnerabilities Found)")
    
    # Auto-return to the main menu after 5 seconds
    print("------------------------------------------------------------")
    print("💀 Returning to the main menu in 5 seconds...")
    time.sleep(5)

if __name__ == "__main__":
    scan_link()
