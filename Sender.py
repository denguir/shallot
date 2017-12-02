import random
import math
import socket
from Topology import Topology
from Relay import Relay
from Receiver import Receiver
from Key import Key

class Sender(object):
    """docstring for Sender."""
    def __init__(self, ip_addr, port):
        super(Sender, self).__init__()
        self.ip_addr = ip_addr
        self.port = port
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

    def encrypt(self, msg):
        '''Build the shallot according to the keys generated in init_keys'''
        pass

    def send(self, encrypted_msg, network, relay):
        '''Send encrypted message to the destination'''
        path = self.shortest_path(network, relay.ip_addr)
        if path is not None:
            try:
                s = self.connect(relay.ip_addr, relay.port)
                s.send(encrypted_msg)
            except socket.error:
                print('Failed while sending message to %s' %(relay.ip_addr))


    def connect(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
        except socket.error:
            print('Connection failed')
        print('Connection success with %s on port %s' % (self.host,self.port))
        return s

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


if __name__ == '__main__':
    topo = Topology()
    topo.build('config/topology.ini')

    # sender = Sender('172.16.1.1')
    # visted, path = sender.find_route(topo)
    # print(visted)
    # print(path)


    '''TEST Key init between Alice-Bob and Alice-relay1
    Note: IP and Port are not yet implemented'''
    Alice = Sender('172.16.1.1')
    Bob = Receiver('')
    relay1 = Relay('','')

    Alice.generate_and_send_new_key('','')
    Bob.generate_key_from_sender('','',1, Alice.keys[1].get_public_key())
    Alice.generate_key_from_replier(1,Bob.keys[1].get_public_key())

    Alice.generate_and_send_new_key('','')
    relay1.generate_key_from_sender('','',2, Alice.keys[2].get_public_key())
    Alice.generate_key_from_replier(2,relay1.keys[2].get_public_key())

    print("Alice-Bob key:")
    print(Alice.keys[1].get_shared_key())
    print(Bob.keys[1].get_shared_key())

    print("\n")
    print("Alice-relay1 key:")
    print(Alice.keys[2].get_shared_key())
    print(relay1.keys[2].get_shared_key())

    print("\n")
    print("shortest path:")
    path = Alice.shortest_path(topo, '172.16.3.2')
    print(path)
