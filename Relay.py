from Key import Key
from Host import Host

class Relay(Host):
    """docstring for Relay."""
    def __init__(self, config_file):
        super(Relay, self).__init__(config_file)
        self.KeyID_key = {}
        self.listen()

    def generate_key_from_sender(self, ip_sender, port_sender,item):
        '''1) Generate a public key with the key ID specified by the sender
           2) Send the public key to the sender
           3) Generate shared key between the sender and the replier.'''

        key_id=item[32:64]
        print(key_id)
        public_key_sender=item[64:]
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

    def send_public_key(self, ip_address, port, key_id, public_key):
        self.send(msg, ip_address, port)

    def decrypt_shallot(self,item):
        '''Decrypt the message enc using the AES algorithm'''
        word=""
        counter=32
        while counter!=64:
       	    word+=item[counter]
            counter+=1
        key_id=int(word,2)
        message_to_send=self.KeyID_key[key_id].cipher.decrypt(item[counter :])
        ip_next_hop=""
        for i in range(4):
            ip_next_hop+=string(int(message_to_send[counter+8*i:counter+8*(i+1)]))
            ip_next_hop+="."
        port=string(int(message_to_send[counter+32:counter+64],2))
        nxt_msg=message_to_send[counter+64:]
        self.send(nxt_msg,ip_next_hop,port)
        return self.keys[key_id].cipher.decrypt(shallot)

    def on_data(self, data,conn):
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
        version=data[0:4]
        msg_type=data[4:8]
        msg_length=data[16:32]
        if msg_type=='0000':
            generate_key_from_sender(ip_origin,port_origin,item)
        elif msg_type=='0001':
            self.send("ACK",ip_origin,port_origin)
        elif msg_type=='0010':
            self.decrypt(item)
        elif msg_type=='0011':
            self.send('ACK')






