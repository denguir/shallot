
# random cost test
edges = {'a':['b'], 'b':['a']}
costs = {('a','b'):4}
for edge in edges:
    for i in range(len(edges[edge])):
        if (edge,edges[edge][i]) not in costs and (edges[edge][i], edge) not in costs:
            print('not here')
        else:
            print('here')
