import random
import math
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
        self.listen()

    def dijkstra(self, topology, source):
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

    def shortest_path(self, topology, destination):
        if destination not in topology.nodes:
            print('Shortest path research failed:')
            print('{} not in network'.format(destination))
        else:
            weigths, previous_path = self.dijkstra(topology, self.ip_addr)
            path = []
            node = destination
            while node is not None:
                path.append(node)
                node = previous_path[node]
            path.reverse()
            return path

    def initialyze_keys(self,path):
        for i in range(1,len(path)):
            self.generate_and_send_new_key(path[i],9000)

    def generate_and_send_new_key(self, ip_address, port):
        '''1) Generate a Key object in which will be stored a unique Key ID and a public key.
           2) Send the key ID and the public key to the other entities'''
        key_id = self.generate_key_id()
        new_key = Key(key_id)
        self.KeyID_key.update({key_id:new_key})
        self.IP_KeyID.update({ip_address:key_id})
        self.send_key_init(ip_address, port, new_key.get_key_id(), new_key.get_public_key())

    def generate_key_id(self):
        '''Generate the unique key ID.'''
        key_id = len(self.KeyID_key)+1
        return self.dec_to_32bits(key_id)

    def send_key_init(self, ip_address, port, key_id, public_key):
        version = '0001'
        msg_type = '0000'
        msg_empty_space = '00000000'

        body = key_id + '{:04b}'.format(self.g) + '{:01024b}'.format(self.p) + '{:01024b}'.format(public_key)

        msg_length = self.compute_msg_length(body)

        header = version + msg_type + msg_empty_space + msg_length
        self.send(header + body, ip_address,port)

    def compute_msg_length(self, body):
        optional_padding1 = (len(body)%8)*(' ')
        body += optional_padding1
        optional_padding2 = int((len(body)/8)%4)*('    ')
        body += optional_padding2
        return '{:016b}'.format(int(((len(body)/8)+4)/4))

    def generate_key_from_replier(self, message):
        '''Generate the shared key between the sender and the replier.'''
        self.KeyID_key[message[32:64]].generate_shared_key(int(message[64:1088],2))

    def encrypt(self, key_id, message):
        '''Encrypt the message raw using the AES algorithm'''
        return self.KeyID_key[key_id].cipher.encrypt(message)

    def decrypt(self, key_id, message):
        '''Decrypt the message enc using the AES algorithm'''
        return self.KeyID_key[key_id].cipher.decrypt(message)

    def build_shallot(self, path, message):
        '''Build the shallot based on the order of the keys ID'''
        shallot = message
        path.append(path[-1])
        path.reverse
        for i in range(1,len(path)-1):
            IP = path[i]
            key_ID = self.IP_KeyID[IP]

            IP_next = path[i-1]
            binary_IP_next = self.ip2bin(IP_next)
            print(key_ID,binary_IP_next+shallot)
            shallot = self.encrypt(key_ID,binary_IP_next+shallot)

            shallot = key_ID + shallot
        return shallot

    def decrypt_shallot(self, keysID_order, message):
        '''The Sender can decrypt the entire shallot by using this function'''
        shallot = message
        for key_id in keysID_order:
            shallot = self.decrypt(key_id, shallot)
        return shallot

    def ip2bin(self, ip):
        octets = map(int, ip.split('/')[0].split('.')) # '1.2.3.4'=>[1, 2, 3, 4]
        binary = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*octets)
        range = int(ip.split('/')[1]) if '/' in ip else None
        return binary[:range] if range else binary

    def dec_to_32bits(self, integer):
        return '{:032b}'.format(integer)

    def dec_to_1024bits(self, integer):
        return '{:01024b}'.format(integer)

    def on_data(self, data, conn):
        data = str(data)[2:]
        ip_origin,port_origin=conn.getsockname()
        version=data[0:4]
        msg_type=data[4:8]
        msg_length=data[16:32]
        if msg_type == '0000':
            # MSG TYPE = KEY_INIT
            self.generate_key_from_sender(ip_origin,port_origin,data)
            print('KEY_INIT')
        elif msg_type == '0001':
            # MSG TYPE = KEY_REPLY
            self.generate_key_from_replier(data)
            print('KEY_REPLY')
        elif msg_type == '0010':
            # MSG TYPE = MESSAGE_RELAY
            self.decrypt_shallot(data)
            print('MESSAGE_RELAY')
        elif msg_type == '0011':
            # MSG TYPE = ERROR
            self.send('ACK')
            print('ERROR')
        else:
            print(data)