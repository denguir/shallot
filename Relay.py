
class Relay(object):
    """docstring for Relay."""
    def __init__(self, ip_addr):
        superRelay, self).__init__()
        self.ip_addr = ip_addr
        self.key = 0

    def decrypt(self, encrypted_msg):
        ''' decrypt the message sent by previous entity'''
        pass

    def send(self, msg, ip_dest):
        '''Send this message to the destination'''
        pass
