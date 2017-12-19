import math

def dijkstra(topology, source):
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
