import socket

target = input("Enter IP Address: ")

try:
    host_name = socket.gethostbyaddr(target)
    print(f"Hostname: {host_name[0]}")
    print(f"Aliases: {host_name[1]}")
    print(f"IP Address: {host_name[2][0]}")
except socket.herror:
    print("Unknown host or IP is private.")
