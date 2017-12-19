from diffiehellman.diffiehellman import DiffieHellman
# diffiehellman found on: https://github.com/chrisvoncsefalvay/diffiehellman

import binascii
from AESCipher import AESCipher

class Key(DiffieHellman):
    '''Key object which stores the key ID, the public key and the shared key between 2 entities.'''
    def __init__(self, key_id, g_parameter, p_parameter):
        DiffieHellman.__init__(self, g_parameter, p_parameter)
        self.key_id = key_id
        self.generate_public_key()
        self.cipher = None

    def get_key_id(self):
        '''Return the unique 32-bits key ID.'''
        return self.key_id

    def get_public_key(self):
        '''Return the public key.'''
        return self.public_key

    def generate_shared_key(self, other_public_key):
        '''Generate the shared key between 2 entities and a AESCipher object for the encryption.'''
        self.generate_shared_secret(other_public_key) # function from the diffiehellman module that generates the shared key
        key = binascii.unhexlify(self.shared_key) # Convert in the appropriate format for the AESCipher module
        self.cipher = AESCipher(key)
