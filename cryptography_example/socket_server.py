import socket, sys
from threading import Thread
from socket_client import Client
import time

HOST = '127.0.0.1'
PORT = 50000
NUM_CLIENTS = 10

#private decomposition of n
p = 10
q = 17
#public_key
n = p*q # which is 170
e = 5

def private_key(p,q,e):
    n = p*q
    phi = (p-1)*(q-1)
    c,d,dd = euclide(e,phi) # pgcd + coeff Bezout
    return (d % phi) # d = inverse de e % phi

def euclide(a,b):
    x = 1 ; xx = 0
    y = 0 ; yy = 1

    while b != 0:
        q = a//b
        a, b = b, a%b
        xx, x = x-q*xx, xx
        yy, y = y-q*yy, yy

    return (a,x,y)

def rsa_decryption(x,n,d):
    return pow(x,d,n)

class Listener(Thread):
	def __init__(self, conn, addr):
		super(Listener, self).__init__()
		self.conn = conn
		self.addr = addr
		self.dataset = []
		self.running = True

	def synchronize(self):
		print('Synchronizing ...')
		synchronized = False
		synch_msg = 'OK'
		self.conn.send(synch_msg.encode('ascii'))
		response = self.conn.recv(1024).decode('ascii')
		if response == synch_msg:
			print('Synchronization succeded')
			synchronized = True
		else:
			print('Synchronization failed')
		return synchronized

	def decrypt(self, msg):
		decrypted_msg = ''
		d = private_key(p,q,e)
		for letter in msg:
			x = ord(letter)
			x_decrypted = rsa_decryption(x,n,d)
			decrypted_msg += chr(x_decrypted)
		return decrypted_msg

	def run(self):
		synchronized = self.synchronize()
		if synchronized:
			while self.running:
				# receiving data from clients
				crypted_data = self.conn.recv(1024)
				print('receiving crypted data: ', crypted_data)
				data = self.decrypt(crypted_data)
				print('decrypted data: ', data )
				self.dataset.append(data)
				time.sleep(2)
		else:
			self.stop()

	def stop(self):
		self.running = False
		self.conn.close()
		print('Client %s disconnected from port %s' % (self.addr[0], self.addr[1]))

if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind((HOST, PORT))
	except socket.error:
		print('Connection to socket failed')
		print('Exiting the process ...')
		sys.exit(1)

	except KeyboardInterrupt:
		print('Connection aborted by user')
		sys.exit(1)

	else:
		print('Server ready to receive connections ...')
		s.listen(NUM_CLIENTS)

		while True:
			try:
				conn, addr = s.accept()
				print("Client %s connected, on port %s" % (addr[0], addr[1]))
				listener = Listener(conn, addr)
				listener.start()
			except KeyboardInterrupt:
				print('Connection aborted by user')
				listener.stop()
				s.close()
				sys.exit(1)
