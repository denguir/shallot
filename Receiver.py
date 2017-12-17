from Key import Key
from Host import Host

class Receiver(Host):
    """docstring for Receiver."""
    def __init__(self, config_file):
        super(Receiver, self).__init__(config_file)
        self.KeyID_key = {}
        self.listen()

    def generate_key_from_sender(self, ip_sender, port_sender, message):
        '''1) Generate a public key with the key ID specified by the sender
           2) Send the public key to the sender
           3) Generate shared key between the sender and the replier.'''

        key_id = message[32:64]
        public_key_sender_bin = message[1092:2116]
        public_key_sender = int(public_key_sender_bin,2)
        new_key = Key(key_id)
        self.KeyID_key.update({key_id:new_key})
        self.send_key_reply(ip_sender, port_sender, new_key.get_key_id(), new_key.get_public_key())
        new_key.generate_shared_key(public_key_sender)

    def send_key_reply(self, ip_address, port, key_id, public_key):
        version = '0001'
        msg_type = '0001'
        msg_empty_space = '00000000'

        body = key_id + '{:01024b}'.format(public_key)

        msg_length = self.compute_msg_length(body)

        header = version + msg_type + msg_empty_space + msg_length
        self.send(header + body, ip_address,port)

    def compute_msg_length(self, body):
        optional_padding1 = (len(body)%8)*(' ')
        body += optional_padding1
        optional_padding2 = int((len(body)/8)%4)*('    ')
        body += optional_padding2
        return '{:016b}'.format(int(((len(body)/8)+4)/4))

    def decrypt_shallot(self,item):
        '''Decrypt the message enc using the AES algorithm'''
        key_id=item[32:64]
        #print(key_id)
        #print(self.KeyID_key)
        payload_deciphered=self.KeyID_key[key_id].cipher.decrypt(item[64:])
        ip_next_hop_bin=payload_deciphered[0:32]
        ip_next_hop = self.ip2dec(ip_next_hop_bin)
        if ip_next_hop == self.ip_addr:
        	nxt_msg = payload_deciphered[32:]
        	print('Message reçu par Bob:',nxt_msg)

    def ip2dec(self, ip_bin):
        ip_dec = str(int(ip_bin[0:8],2))+'.'+str(int(ip_bin[8:16],2))+'.'+str(int(ip_bin[16:24],2))+'.'+str(int(ip_bin[24:32],2))
        return ip_dec

    def key_reply(self):
        self.buffer.get()

    def on_data(self, data, conn):
        data = str(data)[2:]
        ip_origin,port_origin=conn.getsockname()
        version=data[0:4]
        msg_type=data[4:8]
        msg_length=data[16:32]
        if msg_type == '0000':
            # MSG TYPE = KEY_INIT
            # self.generate_key_from_sender(ip_origin,port_origin, data)
            print('KEY_INIT')
            self.generate_key_from_sender('127.16.1.1',9000, data)
        elif msg_type == '0010':
            # MSG TYPE = MESSAGE_RELAY
            print('MESSAGE_RELAY')            
            self.decrypt_shallot(data)
        elif msg_type == '0011':
            # MSG TYPE = ERROR
            print('ERROR')
            self.send('ACK')
        else:
            print(data)