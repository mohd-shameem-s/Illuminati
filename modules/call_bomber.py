import requests
import time

def send_call(phone_number, count):
    CALL_API = "https://api.callmebot.com/start.php"

    for i in range(count):
        data = {
            "phone": phone_number,
            "apikey": "free",  # Replace with actual API key if needed
            "text": "This is a test call from Illuminati tool."
        }

        response = requests.post(CALL_API, data=data)
        if response.status_code == 200:
            print(f"[+] Call {i+1}/{count} Sent Successfully")
        else:
            print(f"[-] Call {i+1}/{count} Failed")

        time.sleep(2)  # Avoid spamming detection

# User input
phone_number = input("📞 Enter target phone number: ")
count = int(input("🔢 Enter number of calls to make: "))

# Run Call Bomber
send_call(phone_number, count)
