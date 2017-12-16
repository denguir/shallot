from Topology import Topology
from Relay import Relay
from Receiver import Receiver
from Host import Host
from Sender import Sender
from Key import Key

if __name__ == '__main__':
    topo = Topology()
    topo.build('config/topology.ini')

    '''TEST Key init between Alice-Bob and Alice-relay1
    Note: IP and Port are not yet implemented'''
    Alice = Sender('config/host_R1.ini')
    Bob = Receiver('config/host_R4.ini')
    relay1 = Relay('config/host_R2.ini')
    relay2 = Relay('config/host_R3.ini')

    sp = Alice.shortest_path(topo, '127.16.4.2')
    #print(sp)

    Alice.initialyze_keys(sp)

    '''Key negotiation with Bob'''
    # Bob_KeyID = Alice.IP_KeyID[Bob.ip_addr]
    # relay1_KeyID = Alice.IP_KeyID[relay1.ip_addr]
    # relay2_KeyID = Alice.IP_KeyID[relay2.ip_addr]
    # Bob.generate_key_from_sender('','',Bob_KeyID, Alice.KeyID_key[Bob_KeyID].get_public_key())
    # Alice.generate_key_from_replier(Bob_KeyID,Bob.KeyID_key[Alice.IP_KeyID[Bob.ip_addr]].get_public_key())

    # '''Key negotiation with relay1'''
    # relay1.generate_key_from_sender('','',relay1_KeyID, Alice.KeyID_key[relay1_KeyID].get_public_key())
    # Alice.generate_key_from_replier(relay1_KeyID,relay1.KeyID_key[relay1_KeyID].get_public_key())

    # '''Key negotiation with relay2'''
    # relay2.generate_key_from_sender('','',relay2_KeyID, Alice.KeyID_key[relay2_KeyID].get_public_key())
    # Alice.generate_key_from_replier(relay2_KeyID,relay2.KeyID_key[relay2_KeyID].get_public_key())
    

    # print("Alice-Bob key:")
    # print(Alice.KeyID_key[Alice.IP_KeyID[Bob.ip_addr]].get_shared_key())
    # print(Bob.KeyID_key[Alice.IP_KeyID[Bob.ip_addr]].get_shared_key())
    # print("\n")

    # print("Alice-relay1 key:")
    # print(Alice.KeyID_key[Alice.IP_KeyID[relay1.ip_addr]].get_shared_key())
    # print(relay1.KeyID_key[Alice.IP_KeyID[relay1.ip_addr]].get_shared_key())
    # print('\n')

    # print("Alice-relay2 key:")
    # print(Alice.KeyID_key[Alice.IP_KeyID[relay2.ip_addr]].get_shared_key())
    # print(relay2.KeyID_key[Alice.IP_KeyID[relay2.ip_addr]].get_shared_key())
    # print('\n')

    #Alice.build_shallot(sp,'caca')