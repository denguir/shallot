import configparser
import random
# topology source code : https://gist.github.com/econchick/4666413

class Topology(object):
    """Contains all the network topology loaded from topology.ini
        nodes is a set of every entity of the network
        each entity is a tuple providing its ip and port : (ip: str, port: int)
        edges depicts the links existing between each node
        costs attributes a random distance between each links of edges
        Use the build method to construct the topology from topology.ini
    """
    def __init__(self):
        self.nodes = set()
        self.edges = dict()
        self.costs = dict()
        self.ip_to_port = dict()

    def build(self, file):
        '''build the topology from a given .ini file'''
        config = configparser.ConfigParser()
        config.read(file)
        for relay in config['relays']:
            ip, port = config['relays'][relay].split(' ')
            self.nodes.add((ip,int(port)))
            self.ip_to_port[ip] = int(port)

        for link in config['topology']:
            ips = config['topology'][link].split(' ')
            self.edges[(ips[0], self.ip_to_port[ips[0]])] = list(zip(ips[1:], [self.ip_to_port[ip] for ip in ips[1:]]))

        self.random_cost()

    def random_cost(self):
        '''computes a random cost for each link of the topology'''
        for edge in self.edges:
            for i in range(len(self.edges[edge])):
                if (edge, self.edges[edge][i]) not in self.costs and \
                (self.edges[edge][i], edge) not in self.costs:
                    self.costs[edge,self.edges[edge][i]]=random.randint(1,16)
                else:
                    self.costs[edge,self.edges[edge][i]] = self.costs[self.edges[edge][i],edge]

    def add_node(self, value):
        '''allows the user to manually modify the topology by adding new nodes'''
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        '''allows the user to manually modify the topology by adding new edges'''
        if from_node != to_node:
            self.edges[from_node].append(to_node)
            self.edges[to_node].append(from_node)
            self.costs[(from_node, to_node)] = distance
        else:
            print("Adding edge failed:")
            print("<from_node> must be different from <to_node>")
