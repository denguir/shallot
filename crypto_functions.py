from Key import Key

def generate_and_send_new_key(self, ip_adress, port):
	'''1) Generate a Key object in which will be stored a unique Key ID and a public key.
	   2) Send the key ID and the public key to the other entities'''
	key_id = self.generate_key_id()
	new_key = Key(key_id)
	self.keys.update({key_id:new_key})
	self.send_public_key(ip_adress, port, new_key.get_key_id(), new_key.get_public_key())

def generate_key_id(self):
	'''Generate the unique key ID.'''
	key_id = len(keys)+1
	return key_id

def send_public_key(self, ip_adress, port, key_id, public_key):
	pass

def generate_key_from_replier(self, key_id, public_key):
	'''Generate the shared key between the sender and the replier.'''
	keys[key_id].generate_shared_key(public_key)



def generate_key_from_sender(self, key_id, public_key):
	'''1) Generate a public key with the key ID specified by the sender
	   2) Send the public key to the sender
	   3) Generate shared key between the sender and the replier.'''

	new_key = Key(key_id)
	self.send_public_key(ip_adress, port, new_key.get_key_id(), new_key.get_public_key())
	new_key.generate_shared_key(public_key)

def send_public_key(self, ip_adress, port, key_id, public_key):
	pass


Alice.generate_and_send_new_key(ip_adress, port)

key_id = 2
alice_key = Key(2)
bob_key = Key(2)

bob_key.generate_shared_key(alice_key.get_public_key())
print(bob_key.get_shared_key())

alice_key.generate_shared_key(bob_key.get_public_key())
print(alice_key.get_shared_key())