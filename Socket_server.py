import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 32000

s = socket.socket()
s.bind((HOST_IP, HOST_PORT))
s.listen()

print(f"Listening for connection on {HOST_IP}, port {HOST_PORT}.......")
connection_socket, client_address = s.accept()
print(f"Connection established with {client_address}")

s.close()