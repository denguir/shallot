#!/usr/bin/env python
 
'''Run PC2 in one terminal'''

import socket

IP = '127.0.0.7' # IP of the PC2
PORT = 5007 # PORT of the PC2

IP_SERVER = '127.0.0.10' # IP of the server
PORT_SERVER = 5005 # PORT of the server

BUFFER_SIZE = 1024
MESSAGE = str.encode("Hello world from PC2!")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.connect((IP_SERVER, PORT_SERVER))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
 
print("received data:", data)