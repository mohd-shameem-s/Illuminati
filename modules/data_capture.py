import os
import time

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Display header
print(f"{CYAN}{BOLD}🔍 Illuminati - Real-Time Network Traffic Capture 🔍{RESET}")
print(f"{YELLOW}-------------------------------------------------------{RESET}")
print(f"{GREEN}📡 Capturing network traffic on all interfaces...{RESET}")
print(f"{RED}⚠️  Press CTRL+C to stop the capture at any time.{RESET}")
print(f"{YELLOW}-------------------------------------------------------{RESET}")
time.sleep(2)

# Run tcpdump
os.system('sudo tcpdump -i any')
