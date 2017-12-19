# from Topology import Topology
# from Sender import Sender
# import time

# if __name__ == '__main__':
#     topo = Topology()
#     topo.build('config/topology.ini')

#     '''TEST Key init between Alice-Bob and Alice-relay1
#     Note: IP and Port are not yet implemented'''
#     Alice = Sender('config/host_R1.ini')

#     sp = Alice.shortest_path(topo,('127.16.4.2',9010))
#     print('Path:', sp)

#     Alice.initialyze_keys(sp)

#     while Alice.init_keys_done != len(sp)-1:
#         pass

#     message = 'First message from Alice to Bob'
#     print('Message to send:', message)
#     shallot = Alice.build_shallot(sp, message)
#     Alice.send_shallot(sp[1][0], sp[1][1], shallot)




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
