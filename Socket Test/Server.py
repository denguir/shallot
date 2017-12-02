#!/usr/bin/env python

# Example found here: https://wiki.python.org/moin/TcpCommunication

'''Run Server in one terminal'''

import socket

IP = '127.0.0.10' # IP of the server
PORT = 5005 # PORT of the server
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(1)

# conn, addr = s.accept()
# print('Connection address:', addr)
# while 1:
#     data = conn.recv(BUFFER_SIZE)
#     if not data: break
#     print("received data:", data)
#     conn.send(data)  # echo
# conn.close()

try:
    while True:
        conn, addr = s.accept()
        print('Connection address:', addr)

        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print("received data:", data)
        conn.send(data)  # echo
        conn.close()
except KeyboardInterrupt:
    print("\n Server stopped")