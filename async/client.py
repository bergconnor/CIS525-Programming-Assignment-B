import asynchat
import asyncore
import socket
import threading

from inet import CODE
 
class ChatClient(asynchat.async_chat):
 
    def __init__(self, host, port):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
 
        self.set_terminator('\n')
        self.buffer = []
 
    def collect_incoming_data(self, data):
        if int(data) == CODE:
            self.handle_server_message()
        else:
            self.buffer.append(data)
 
    def found_terminator(self):
        msg = ''.join(self.buffer)
        print 'Received:', msg
        self.buffer = []

    def handle_server_message(self):
        self.push('ACK\n')
 
client = ChatClient('localhost', 5050)
 
comm = threading.Thread(target=asyncore.loop)
comm.daemon = True
comm.start()
 
while True:
    msg = raw_input('> ')
    client.push(msg + '\n')