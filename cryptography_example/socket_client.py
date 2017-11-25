import socket, sys, random, time
from threading import Thread

# IP SERVER
HOST = '127.0.0.1'
PORT = 50000

#message
msg = "Ceci est un message top secret"
# public_key
n = 170
e = 5

def rsa_encryption(m,n,e):
    return pow(m,e,n)

class Client(object):
	def __init__(self, host, port):
		super(Client, self).__init__()
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connected = True

	def connect(self):
		try:
			self.sock.connect((self.host,self.port))
		except socket.error:
			print('Connection failed')
			sys.exit()
		print('Connection success with %s on port %s' % (self.host,self.port))

	def disconnect(self):
		self.connected = False
		self.sock.close()

	def synchronize(self):
		synchronized = False
		sync_msg = self.sock.recv(1024).decode('ascii')
		if sync_msg.upper() == 'OK':
			self.sock.send(sync_msg.encode('ascii'))
			synchronized = True
			print('Synchronization succeded')
		else:
			print('Synchronization failed')
		return synchronized

	def encrypt(self, msg):
		encrypted_msg = ''
		for letter in msg:
			m = ord(letter)
			m_encrypted = rsa_encryption(m,n,e)
			encrypted_msg += chr(m_encrypted)
		return encrypted_msg

	def send(self, msg):
		encrypted_msg = self.encrypt(msg)
		self.sock.send(encrypted_msg)

if __name__ == '__main__':
	try:
		client = Client(HOST, PORT)
		client.connect()
		client.synchronize()
		time.sleep(2)
		client.send(msg)

	except KeyboardInterrupt:
		client.disconnect()
		print('Connection aborted by user')
		sys.exit
