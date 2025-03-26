import os
import subprocess
import shutil
import re

# Check if Sublist3r is installed
try:
    import sublist3r
    SUBLIST3R_AVAILABLE = True
except ImportError:
    SUBLIST3R_AVAILABLE = False


def check_tool_installed(tool):
    """Check if a command-line tool is installed."""
    return shutil.which(tool) is not None


def scan_ports(target):
    """Scan open ports on the target domain/IP using nmap."""
    if not check_tool_installed("nmap"):
        print("[❌] Nmap is not installed. Install it using: sudo apt install nmap")
        return
    
    print(f"\n[🔍] Scanning open ports on {target} using Nmap...\n")
    
    try:
        command = f"nmap -Pn -p- --open {target}"
        result = subprocess.getoutput(command)
        print(result)
    except Exception as e:
        print(f"[❌] Error during port scan: {e}")


def scan_subdomains(target):
    """Find active subdomains using Sublist3r or fallback to Amass."""
    
    if SUBLIST3R_AVAILABLE:
        print(f"\n[🔍] Scanning for active subdomains of {target} using Sublist3r...\n")
        
        try:
            subdomains = sublist3r.main(
                domain=target, 
                threads=40, 
                savefile=None, 
                ports=None, 
                silent=True, 
                verbose=False, 
                enable_bruteforce=False, 
                engines=None
            )
            
            if subdomains:
                print("\n[✔] Found Subdomains:")
                for sub in subdomains:
                    print(f"  - {sub}")
            else:
                print("[❌] No active subdomains found.")

        except IndexError:
            print("[⚠️] Sublist3r encountered an issue with parsing DNSDumpster response. Consider updating Sublist3r.")
        except Exception as e:
            print(f"[❌] Error using Sublist3r: {e}")

    else:
        print("\n[⚠️] Sublist3r is not installed. Falling back to Amass...\n")
        if check_tool_installed("amass"):
            try:
                print(f"[🔍] Scanning for active subdomains of {target} using Amass...\n")
                command = f"amass enum -d {target}"
                result = subprocess.getoutput(command)
                print(result)
            except Exception as e:
                print(f"[❌] Error using Amass: {e}")
        else:
            print("[❌] Amass is not installed. Install it using: sudo apt install amass")


if __name__ == "__main__":
    target_domain = input("🔹 Enter the target domain (e.g., example.com): ").strip()
    
    if not target_domain:
        print("[❌] Invalid input. Please enter a valid domain.")
        exit(1)
    
    scan_ports(target_domain)
    scan_subdomains(target_domain)
