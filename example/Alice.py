import os, sys
# Import needed python files from parent path of the example folder
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from Topology import Topology
from Sender import Sender

if __name__ == '__main__':
    topo = Topology()
    topo.build(parentPath + '/config/topology.ini')

    Alice = Sender(parentPath + '/config/host_R1.ini')

    Alice.init_encryption_parameters(parentPath + '/config/encryption.ini')

    ip_bob = '127.16.4.2'
    port_bob = 9010

    sp = Alice.shortest_path(topo,(ip_bob, port_bob))
    print(sp)

    Alice.initialyze_keys(sp)

    print("Handshaking with the relays ...")
    while Alice.init_keys_done != len(sp)-1:
        pass

    print("Send first message ...")
    first_shallot = Alice.build_shallot(sp, 'First message from Alice to Bob')
    Alice.send_shallot(sp[1][0], sp[1][1], first_shallot)

    while Alice.alive:
        message = input(">>>")
        shallot = Alice.build_shallot(sp, message)
        Alice.send_shallot(sp[1][0], sp[1][1], shallot)
