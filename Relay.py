from Key import Key
from Host import Host

class Relay(Host):
    """docstring for Relay."""
    def __init__(self, ip_addr, port):
        super(Relay, self).__init__(ip_addr, port)
        self.keys = {}

    def generate_key_from_sender(self, sender, key_id, public_key_sender):
        '''1) Generate a public key with the key ID specified by the sender
           2) Send the public key to the sender
           3) Generate shared key between the sender and the replier.'''

        new_key = Key(key_id)
        self.keys.update({key_id:new_key})
        self.send_public_key(sender.ip_addr, sender.port, new_key.get_key_id(), new_key.get_public_key())
        new_key.generate_shared_key(public_key_sender)

    def send_public_key(self, ip_adress, port, key_id, public_key):
        pass

    def decrypt(self, key_id, message):
        '''Decrypt the message enc using the AES algorithm'''
        return self.keys[key_id].cipher.decrypt(message)

    def decrypt_shallot(self, key_id, shallot):
        return self.decrypt(key_id, shallot)
