
class Topology(object):
    """Contains all the network topology loaded from topology.ini"""
    def __init__(self):
        self.nodes = set()
        self.edges = dict()
        self.distances = dict()

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

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance


if __name__ == '__main__':
    topo = Topology()
    topo.build('config/topology.ini')
    print(topo.nodes)
    print(topo.edges)
