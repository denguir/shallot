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
    def __init__(self, ip_addr, port):
        super(Host, self).__init__()
        self.ip_addr = ip_addr
        self.port = port
        self.alive = True
        self.buffer = queue.Queue()

    @threaded
    def listen(self):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((self.ip_addr, self.port))
        s.listen(5) # length of the network
        BUFFER_SIZE = 1024

        while self.alive:
            conn, addr = s.accept()
            data = conn.recv(BUFFER_SIZE)
            self.buffer.put(data)
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


if __name__ == '__main__':
    A = Host('127.0.0.1', 5000)
    R = Host('127.0.0.2', 5000)
    A.listen()
    R.listen()
    A.send('coucou', '127.0.0.2', 5000)
    R.send('ok', '127.0.0.1', 5000)
    print(A.buffer.get())
    print(R.buffer.get())
