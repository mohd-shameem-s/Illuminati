
# 💀 Illuminati -  The Cyber Weapon You Always Needed !

Illuminati is a powerful cybersecurity toolkit designed for penetration testers, ethical hackers, and network administrators. It offers a range of advanced features to perform network mapping, IP tracking, Wi-Fi attacks, metadata extraction, and more.

✅ Built by **[Mohammed Shameem S](https://github.com/mohd-shameem-s)**  
✅ Optimized for **Kali Linux 2024+**  
✅ Designed for **Educational and Penetration Testing Purposes Only**  


## 💻 Installation
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y
git clone https://github.com/mohd-shameem-s/illuminati.git
cd illuminati
sudo pip3 install -r requirements.txt --break-system-packages
chmod +x illuminati.py
sudo python3 illuminati.py
```

## 🚀 Features

### 1. Location Finder 📍
**-> Track IP Geolocation of any public IP address.**

**-> Retrieve details like Country, City, ISP, Coordinates, and Google Maps Link.**

**Example Output:**
```
Enter IP Address: 100.109.142.38
[+] IP Address: 100.109.142.38
[+] Country: India
[+] Region: Tamil Nadu
[+] City: Chennai
[+] ISP: Airtel
[+] Latitude: ab.cdef
[+] Longitude: gh.ijkh
[+] Google Maps Link: https://maps.google.com/?q=ab.cdef,gh.ijkh
```

---

### 2. IP Identifier 🌐
**-> Retrieve complete information of any IP address or domain.**

**-> Find Hostname, ISP, IP Range, and Autonomous System Number.**

**Example Output:**
```
Enter IP Address: 172.217.166.110
[+] Hostname: bom07s17-in-f14.1e100.net
[+] ISP: Google LLC
[+] Organization: Google LLC
[+] Country: United States
```

---

### 3. Network Scanner 🖥️
**-> Scan all connected devices on your network.**

**-> Get IP, MAC Address, Device Type, and Open Ports.**

**Example Output:**
```
Scanning your network...
[+] Device: Phone - 192.168.1.12 - MAC: 08:ED:6F:XX:XX:XX
[+] Device: Laptop - 192.168.1.14 - MAC: 9A:1B:2C:XX:XX:XX
[+] Device: PC - 192.168.1.15 - MAC: 6B:3E:8F:XX:XX:XX
```

---

### 4. Network Mapper 🗺️
**-> Generate a full Network Topology Map.**

**-> Identify Routers, Switches, Gateways, and VLANs.**

**Example Output:**
```
Generating Network Map...
[+] Router -> Laptop -> Mobile -> PC
[+] Router -> IoT Device
[+] Router -> Printer
Network map generated successfully as 'network_map.png'
```

---

### 5. Link Scanner 🔗
**-> Scan any website link for vulnerabilities.**

**-> Check SSL, Headers, Open Ports, etc.**

**Example Output:**
```
Enter URL: https://example.com
[+] Scanning for vulnerabilities...
[+] Found XSS Vulnerability
[+] Found SQL Injection Vulnerability
[+] Found Directory Traversal Vulnerability
[+] Website Status: Unsecure
```

---

### 6. Data Capture 📡
**->Capture and Analyze Real-Time Network Traffic.**

**Example Output:**
```
Capturing Network Traffic...
[+] Source IP: 192.168.1.12 -> Destination IP: 192.168.1.1
[+] Protocol: TCP
[+] Packet Size: 512 bytes
[+] Data Captured Successfully
```

---

### 7. Track Mobile Location 📲
**->Track Live Location of any Mobile Number.**

**Example Output:**
```
Enter Mobile Number: +9198xx54xx10
[+] Phone Number: +9198xx54xx10
[+] Location: Bangalore, Karnataka
[+] Service Provider: Airtel
[+] Latitude: ab.cdef
[+] Longitude: gh.ijkh
[+] Google Maps Link: https://maps.google.com/?q=ab.cdef,gh.ijkh
```

---

### 8. Metadata Extractor 🗂️
**->Extract hidden metadata from images, documents, and PDFs.**

**->Get details like Author, GPS Location, Device Info, and Modification History.**

**Example Output:**
```
Enter File Path: example.jpg
[+] File: example.jpg
[+] Author: John Doe
[+] Camera Model: Canon EOS 80D
[+] GPS Coordinates: 37.7749° N, 122.4194° W
[+] Created On: 2024-03-10

```

---

### 9. Subdomain & Port Scanner 🌐
**-> Scan any target domain for active subdomains using Amass and Subfinder.**

**-> Perform a detailed Nmap scan to discover open ports and running services.**

**Example Output:**
```
Enter Domain: example.com
[+] Found Subdomains:
 - mail.example.com
 - blog.example.com
 - dev.example.com

[+] Starting Nmap Port Scan...
 - Open Port: 22 (SSH)
 - Open Port: 80 (HTTP)
 - Open Port: 443 (HTTPS)
Port Scan Completed Successfully.

```

---

### 10. Password Strength Checker 🔐
**-> Check the strength of passwords based on complexity, length, and common patterns.**

**-> Suggest improvements for weak passwords.**

**Example Output:**
```
🔐 Enter your password to check its strength: Admin123

🔐 Checking Password Strength...

[✅] Length (>= 12 chars): ❌
[✅] Uppercase Letter
[✅] Lowercase Letter
[✅] Digit
[❌] Special Character

[⚠] WARNING: This is a commonly used weak password!

[+] Password Strength: Very Weak ❌

📌 Suggestions to improve your password:
 - Use at least 12 characters.
 - Add special characters (e.g., !@#$%).
 - Avoid common passwords (e.g., 'admin', '123456', 'password').

```

---

### 11. Exit 🚪
**->Quit the Illuminati Cyber Toolkit.**

---



## 📜 Legal Disclaimer
This tool is for educational and research purposes only. The misuse of this tool for illegal purposes is strictly prohibited. The developer is not responsible for any misuse or damage caused by this tool.


## 💎 Developed with -`♡´- By
**Mohammed Shameem S**
