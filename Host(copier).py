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
        self.port_out = self.port_in + 1000
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.bind((self.ip_addr, self.port_in))
        self.server.listen(5)
        self.inputs = [self.server]
        self.outputs = []
        self.alive = True
        self.buffer = {}
        self.i = 0

    def init_address(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        ip = config['host']['ip']
        port = config['host']['port']
        return ip, int(port)

    @threaded
    def listen(self):
        BUFFER_SIZE = 4096
        while self.alive:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            for s in readable:
                if s is self.server:
                    # Establish a new connection and put it in the buffer
                    conn, addr = s.accept()
                    print("connection from :", addr[0], addr[1], '\t to:', self.ip_addr, self.port_in)
                    conn.setblocking(0)
                    self.inputs.append(conn)
                    self.buffer[conn] = queue.Queue()
                else:
                    # read the input socket and put it in outputs
                    # to potentially reply through this connection
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
                # apply the on_data function on the available
                # sockets of the outputs list
                try:
                    print(s,'\n')
                    print(self.buffer,'\n')
                    next_msg = self.buffer[s].get()
                except queue.Empty:
                    self.outputs.remove(s)
                else:
                    #print(next_msg)
                    self.on_data(next_msg, s)

            for s in exceptional:
                # if there is any error on the inputs, close the connection
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.buffer[s]

    def stop(self):
        self.alive = False

    def connect(self, ip, port):
        # if the connection is already established, use it
        for s in self.outputs:
            if s.getsockname == (ip, port):
                return s
        # else, create a new connection, with an used port number
        new_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        new_s.bind((self.ip_addr, self.port_out + self.i))
        self.i += 1
        self.outputs.append(new_s)
        try:
            new_s.connect((ip, port))
        except socket.error:
            print('Connection failed')
        return new_s

    def send(self, msg, ip, port):
        s = self.connect(ip,port)
        if s is None:
            pass
        else:
            s.send(msg.encode('utf-8'))

    @abstractmethod
    def on_data(self, data, conn):
        """Handle the data on the basis of the type of msg
        ip_origin and port_origin refer to the address of the
        sender"""
