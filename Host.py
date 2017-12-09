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
    def __init__(self, config_file):
        # TODO: host must look at host.ini
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
            data_with_origin = {addr:data}
            self.buffer.put(data_with_origin)
            if not self.buffer.empty():
                msg = self.buffer.get()[addr]
                key_id = msg[0:32]
                public_key = msg[32:]

            if not data: break
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