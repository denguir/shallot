
class Sender(object):
    """docstring for Sender."""
    def __init__(self, ip_addr):
        super(Sender, self).__init__()
        self.ip_addr = ip_addr
        self.route = []

    def find_route(self, ip_dest, topology):
        '''
        Apply Dijkstra algorithm to find the route between Sender and Reicever
        https://gist.github.com/econchick/4666413
        '''
        pass

    def init_keys(self, route):
        '''Apply Diffie-Hellmann to initialize key with all the routed relays'''
        pass

    def encrypt(self, msg):
        '''Build the shallot according to the keys generated in init_keys'''
        pass

    def send(self, encrypted_msg, ip_dest):
        '''Send encrypted message to the destination'''
        pass
