from diffiehellman.diffiehellman import DiffieHellman
#https://github.com/chrisvoncsefalvay/diffiehellman

import binascii
from AESCipher import AESCipher

class Key(DiffieHellman):
    """Key object which stores the key ID, the public key and the share key between 2 entities."""
    def __init__(self, key_id):
        DiffieHellman.__init__(self, group=2, key_length=640)
        self.key_id = key_id
        self.generate_public_key()
        self.cipher = None

    def get_key_id(self):
        '''Return the unique 32-bits key ID.'''
        return self.key_id

    def get_public_key(self):
        '''Return the public key.'''
        return self.public_key

    def get_shared_key(self):
        '''Return the shared key between 2 entities and will be used for the encryption.'''
        return self.shared_key

    def generate_shared_key(self, other_public_key):
        '''Generate the shared key between 2 entities.'''
        self.generate_shared_secret(other_public_key)
        key = binascii.unhexlify(self.shared_key)
        self.cipher = AESCipher(key)