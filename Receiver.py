from Key import Key
from Host import Host

class Receiver(Host):
    """docstring for Receiver."""
    def __init__(self, config_file):
        super(Receiver, self).__init__(config_file)
        self.KeyID_key = {}

    def generate_key_from_sender(self, ip_sender, port_sender, key_id, public_key_sender):
        '''1) Generate a public key with the key ID specified by the sender
           2) Send the public key to the sender
           3) Generate shared key between the sender and the replier.'''

        new_key = Key(key_id)
        self.KeyID_key.update({key_id:new_key})
        self.send_public_key(ip_sender, port_sender, new_key.get_key_id(), new_key.get_public_key())
        new_key.generate_shared_key(public_key_sender)

    def send_public_key(self, ip_adress, port, key_id, public_key):
        pass

    def decrypt_shallot(self, key_id, shallot):
        '''Decrypt the message enc using the AES algorithm'''
        return self.keys[key_id].cipher.decrypt(shallot)