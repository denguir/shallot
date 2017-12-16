from Key import Key
from Host import Host

class Receiver(Host):
    """docstring for Receiver."""
    def __init__(self, config_file):
        super(Receiver, self).__init__(config_file)
        self.KeyID_key = {}
        self.listen()

    def generate_key_from_sender(self, ip_sender, port_sender, key_id, public_key_sender):
        '''1) Generate a public key with the key ID specified by the sender
           2) Send the public key to the sender
           3) Generate shared key between the sender and the replier.'''

        new_key = Key(key_id)
        self.KeyID_key.update({key_id:new_key})
        self.send_key_reply(ip_sender, port_sender, new_key.get_key_id(), new_key.get_public_key())
        new_key.generate_shared_key(public_key_sender)

    def send_key_reply(self, ip_address, port, key_id, public_key):
        version = '0001'
        msg_type = '0001'
        msg_empty_space = '00000000'

        body = key_id + '{:01024b}'.format(public_key)

        msg_length = '{:016b}'.format(len(body))
        header = version + msg_type + msg_empty_space + msg_length
        self.send(header + body, ip_address,port)

    def decrypt_shallot(self, key_id, shallot):
        '''Decrypt the message enc using the AES algorithm'''
        return self.keys[key_id].cipher.decrypt(shallot)

    def key_reply(self):
        self.buffer.get()

    def on_data(self, data, conn):
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
        ip_origin,port_origin=conn.getsockname()
        data = str(data)
        version=data[0:4]
        msg_type=data[4:8]
        msg_length=data[16:32]
        if msg_type == '0000':
            # MSG TYPE = KEY_INIT
            self.generate_key_from_sender(ip_origin,port_origin, data)
            print('KEY_INIT')
        elif msg_type == '0001':
            # MSG TYPE = KEY_REPLY
            self.send("ACK", ip_origin, port_origin)
            print('KEY_REPLY')
        elif msg_type == '0010':
            # MSG TYPE = MESSAGE_RELAY
            self.decrypt_shallot(data)
            print('MESSAGE_RELAY')
        elif msg_type == '0011':
            # MSG TYPE = ERROR
            self.send('ACK')
            print('ERROR')
        else:
            print('AUCUN')
