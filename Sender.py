import random
from Topology import Topology
from Relay import Relay
from Receiver import Receiver
from Key import Key

class Sender(object):
    """docstring for Sender."""
    def __init__(self, ip_addr):
        super(Sender, self).__init__()
        self.ip_addr = ip_addr
        self.route = []
        self.p = 2**1024
        self.g = 2
        self.keys = {}

    def find_route(self, topology):
        '''
        Apply Dijkstra algorithm to find the route between Sender and Reicever
        https://gist.github.com/econchick/4666413
        '''
        visited = {self.ip_addr: 0}
        path = {}
        nodes = set(topology.nodes)

        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node

            if min_node is None:
                break

            nodes.remove(min_node)
            current_weight = visited[min_node]

            for edge in topology.edges[min_node]:
                weight = current_weight + topology.costs[(min_node, edge)]
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node

        return visited, path


    def init_keys(self, conn):
        '''Apply Diffie-Hellmann to initialize key with all the routed relays'''
        secretnumber=random.randint(1,p)
        init_msg=(g**secretnumber)%p
        conn.send(init_msg)
        secretkey=conn.rcv(buffer_size)

    def encrypt(self, msg):
        '''Build the shallot according to the keys generated in init_keys'''
        pass

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


if __name__ == '__main__':
    # topo = Topology()
    # topo.build('config/topology.ini')

    # sender = Sender('172.16.1.1')
    # visted, path = sender.find_route(topo)
    # print(visted)
    # print(path)


    '''TEST Key init between Alice-Bob and Alice-relay1
    Note: IP and Port are not yet implemented'''
    Alice = Sender('')
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
    