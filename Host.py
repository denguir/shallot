from abc import ABCMeta, abstractmethod
import configparser
import threading
import queue
import socket

def threaded(func):
    def run(*k, **kw):
        t = threading.Thread(target=func, args=k, kwargs=kw)
        t.start()
    return run

class Host(object):
    """docstring for Server."""
    __metaclass__  = ABCMeta
    def __init__(self, config_file):
        super(Host, self).__init__()
        self.ip_addr, self.port = self.init_address(config_file)
        self.alive = True
        self.buffer = queue.Queue()

    def init_address(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        ip = config['host']['ip']
        port = config['host']['port']
        return ip, int(port)

    @threaded
    def listen(self):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((self.ip_addr, self.port))
        s.listen(5) # length of the network
        BUFFER_SIZE = 2148

        while self.alive:
            conn, addr = s.accept()
            data = conn.recv(BUFFER_SIZE)
            if data:
                self.buffer.put(data)
                self.on_data(addr[0], addr[1])

            else: break
            print("received data:", data)
            conn.close()

    def stop(self):
        self.alive = False

    def connect(self, ip, port):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
        except socket.error:
            print('Connection failed')
        return s

    @threaded
    def send(self, msg, ip, port):
        s = self.connect(ip,port)
        s.send(msg.encode('utf-8'))

    # @threaded
    # def key_reply(self):
    #     self.buffer.get()[]
    #     msg = self.buffer.get()
    #     key_id = msg[0:32]
    #     public_key = msg[32:]

    @abstractmethod
    @threaded
    def on_data(self, ip_origin, port_origin):
        """Handle the data on the basis of the type of msg
        ip_origin and port_origin refer to the address of the
        sender"""
