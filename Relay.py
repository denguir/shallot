from utils.digit_conversion import *
from Key import Key
from Host import Host

class Relay(Host):
    """docstring for Relay."""
    def __init__(self, config_file):
        super(Relay, self).__init__(config_file)
        self.KeyID_key = {}
        self.listen()
        self.write()

    def generate_key_from_sender(self, conn_with_sender, message):
        '''1) Generate a public key with the key ID specified by the sender
           2) Send the public key to the sender
           3) Generate shared key between the sender and the replier.'''

        key_id = message[32:64]
        g = int(message[64:68],2)
        p = int(message[68:1092],2)
        public_key_sender_bin = message[1092:2116]
        public_key_sender = int(public_key_sender_bin,2)
        new_key = Key(key_id)
        self.KeyID_key.update({key_id:new_key})
        self.send_key_reply(conn_with_sender, new_key.get_key_id(), new_key.get_public_key())
        new_key.generate_shared_key(public_key_sender)

    def send_key_reply(self, conn_with_sender, key_id, public_key):
        version = '0001'
        msg_type = '0001'
        msg_empty_space = '00000000'

        body = key_id + dec_to_1024bits(public_key)

        msg_length = self.compute_msg_length(body)

        header = version + msg_type + msg_empty_space + msg_length
        conn_with_sender.send(str.encode(header+body))
        conn_with_sender.close()

    def send_message_relay(self, message_relay, ip_address, port):
        version = '0001'
        msg_type = '0010'
        msg_empty_space = '00000000'

        msg_length = self.compute_msg_length(message_relay)

        header = version + msg_type + msg_empty_space + msg_length
        self.send(header + message_relay, ip_address,port)

    def decrypt_shallot(self,item):
        '''Decrypt the message enc using the AES algorithm'''
        key_id=item[32:64]
        #print(key_id)
        #print(self.KeyID_key)
        payload_deciphered=self.KeyID_key[key_id].cipher.decrypt(item[64:])

        ip_next_hop_bin=payload_deciphered[0:32]
        ip_next_hop = ip2dec(ip_next_hop_bin)

        port_next_hop_bin=payload_deciphered[32:64]
        port_next_hop = int(port_next_hop_bin,2)

        nxt_msg = payload_deciphered[64:]

        print(nxt_msg)
        self.send_message_relay(nxt_msg,ip_next_hop,port_next_hop)

    def on_data(self, data, conn):
        data = str(data)[2:]
        version=data[0:4]
        msg_type=data[4:8]
        msg_length=data[16:32]
        if msg_type == '0000':
            # MSG TYPE = KEY_INIT
            print('KEY_INIT')
            self.generate_key_from_sender(conn, data)
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
