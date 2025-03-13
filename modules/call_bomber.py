import requests
import time
import random

# Free Call APIs (Limited)
CALL_APIs = [
    {
        "name": "CallMeBot",
        "url": "https://api.callmebot.com/start.php",
        "params": lambda num, msg: {"source": "python", "phone": num, "text": msg, "lang": "en-uk", "apikey": "123456"},  # Requires setup
    }
]

def send_call(phone_number, message, count=2, delay=10):
    print(f"📞 Sending {count} Calls to {phone_number}")

    for i in range(count):
        sent = False

        for api in CALL_APIs:
            try:
                print(f"[*] Trying {api['name']} for Call {i+1}/{count}...")

                response = requests.get(api["url"], params=api["params"](phone_number, message), verify=False)
                result = response.text

                if response.status_code == 200 and "success" in result.lower():
                    print(f"[+] Call Sent Successfully via {api['url']}")
                    sent = True
                    break
                else:
                    print(f"[-] Call Failed via {api['url']} - Response: {result}")

            except Exception as e:
                print(f"[!] Error with {api['name']}: {str(e)}")

        if not sent:
            print(f"[✖] Call #{i+1} failed. No working API.")
        time.sleep(random.randint(delay, delay + 3))

    print("\n💀 Call Bombing Completed! 💀")

# Example usage
if __name__ == "__main__":
    phone_number = input("📞 Enter Target Phone Number: ")
    message = input("📞 Enter Message for Call: ")
    count = int(input("📞 How many Calls to make? (Max 10 to avoid detection): "))
    delay = int(input("⏱ Enter delay between calls (in seconds): "))

    send_call(phone_number, message, count, delay)
