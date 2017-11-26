import random
from Topology import Topology

class Sender(object):
    """docstring for Sender."""
    def __init__(self, ip_addr):
        super(Sender, self).__init__()
        self.ip_addr = ip_addr
        self.route = []
        self.p = 2**1024
        self.g = 2

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

if __name__ == '__main__':
    topo = Topology()
    topo.build('config/topology.ini')

    sender = Sender('172.16.1.1')
    visted, path = sender.find_route(topo)
    print(visted)
    print(path)
