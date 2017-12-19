from abc import ABCMeta, abstractmethod
from utils.digit_conversion import *
import configparser
import threading
import queue
import socket
import sys

def threaded(func):
    def run(*k, **kw):
        t = threading.Thread(target=func, args=k, kwargs=kw)
        t.start()
    return run

class Host(object):
    """
    Abstract class that runs in server mode (listen)
        and client mode (write) in the same time
    """
    __metaclass__  = ABCMeta
    def __init__(self, config_file):
        super(Host, self).__init__()
        self.ip_addr, self.port_in = self.init_address(config_file)
        self.port_out = self.port_in + 1000
        self.alive = True
        self.buffer = queue.Queue()

    def init_address(self, config_file):
        '''read the <config_file> to attribute the ip and port
            of a specified entity'''
        config = configparser.ConfigParser()
        config.read(config_file)
        ip = config['host']['ip']
        port = config['host']['port']
        return ip, int(port)

    @threaded
    def listen(self):
        '''Always listen to new connections from the outside'''
        BUFFER_SIZE = 4096
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip_addr, self.port_in))
        s.listen(1)
        try:
            while self.alive:
                conn, addr = s.accept()
                print(' ')
                print('Connection address:', addr)
                data = conn.recv(BUFFER_SIZE)
                if data:
                    self.buffer.put((data, conn))
                else: break
        except KeyboardInterrupt:
            print("\n Server stopped")
            sys.exit(0)

    @threaded
    def write(self):
        '''Always check the buffer if there are some data to be sent'''
        while self.alive:
            data, conn = self.buffer.get()
            self.on_data(data, conn)

    def stop(self):
        '''kill server and client mode'''
        self.alive = False

    def send(self, msg, ip, port):
        '''send a message <msg> to a specified entity described by
            its ip and port'''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip_addr, self.port_out))
        s.connect((ip, port))
        s.send(msg.encode('utf-8'))
        s.close()

    def compute_msg_length(self, body):
        padding = ' '
        optional_padding1 = (len(body)%8)*padding
        body += optional_padding1
        optional_padding2 = int((len(body)/8)%4)*4*padding
        body += optional_padding2
        return dec_to_16bits(int(((len(body)/8)+4)/4))

    @abstractmethod
    def on_data(self, data, conn):
        """Handle the data on the basis of the type of the message type
        <conn> refers to the connection established with the sender"""
