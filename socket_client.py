import socket
import time

HOST_IP = "127.0.0.1"
HOST_PORT = 32000

s = socket.socket()
print(f"Connecting to {HOST_IP}, port {HOST_PORT}......")
while True:
    try:
        s.connect((HOST_IP, HOST_PORT))
    except ConnectionRefusedError:
        print(f"Impossible to connect to server. Reconnection.....")
        time.sleep(4)
    else:
        print("Connection established")
        break

s.close()
