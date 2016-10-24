import asynchat
import asyncore
import socket
import threading
import sys

from inet import CODE
 
class ChatClient(asynchat.async_chat):
 
    def __init__(self, host, port):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
 
        self.set_terminator('\n')
        self.buffer = []

        while True:
            while True:
                try:
                    name = raw_input(self.socket.recv(1024))
                    break
                except:
                    continue
            self.socket.send(name)
            flag = int(self.socket.recv(1024))
            if flag:
                continue
            else:
                break

    def collect_incoming_data(self, data):
        if data:
            self.buffer.append(data)
 
    def found_terminator(self):
        msg = ''.join(self.buffer)
        print msg
        self.buffer = []
 
client = ChatClient('localhost', 5050)
 
comm = threading.Thread(target=asyncore.loop)
comm.daemon = True
comm.start()
 
while True:
    msg = raw_input('> ')
    client.push(msg + '\n')