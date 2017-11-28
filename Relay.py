from Key import Key

class Relay(object):
    """docstring for Relay."""
    def __init__(self, ip_addr, port):
        super(Relay, self).__init__()
        self.ip_addr = ip_addr
        self.port = port
        self.keys = {}

    def decrypt(self, encrypted_msg):
        ''' decrypt the message sent by previous entity'''
        pass

    def send(self, msg, ip_dest):
        '''Send this message to the destination'''
        pass

    def generate_key_from_sender(self, ip_sender, port_sender, key_id, public_key_sender):
        '''1) Generate a public key with the key ID specified by the sender
           2) Send the public key to the sender
           3) Generate shared key between the sender and the replier.'''

        new_key = Key(key_id)
        self.keys.update({key_id:new_key})
        self.send_public_key(ip_sender, port_sender, new_key.get_key_id(), new_key.get_public_key())
        new_key.generate_shared_key(public_key_sender)

    def send_public_key(self, ip_adress, port, key_id, public_key):
        pass

    def encrypt(self, key_id, message):
        '''Encrypt the message raw using the AES algorithm'''
        return self.keys[key_id].cipher.encrypt(message)

    def decrypt(self, key_id, message):
        '''Decrypt the message enc using the AES algorithm'''
        return self.keys[key_id].cipher.decrypt(message)