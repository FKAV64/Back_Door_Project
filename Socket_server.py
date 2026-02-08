import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

s = socket.socket()
s.bind((HOST_IP, HOST_PORT))
s.listen()

print(f"Listening for connection on {HOST_IP}, port {HOST_PORT}.......")
connection_socket, client_address = s.accept()
print(f"Connection established with {client_address}")
s.close()
while True:
    text = input("YOU: ")
    if text == "" : break
    connection_socket.sendall(text.encode())
    data_received = connection_socket.recv(MAX_DATA_SIZE)
    if data_received:
        print(f"MESSAGE : {data_received.decode()}")
    else:
        print("No data received")

connection_socket.close()