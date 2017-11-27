import random
import math
from Topology import Topology

class Sender(object):
    """docstring for Sender."""
    def __init__(self, ip_addr):
        super(Sender, self).__init__()
        self.ip_addr = ip_addr
        self.route = []
        self.p = 2**1024
        self.g = 2

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

    def send(self, encrypted_msg, ip_dest):
        '''Send encrypted message to the destination'''
        pass

if __name__ == '__main__':
    topo = Topology()
    topo.build('config/topology.ini')

    sender = Sender('172.16.1.1')
    path = sender.shortest_path(topo, '172.16.3.2')
    print(path)
