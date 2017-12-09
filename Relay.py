from Key import Key
from Host import Host

class Relay(Host):
    """docstring for Relay."""
    def __init__(self, config_file):
        super(Relay, self).__init__(config_file)
        self.KeyID_key = {}
        self.listen()

    def generate_key_from_sender(self, ip_sender, port_sender, key_id, public_key_sender):
        '''1) Generate a public key with the key ID specified by the sender
           2) Send the public key to the sender
           3) Generate shared key between the sender and the replier.'''

        new_key = Key(key_id)
        self.KeyID_key.update({key_id:new_key})
        self.send_public_key(ip_sender, port_sender, new_key.get_key_id(), new_key.get_public_key())
        new_key.generate_shared_key(public_key_sender)

    def send_public_key(self, ip_address, port, key_id, public_key):
        self.send(msg, ip_address, port)


    def decrypt_shallot(self, key_id, shallot):
        '''Decrypt the message enc using the AES algorithm'''
        return self.keys[key_id].cipher.decrypt(shallot)

    def on_data(self, data, ip_origin, port_origin):
        """
        if data_type is KEY_INIT : apply generate_key_from_sender
        if data_type is KEY_REPLY : reply
        example:                if not self.buffer.empty():
                                    msg = self.buffer.get()
                                    key_id = msg[0:32]
                                    public_key = msg[32:]
        if data_type is MESSAGE_RELAY : send to next hop
        if data_type is ERROR :
        """
