import os

print("Capturing network traffic...")
print("Press CTRL+C to stop.")

os.system('sudo tcpdump -i any')
