

def ip2bin(ip):
    octets = map(int, ip.split('/')[0].split('.')) # '1.2.3.4'=>[1, 2, 3, 4]
    binary = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*octets)
    range = int(ip.split('/')[1]) if '/' in ip else None
    return binary[:range] if range else binary

def ip2dec(ip_bin):
    ip_dec = str(int(ip_bin[0:8],2))+'.'+str(int(ip_bin[8:16],2))+'.'+str(int(ip_bin[16:24],2))+'.'+str(int(ip_bin[24:32],2))
    return ip_dec

def dec_to_4bits(integer):
    return '{:04b}'.format(integer)

def dec_to_16bits(integer):
    return '{:016b}'.format(integer)

def dec_to_32bits(integer):
    return '{:032b}'.format(integer)

def dec_to_1024bits(integer):
    return '{:01024b}'.format(integer)
