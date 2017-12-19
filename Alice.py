from Topology import Topology
from Sender import Sender
import time

if __name__ == '__main__':
    topo = Topology()
    topo.build('config/topology.ini')

    Alice = Sender('config/host_R1.ini')

    sp = Alice.shortest_path(topo,('127.16.4.2',9010))
    print(sp)

    Alice.initialyze_keys(sp)

    while Alice.init_keys_done != len(sp)-1:
        pass

    message = input(">>>")
    shallot = Alice.build_shallot(sp, message)
    Alice.send_shallot(sp[1][0], sp[1][1], shallot)

    time.sleep(3)

    message = input(">>>")
    shallot = Alice.build_shallot(sp, message)
    Alice.send_shallot(sp[1][0], sp[1][1], shallot)
