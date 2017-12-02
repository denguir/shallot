from Key import Key

class Receiver(Host):
    """docstring for Receiver."""
    def __init__(self, ip_addr):
        super(Receiver, self).__init__()
        self.ip_addr = ip_addr
        self.keys = {}

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

    def decrypt(self, key_id, message):
        '''Decrypt the message enc using the AES algorithm'''
        return self.keys[key_id].cipher.decrypt(message)

    def decrypt_shallot(self, key_id, shallot):
        return self.decrypt(key_id, shallot)
