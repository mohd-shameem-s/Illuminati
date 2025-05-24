
# 💀 Illuminati -  The Cyber Weapon You Always Needed !

Illuminati is a powerful cybersecurity toolkit designed for penetration testers, ethical hackers, and network administrators. It offers a range of advanced features to perform network mapping, IP tracking, Wi-Fi attacks, metadata extraction, and more.

✅ Built by **[Mohammed Shameem S](https://github.com/mohd-shameem-s)**  
✅ Optimized for **Kali Linux 2024+**  
✅ Designed for **Educational and Penetration Testing Purposes Only**  


## 📦 Requirements

- Python 3.8+
- `tshark` (for PyShark - install via `sudo apt install tshark`)
- `nmap` (for network scanning - `sudo apt install nmap`)
- Internet connection for API-based modules (IP tracking, GeoIP, etc.)


## 💻 Installation Steps
🔄 Updates system package lists and upgrades installed packages
```bash
sudo apt update && sudo apt upgrade -y
```
🐍 Installs Python 3, pip, and Git (requires Python 3.8+)
```bash
sudo apt install python3 python3-pip git -y
```
📥 Clones the Illuminati toolkit repository from GitHub
```bash
git clone https://github.com/mohd-shameem-s/illuminati.git
```
📂 Navigates into the cloned Illuminati project directory
```bash
cd illuminati
```
📦 Installs all required Python dependencies listed in requirements.txt
```bash
sudo pip3 install -r requirements.txt --break-system-packages
```
✅ Makes the main Python script executable
```bash
chmod +x illuminati.py
```
🚀 Launches the Illuminati Cyber Toolkit with root privileges
```bash
sudo python3 illuminati.py
```

## 🚀 Features

### 1. Location Finder 📍
**-> Track IP Geolocation of any public IP address.**

**-> Retrieve details like Country, City, ISP, Coordinates, and Google Maps Link.**

---

### 2. IP Identifier 🌐
**-> Retrieve complete information of any IP address or domain.**

**-> Find Hostname, ISP, IP Range, and Autonomous System Number.**

---

### 3. Network Scanner 🖥️
**-> Scan all connected devices on your network.**

**-> Get IP, MAC Address, Device Type, and Open Ports.**

---

### 4. Network Mapper 🗺️
**-> Generate a full Network Topology Map.**

**-> Identify Routers, Switches, Gateways, and VLANs.**

---

### 5. Link Scanner 🔗
**-> Scan any website link for vulnerabilities.**

**-> Check SSL, Headers, Open Ports, etc.**

---

### 6. Data Capture 📡
**->Capture and Analyze Real-Time Network Traffic.**

---

### 7. Track Mobile Location 📲
**->Track Live Location of any Mobile Number.**

---

### 8. Metadata Extractor 🗂️
**->Extract hidden metadata from images, documents, and PDFs.**

**->Get details like Author, GPS Location, Device Info, and Modification History.**

---

### 9. Subdomain & Port Scanner 🌐
**-> Scan any target domain for active subdomains using Amass and Subfinder.**

**-> Perform a detailed Nmap scan to discover open ports and running services.**

---

### 10. Password Strength Checker 🔐
**-> Check the strength of passwords based on complexity, length, and common patterns.**

**-> Suggest improvements for weak passwords.**

---

### 11. Exit 🚪
**->Quit the Illuminati Cyber Toolkit.**

---


## 📜 Legal Disclaimer
> This tool is for educational and research purposes only. Any misuse of this tool for illegal activities is strictly prohibited. The developer is not responsible for any damage or consequences resulting from the use of this tool.


## 💎 Developed with ❤️ By
**Mohammed Shameem S**
