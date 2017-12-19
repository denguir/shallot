def ip2bin(ip):
    ''' Convert a ip in format: 192.168.10.1 to binary format: 11000000101010000000101000000001 '''
    octets = map(int, ip.split('/')[0].split('.')) # '1.2.3.4'=>[1, 2, 3, 4]
    binary = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*octets)
    range = int(ip.split('/')[1]) if '/' in ip else None
    return binary[:range] if range else binary

def ip2dec(ip_bin):
    ''' Convert a ip in binary format: 11000000101010000000101000000001 to the classic format: 192.168.10.1 '''
    ip_dec = str(int(ip_bin[0:8],2))+'.'+str(int(ip_bin[8:16],2))+'.'+str(int(ip_bin[16:24],2))+'.'+str(int(ip_bin[24:32],2))
    return ip_dec

def dec_to_4bits(integer):
    ''' Convert an integer to binary (4 bits) '''
    return '{:04b}'.format(integer)

def dec_to_16bits(integer):
    ''' Convert an integer to binary (16 bits) '''
    return '{:016b}'.format(integer)

def dec_to_32bits(integer):
    ''' Convert an integer to binary (32 bits) '''
    return '{:032b}'.format(integer)

def dec_to_1024bits(integer):
    ''' Convert an integer to binary (1024 bits) '''
    return '{:01024b}'.format(integer)
