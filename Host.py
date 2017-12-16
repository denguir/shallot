from abc import ABCMeta, abstractmethod
import configparser
import threading
import queue
import select
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
        self.ip_addr, self.port_in = self.init_address(config_file)
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.bind((self.ip_addr, self.port_in))
        self.server.listen(5)
        self.inputs = [self.server]
        self.outputs = []
        self.alive = True
        self.buffer = {}

    def init_address(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        ip = config['host']['ip']
        port = config['host']['port']
        return ip, int(port)

    def listen(self):
        BUFFER_SIZE = 4096
        while self.alive:
            readable, writable, exceptional = select.select(self.inputs,
            self.outputs, self.inputs)
            for s in readable:
                if s is self.server:
                    conn, addr = s.accept()
                    print("in:", addr)
                    conn.setblocking(0)
                    self.inputs.append(conn)
                    self.buffer[conn] = queue.Queue()
                else:
                    data = s.recv(BUFFER_SIZE)
                    if data:
                        self.buffer[s].put(data)
                        if s not in self.outputs:
                            self.outputs.append(s)
                    else:
                        if s in self.outputs:
                            self.outputs.remove(s)
                        self.inputs.remove(s)
                        s.close()
                        del self.buffer[s]

            for s in writable:
                try:
                    next_msg = self.buffer[s].get_nowait()
                except Queue.Empty:
                    self.outputs.remove(s)
                else:
                    s.send(next_msg)

            for s in exceptional:
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.buffer[s]

    def stop(self):
        self.alive = False

    def connect(self, ip, port):
        readable, writable, exceptional = select.select(self.inputs,
        self.outputs, self.inputs)
        print(writable)
        for s in writable:
            if s.getsockname()[0] == ip:
                self.socket_out.connect((ip, port))
                print("connect:", self.ip_addr, self.port_out)
                return s

    def send(self, msg, ip, port):
        s = self.connect(ip,port)
        if s is None:
            pass
        else:
            s.send(msg.encode('utf-8'))

    @abstractmethod
    @threaded
    def on_data(self, ip_origin, port_origin):
        """Handle the data on the basis of the type of msg
        ip_origin and port_origin refer to the address of the
        sender"""
