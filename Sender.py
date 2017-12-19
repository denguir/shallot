from utils.digit_conversion import *
from utils.dijkstra import *
from Host import Host
from Key import Key


class Sender(Host):
    """docstring for Sender."""
    def __init__(self, config_file):
        super(Sender, self).__init__(config_file)
        self.route = []
        self.KeyID_key = {}
        self.IP_KeyID = {}
        self.g = 2
        self.p = 179769313486231590770839156793787453197860296048756011706444423684197180216158519368947833795864925541502180565485980503646440548199239100050792877003355816639229553136239076508735759914822574862575007425302077447712589550957937778424442426617334727629299387668709205606050270810842907692932019128194467627007
        self.init_keys_done = 0
        self.listen()
        self.write()

    def shortest_path(self, topology, destination):
        if destination not in topology.nodes:
            print('Shortest path research failed:')
            print('{} not in network'.format(destination))
        else:
            weigths, previous_path = dijkstra(topology, (self.ip_addr,self.port_in))
            path = []
            node = destination
            while node is not None:
                path.append(node)
                node = previous_path[node]
            path.reverse()
            # path.append(path[-1])
            return path

    def initialyze_keys(self,path):
        for i in range(1,len(path)):
            self.generate_and_send_new_key(path[i][0],path[i][1])

    def generate_and_send_new_key(self, ip_address, port):
        '''1) Generate a Key object in which will be stored a unique Key ID and a public key.
           2) Send the key ID and the public key to the other entities'''
        key_id = self.generate_key_id()
        new_key = Key(key_id, self.g, self.p)
        self.KeyID_key.update({key_id:new_key})
        self.IP_KeyID.update({ip_address:key_id})
        self.send_key_init(ip_address, port, new_key.get_key_id(), new_key.get_public_key())

    def generate_key_id(self):
        '''Generate the unique key ID.'''
        key_id = len(self.KeyID_key)+1
        return dec_to_32bits(key_id)

    def send_key_init(self, ip_address, port, key_id, public_key):
        version = '0001'
        msg_type = '0000'
        msg_empty_space = '00000000'

        body = key_id + dec_to_4bits(self.g) + dec_to_1024bits(self.p) + dec_to_1024bits(public_key)

        msg_length = self.compute_msg_length(body)

        header = version + msg_type + msg_empty_space + msg_length
        self.handshake(header + body, ip_address,port)

    def send_shallot(self, ip_address, port, shallot):
        version = '0001'
        msg_type = '0010'
        msg_empty_space = '00000000'

        msg_length = self.compute_msg_length(shallot)

        header = version + msg_type + msg_empty_space + msg_length
        self.send(header + shallot, ip_address,port)

    def generate_key_from_replier(self, message):
        '''Generate the shared key between the sender and the replier.'''
        self.KeyID_key[message[32:64]].generate_shared_key(int(message[64:1088],2))
        self.init_keys_done += 1

    def encrypt(self, key_id, message):
        '''Encrypt the message raw using the AES algorithm'''
        return self.KeyID_key[key_id].cipher.encrypt(message)

    def decrypt(self, key_id, message):
        '''Decrypt the message enc using the AES algorithm'''
        return self.KeyID_key[key_id].cipher.decrypt(message)

    def build_shallot(self, path, message):
        '''Build the shallot based on the order of the keys ID'''
        shallot = message
        path.reverse()

        IP = path[0][0]
        PORT = path[0][1]
        key_ID = self.IP_KeyID[IP]
        IP_next = path[0][0]
        PORT_next = path[0][1]
        binary_IP_next = ip2bin(IP_next)
        binary_PORT_next = dec_to_32bits(PORT_next)
        shallot = self.encrypt(key_ID,binary_IP_next+binary_PORT_next+shallot)
        shallot = key_ID + shallot

        for i in range(1,len(path)-1):
            IP = path[i][0]
            PORT = path[i][1]
            key_ID = self.IP_KeyID[IP]

            IP_next = path[i-1][0]
            PORT_next = path[i-1][1]
            binary_IP_next = ip2bin(IP_next)
            binary_PORT_next = dec_to_32bits(PORT_next)
            shallot = self.encrypt(key_ID,binary_IP_next+binary_PORT_next+shallot)

            shallot = key_ID + shallot
            
        path.reverse()
        return shallot

    def on_data(self, data, conn):
        data = str(data)[2:]
        version=data[0:4]
        msg_type=data[4:8]
        msg_length=data[16:32]
        if msg_type == '0001':
            # MSG TYPE = KEY_REPLY
            print('KEY_REPLY')
            self.generate_key_from_replier(data)
        elif msg_type == '0011':
            # MSG TYPE = ERROR
            print('ERROR')
            self.send('ACK')
        else:
            print(data)
