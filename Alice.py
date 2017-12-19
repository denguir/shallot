from Topology import Topology
from Sender import Sender
import time

if __name__ == '__main__':
    topo = Topology()
    topo.build('config/topology.ini')

    '''TEST Key init between Alice-Bob and Alice-relay1
    Note: IP and Port are not yet implemented'''
    Alice = Sender('config/host_R1.ini')

    sp = Alice.shortest_path(topo,('127.16.4.2',9010))
    print(sp)

    Alice.initialyze_keys(sp)

    while Alice.init_keys_done != len(sp)-1:
        pass

    message1 = 'Gros caca de Alice'
    print('Message à envoyer:', message1)

    shallot1 = Alice.build_shallot(sp, message1)
    Alice.send_shallot(sp[1][0], sp[1][1], shallot1)
    time.sleep(0.1)

    message2 = 'Deuxieme gros caca de Alice'
    print('Message à envoyer:', message2)
    shallot2 = Alice.build_shallot(sp, message2)
    Alice.send_shallot(sp[1][0], sp[1][1], shallot2)
