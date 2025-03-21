import os
import subprocess
import re
import sublist3r

def scan_ports(target):
    """Scan open ports on the target domain/IP using nmap."""
    print(f"\n[+] Scanning open ports on {target}...")
    command = f"nmap -Pn -p- --open {target}"
    result = subprocess.getoutput(command)
    print(result)

def scan_subdomains(target):
    """Find active subdomains using sublist3r."""
    print(f"\n[+] Scanning for active subdomains of {target}...")
    subdomains = sublist3r.main(target, 40, savefile=None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
    
    if subdomains:
        print("\n[+] Found Subdomains:")
        for sub in subdomains:
            print(f"  - {sub}")
    else:
        print("[!] No active subdomains found.")

if __name__ == "__main__":
    target_domain = input("Enter the target domain (e.g., example.com): ").strip()
    
    if not target_domain:
        print("[!] Invalid input. Please enter a valid domain.")
        exit(1)
    
    scan_ports(target_domain)
    scan_subdomains(target_domain)
