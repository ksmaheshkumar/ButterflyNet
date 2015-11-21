import socket
import ssl
import struct

# Open a new SSL socket
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s = ssl.wrap_socket(s)

s.connect(("127.0.0.1", 8001))

while True:
    to_send = input("> ")
    to_send_pak = struct.pack("!2shhh{}s".format(len(to_send)), "BF".encode(), 1, 0, len(to_send), to_send.encode())

    s.write(to_send_pak)
    data = s.recv(size).decode()
    print(data)


s.close()
