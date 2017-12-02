import random
import math
import socket
from Topology import Topology
from Relay import Relay
from Receiver import Receiver
from Host import Host
from Key import Key

class Sender(Host):
    """docstring for Sender."""
    def __init__(self, ip_addr, port):
        super(Sender, self).__init__(ip_addr, port)
        self.route = []
        self.p = 2**1024
        self.g = 2
        self.keys = {}

    def dijkstra(self, topology, source):
        '''
        Apply Dijkstra algorithm to find the route between Sender and Reicever
        https://gist.github.com/econchick/4666413
        http://alexhwoods.com/dijkstra/
        '''
        S = set()
        weights = dict.fromkeys(list(topology.nodes), math.inf)
        previous_path = dict.fromkeys(list(topology.nodes), None)

        weights[source] = 0
        while S != topology.nodes:
            v = min((set(weights.keys()) - S), key=weights.get)

            for neighbor in set(topology.edges[v]) - S:
                new_path = weights[v] + topology.costs[v,neighbor]

                if new_path < weights[neighbor]:
                    weights[neighbor] = new_path
                    previous_path[neighbor] = v
            S.add(v)
        return (weights, previous_path)

    def shortest_path(self, topology, destination):
        if destination not in topology.nodes:
            print('Shortest path research failed:')
            print('{} not in network'.format(destination))
        else:
            weigths, previous_path = self.dijkstra(topology, self.ip_addr)
            path = []
            node = destination
            while node is not None:
                path.append(node)
                node = previous_path[node]
            path.reverse()
            return path

    def init_keys(self, conn):
        '''Apply Diffie-Hellmann to initialize key with all the routed relays'''
        secretnumber=random.randint(1,p)
        init_msg=(g**secretnumber)%p
        conn.send(init_msg)
        secretkey=conn.rcv(buffer_size)

    def send(self, encrypted_msg, ip_dest):
        '''Send encrypted message to the destination'''
        pass

    def generate_and_send_new_key(self, ip_adress, port):
        '''1) Generate a Key object in which will be stored a unique Key ID and a public key.
           2) Send the key ID and the public key to the other entities'''
        key_id = self.generate_key_id()
        new_key = Key(key_id)
        self.keys.update({key_id:new_key})
        self.send_public_key(ip_adress, port, new_key.get_key_id(), new_key.get_public_key())

    def generate_key_id(self):
        '''Generate the unique key ID.'''
        key_id = len(self.keys)+1
        return key_id

    def send_public_key(self, ip_adress, port, key_id, public_key):
        pass

    def generate_key_from_replier(self, key_id, public_key_replier):
        '''Generate the shared key between the sender and the replier.'''
        self.keys[key_id].generate_shared_key(public_key_replier)

    def convert_str_to_hex(self, hex_in_str):
        hex_str = hex_in_str
        hex_int = int(hex_str, 16)
        new_int = hex_int + 0x200
        return (hex(new_int)[2:])

    def encrypt(self, key_id, message):
        '''Encrypt the message raw using the AES algorithm'''
        return self.keys[key_id].cipher.encrypt(message)

    def decrypt(self, key_id, message):
        '''Decrypt the message enc using the AES algorithm'''
        return self.keys[key_id].cipher.decrypt(message)

    def build_shallot(self, keysID_order, message):
        '''Build the shallot based on the order of the keys ID'''
        shallot = message
        for key_id in keysID_order[::-1]:
            shallot = self.encrypt(key_id, shallot)
        return shallot

    def decrypt_shallot(self, keysID_order, message):
        '''The Sender can decrypt the entire shallot by using this function'''
        shallot = message
        for key_id in keysID_order:
            shallot = self.decrypt(key_id, shallot)
        return shallot


if __name__ == '__main__':
    topo = Topology()
    topo.build('config/topology.ini')

    '''TEST Key init between Alice-Bob and Alice-relay1
    Note: IP and Port are not yet implemented'''
    Alice = Sender('172.16.1.1', 4000)
    Bob = Receiver('')
    relay1 = Relay('','')
    relay2 = Relay('','')


    '''Key negotiation with Bob'''
    Alice.generate_and_send_new_key('','')
    Bob.generate_key_from_sender('','',1, Alice.keys[1].get_public_key())
    Alice.generate_key_from_replier(1,Bob.keys[1].get_public_key())

    '''Key negotiation with relay1'''
    Alice.generate_and_send_new_key('','')
    relay1.generate_key_from_sender('','',2, Alice.keys[2].get_public_key())
    Alice.generate_key_from_replier(2,relay1.keys[2].get_public_key())

    '''Key negotiation with relay2'''
    Alice.generate_and_send_new_key('','')
    relay2.generate_key_from_sender('','',3, Alice.keys[3].get_public_key())
    Alice.generate_key_from_replier(3,relay2.keys[3].get_public_key())


    print("Alice-Bob key:")
    print(Alice.keys[1].get_shared_key())
    print(Bob.keys[1].get_shared_key())
    print("\n")

    print("Alice-relay1 key:")
    print(Alice.keys[2].get_shared_key())
    print(relay1.keys[2].get_shared_key())
    print('\n')

    print("Alice-relay2 key:")
    print(Alice.keys[3].get_shared_key())
    print(relay2.keys[3].get_shared_key())
    print('\n')


    print("\n")
    print("shortest path:")
    path = Alice.shortest_path(topo, '172.16.4.2')
    print(path, "\n")

"""
    encrypted_Bob = Alice.encrypt(1,'Hello Bob')
    decrypted_Bob = Bob.decrypt(1,encrypted_Bob)
    print('Encrypted: %s' % encrypted_Bob)
    print('Decrypted: %s' % decrypted_Bob,"\n")

    encrypted_relay1 = Alice.encrypt(2,'Hello relay1')
    decrypted_relay1 = relay1.decrypt(2,encrypted_relay1)
    print('Encrypted: %s' % encrypted_relay1)
    print('Decrypted: %s' % decrypted_relay1,"\n")


    '''Encryption of a message 3 times'''
    msg = 'Allah akbar!'
    print('Message to encrypt 3 times: %s' % msg)
    encrypted1 = Alice.encrypt(1,msg) # encrypted with Alice-Bob key
    print('Encrypted 1 time: %s' % encrypted1)
    encrypted2 = Alice.encrypt(2,encrypted1) # encrypted with Alice-relay1 key
    print('Encrypted 2 times: %s' % encrypted2)
    encrypted3 = Alice.encrypt(3,encrypted2) # encrypted with Alice-relay2 key
    print('Encrypted 3 times: %s' % encrypted3,"\n")

    decrypted1 = relay2.decrypt(3,encrypted3) # decrypted with Alice-relay2 key
    print('Decrypted 1 time: %s' % decrypted1)
    decrypted2 = relay1.decrypt(2,decrypted1) # decrypted with Alice-relay1 key
    print('Decrypted 2 time: %s' % decrypted2)
    decrypted3 = Bob.decrypt(1,decrypted2) # decrypted with Alice-Bob key
    print('Decrypted 3 times: %s' % decrypted3,'\n')


    '''Shallot building with decryption'''
    msg2 = 'Ta mere la reine des putes'
    keysID_order = [3,2,1]
    shallot = Alice.build_shallot(keysID_order,msg2)
    print('Encrypted shallot: %s' % shallot)
    msg2_recover = Alice.decrypt_shallot(keysID_order,shallot)
    print('Decrypted shallot: %s' % msg2_recover)
"""
