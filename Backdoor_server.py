import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

def socket_receive_all_data(socket_p, data_len):
    # The none initialisation of data_received is to notify the caller that the data has not been received if data_len is 0
    data_received = None
    current_data_length = 0
    while current_data_length < data_len:
        chunk_len = data_len-current_data_length
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data_segment = socket_p.recv(chunk_len)
        if not data_segment:
            return None
        if not data_received:
            data_received = data_segment
        else:
            data_received += data_segment
        current_data_length += len(data_segment)
    return data_received

def send_command_and_receive_all_data(socket_p, command):
    if not command:
        return None
    socket_p.sendall(command.encode())
    header_data = socket_p.recv(13)
    data_len = int(header_data.decode())
    data_received = socket_receive_all_data(socket_p, data_len)
    return data_received


s = socket.socket()
s.bind((HOST_IP, HOST_PORT))
s.listen()

print(f"Listening for connection on {HOST_IP}, port {HOST_PORT}.......")
connection_socket, client_address = s.accept()
print(f"Connection established with {client_address}")
s.close()
while True:
    client_machine_info = send_command_and_receive_all_data(connection_socket, "info")
    if not client_machine_info:
        break
    command = input(f"{client_machine_info.decode()} >  ")
    data = send_command_and_receive_all_data(connection_socket, command)
    if not data:
        break
    print(data.decode())

connection_socket.close()