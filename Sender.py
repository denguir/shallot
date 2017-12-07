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
    def __init__(self, config_file):
        super(Sender, self).__init__(config_file)
        self.route = []
        self.KeyID_key = {}
        self.IP_KeyID = {}

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

    def initialyze_keys(self,path):
        for i in range(1,len(path)):
            self.generate_and_send_new_key(path[i],'')

    def generate_and_send_new_key(self, ip_address, port):
        '''1) Generate a Key object in which will be stored a unique Key ID and a public key.
           2) Send the key ID and the public key to the other entities'''
        key_id = self.generate_key_id()
        new_key = Key(key_id)
        self.KeyID_key.update({key_id:new_key})
        self.IP_KeyID.update({ip_address:key_id})
        self.send_public_key(ip_address, port, new_key.get_key_id(), new_key.get_public_key())

    def generate_key_id(self):
        '''Generate the unique key ID.'''
        key_id = len(self.KeyID_key)+1
        return key_id

    def send_public_key(self, ip_address, port, key_id, public_key):
        pass

    def generate_key_from_replier(self, key_id, public_key_replier):
        '''Generate the shared key between the sender and the replier.'''
        self.KeyID_key[key_id].generate_shared_key(public_key_replier)

    def encrypt(self, key_id, message):
        '''Encrypt the message raw using the AES algorithm'''
        return self.KeyID_key[key_id].cipher.encrypt(message)

    def decrypt(self, key_id, message):
        '''Decrypt the message enc using the AES algorithm'''
        return self.KeyID_key[key_id].cipher.decrypt(message)

    def build_shallot(self, path, message):
        '''Build the shallot based on the order of the keys ID'''
        shallot = message
        path.append(path[-1])
        path.reverse
        for i in range(1,len(path)-1):
            IP = path[i]
            key_ID = self.IP_KeyID[IP]

            IP_next = path[i-1]
            binary_IP_next = self.ip2bin(IP_next)
            shallot = self.encrypt(key_ID,binary_IP_next+shallot)

            keyID_in_bits = self.dec_to_32bits(key_ID)
            shallot = keyID_in_bits + shallot
        return shallot

    def decrypt_shallot(self, keysID_order, message):
        '''The Sender can decrypt the entire shallot by using this function'''
        shallot = message
        for key_id in keysID_order:
            shallot = self.decrypt(key_id, shallot)
        return shallot

    def ip2bin(self, ip):
        octets = map(int, ip.split('/')[0].split('.')) # '1.2.3.4'=>[1, 2, 3, 4]
        binary = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*octets)
        range = int(ip.split('/')[1]) if '/' in ip else None
        return binary[:range] if range else binary

    def dec_to_32bits(self, integer):
        return '{:032b}'.format(integer)

if __name__ == '__main__':
    topo = Topology()
    topo.build('config/topology.ini')

    '''TEST Key init between Alice-Bob and Alice-relay1
    Note: IP and Port are not yet implemented'''
    Alice = Sender('config/host_R1.ini')
    Bob = Receiver('config/host_R4.ini')
    relay1 = Relay('config/host_R2.ini')
    relay2 = Relay('config/host_R3.ini')

    sp = Alice.shortest_path(topo, '172.16.4.2')


    Alice.initialyze_keys(sp)
    print(sp)

    '''Key negotiation with Bob'''
    Bob_KeyID = Alice.IP_KeyID[Bob.ip_addr]
    relay1_KeyID = Alice.IP_KeyID[relay1.ip_addr]
    relay2_KeyID = Alice.IP_KeyID[relay2.ip_addr]
    Bob.generate_key_from_sender('','',Bob_KeyID, Alice.KeyID_key[Bob_KeyID].get_public_key())
    Alice.generate_key_from_replier(Bob_KeyID,Bob.KeyID_key[Alice.IP_KeyID[Bob.ip_addr]].get_public_key())

    '''Key negotiation with relay1'''
    relay1.generate_key_from_sender('','',relay1_KeyID, Alice.KeyID_key[relay1_KeyID].get_public_key())
    Alice.generate_key_from_replier(relay1_KeyID,relay1.KeyID_key[relay1_KeyID].get_public_key())

    '''Key negotiation with relay2'''
    relay2.generate_key_from_sender('','',relay2_KeyID, Alice.KeyID_key[relay2_KeyID].get_public_key())
    Alice.generate_key_from_replier(relay2_KeyID,relay2.KeyID_key[relay2_KeyID].get_public_key())
    

    # print("Alice-Bob key:")
    # print(Alice.KeyID_key[Alice.IP_KeyID[Bob.ip_addr]].get_shared_key())
    # print(Bob.KeyID_key[Alice.IP_KeyID[Bob.ip_addr]].get_shared_key())
    # print("\n")

    # print("Alice-relay1 key:")
    # print(Alice.KeyID_key[Alice.IP_KeyID[relay1.ip_addr]].get_shared_key())
    # print(relay1.KeyID_key[Alice.IP_KeyID[relay1.ip_addr]].get_shared_key())
    # print('\n')

    # print("Alice-relay2 key:")
    # print(Alice.KeyID_key[Alice.IP_KeyID[relay2.ip_addr]].get_shared_key())
    # print(relay2.KeyID_key[Alice.IP_KeyID[relay2.ip_addr]].get_shared_key())
    # print('\n')

    Alice.build_shallot(sp,'caca')
    