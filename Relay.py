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
        '''1) Generate a public key with the key ID specified and sent by the sender
           2) Send the public key and the associated key ID to the sender
           3) Generate shared key between the sender and the replier.'''

        key_id = message[32:64] # Extract Key ID from the message sent by the Sender
        g = int(message[64:68],2) # Extract g paramter from the message sent by the Sender
        p = int(message[68:1092],2) # Extract p parameter from the message sent by the Sender
        public_key_sender_bin = message[1092:2116] # Extract the public key from the message sent by the Sender
        public_key_sender = int(public_key_sender_bin,2) # Convert the public key from binary to decimal
        new_key = Key(key_id, g, p) # Generate a new key
        self.KeyID_key.update({key_id:new_key}) # update the dico with the link: Key ID - Object Key
        self.send_key_reply(conn_with_sender, new_key.get_key_id(), new_key.get_public_key()) # Send the public key of the Receiver and the associated Key ID to Sender
        new_key.generate_shared_key(public_key_sender) # Generate shared key with the public key of the Sender

    def send_key_reply(self, conn_with_sender, key_id, public_key):
        '''Send a KEY_REPLY message in the specified format for this project.'''
        version = '0001'
        msg_type = '0001'
        msg_empty_space = '00000000'

        body = key_id + dec_to_1024bits(public_key)

        msg_length, body_with_padding = self.compute_msg_length(body)

        header = version + msg_type + msg_empty_space + msg_length
        conn_with_sender.send(str.encode(header+body_with_padding))
        conn_with_sender.close()

    def send_message_relay(self, message_relay, ip_address, port):
        '''Send a MESSAGE_RELAY message in the specified format for this project.'''
        version = '0001'
        msg_type = '0010'
        msg_empty_space = '00000000'

        msg_length, message_relay_with_padding = self.compute_msg_length(message_relay)

        header = version + msg_type + msg_empty_space + msg_length
        self.send(header + message_relay_with_padding, ip_address,port)

    def decrypt_shallot(self,conn, item):
        '''Decrypt the message using the AES algorithm'''
        key_ID = item[32:64]
        if self.check_key_ID_exist(key_ID):
            payload_deciphered = self.KeyID_key[key_ID].cipher.decrypt(item[64:])

            ip_next_hop_bin = payload_deciphered[0:32]
            ip_next_hop = ip2dec(ip_next_hop_bin)

            port_next_hop_bin = payload_deciphered[32:64]
            port_next_hop = int(port_next_hop_bin,2)

            nxt_msg = payload_deciphered[64:]
            print(nxt_msg)

            self.send_message_relay(nxt_msg,ip_next_hop,port_next_hop)
        else:
            print('ERROR')
            print('INVALID_KEY_ID')
            self.send_error(conn, 1)

    def check_key_ID_exist(self, key_ID):
        '''Check if the Key ID is valid'''
        return key_ID in self.KeyID_key

    def on_data(self, data, conn):
        '''Execute the appropriate function based on the type of the received data'''
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
            self.decrypt_shallot(conn, data)
        elif msg_type == '0011':
            # MSG TYPE = ERROR
            print('ERROR')
            if int(data[32:48],2) == 0:
                print('INVALID_MESSAGE_FORMAT')
            elif int(data[32:48],2) == 1:
                print('INVALID_KEY_ID')
        else:
            print('ERROR')
            print('INVALID_MESSAGE_FORMAT')
            self.send_error(conn, 0)
            