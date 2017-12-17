from Topology import Topology
from Sender import Sender

if __name__ == '__main__':
    topo = Topology()
    topo.build('config/topology.ini')

    '''TEST Key init between Alice-Bob and Alice-relay1
    Note: IP and Port are not yet implemented'''
    Alice = Sender('config/host_R1.ini')

    sp = Alice.shortest_path(topo, '127.16.4.2')
    print(sp)

    Alice.initialyze_keys(sp)

    while Alice.init_keys_done != len(sp)-1:
        pass

    message = 'Gros caca de Alice'
    print('Message à envoyer:', message)    
    
    shallot = Alice.build_shallot(sp, message)
    Alice.send_shallot(sp[1], 9000, shallot)