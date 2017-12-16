#!/usr/bin/env python

# Example found here: https://wiki.python.org/moin/TcpCommunication

'''Run PC1 in one terminal'''

import socket

IP = '127.0.0.5' # IP of the PC1
PORT = 5000 # PORT of the PC1

IP_SERVER = '127.0.0.10' # IP of the server
PORT_SERVER = 5005 # PORT of the server

BUFFER_SIZE = 1024
MESSAGE = str.encode("Hello world from PC1!")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.connect((IP_SERVER, PORT_SERVER))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
print(s.getsockname()[0], s.getsockname()[1])
s.close()

print("received data:", data)
