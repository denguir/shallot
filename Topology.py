import random

class Topology(object):
    """Contains all the network topology loaded from topology.ini
    source : https://gist.github.com/econchick/4666413"""
    def __init__(self):
        self.nodes = set()
        self.edges = dict()
        self.costs = dict()

    def build(self, file):
        i_relay, i_topo = 0, 0
        with open(file, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            line = line.join(line.splitlines())
            if line == '[relays]':
                i_rel = i
            elif line == '[topology]':
                i_topo = i

        for i, line in enumerate(lines):
            line = line.join(line.splitlines())
            if i > i_rel and i < i_topo and line:
                ip, port = line.split(' ')
                self.nodes.add(ip)
            elif i > i_topo and line:
                ips = line.split(' ')
                self.edges[ips[0]] = ips[1:]

        self.random_cost()

    def random_cost(self):
        for edge in self.edges:
            for i in range(len(self.edges[edge])):
                if (edge, self.edges[edge][i]) not in self.costs and \
                (self.edges[edge][i], edge) not in self.costs:
                    self.costs[edge,self.edges[edge][i]]=random.randint(1,16)
                else:
                    self.costs[edge,self.edges[edge][i]] = self.costs[self.edges[edge][i],edge]


    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        if from_node != to_node:
            self.edges[from_node].append(to_node)
            self.edges[to_node].append(from_node)
            self.costs[(from_node, to_node)] = distance
        else:
            print("Adding edge failed:")
            print("<from_node> must be different from <to_node>")


if __name__ == '__main__':
    topo = Topology()
    topo.build('config/topology.ini')
    print(topo.nodes)
    print(topo.edges)
    print(topo.costs)
