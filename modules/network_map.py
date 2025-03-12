import os
import socket

ip = socket.gethostbyname(socket.gethostname())
network_range = ip.rsplit('.', 1)[0] + '.0/24'

print(f"[+] Your Device IP Address: {ip}")
print(f"[+] Network Range Identified: {network_range}")
print("[+] Mapping All Devices on the Network...")

os.system(f'nmap -sP {network_range}')
