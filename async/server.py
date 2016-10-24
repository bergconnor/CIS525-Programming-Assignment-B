import asynchat
import asyncore
import socket

from inet import CODE
 
chat_room = {}
usernames = []
sockets   = []
 
class ChatHandler(asynchat.async_chat):
    def __init__(self, sock):
        asynchat.async_chat.__init__(self, sock=sock, map=chat_room)
        self.sock = sock
        self.set_terminator('\n')
        self.buffer = []
 
    def collect_incoming_data(self, data):
        self.buffer.append(data)
 
    def found_terminator(self):
        msg = ''.join(self.buffer)
        for handler in chat_room.itervalues():
            if hasattr(handler, 'push'):
                if handler is not self:
                    index = sockets.index(str(self.sock))
                    prompt = '<' + usernames[index] + '>'
                    handler.push(prompt + ' ' + msg + '\n')
        self.buffer = []
 
class ChatServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self, map=chat_room)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
 
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = ChatHandler(sock)
            self.get_username(sock)

    def get_username(self, sock):
        username_prompt = 'Enter a username: '
        msg = username_prompt
        while True:
            sock.send(msg)
            while True:
                try:
                    name = sock.recv(1024)
                    break
                except:
                    continue
            if name in usernames:
                msg = 'This username is already in use.\n' + username_prompt
                continue
            else:
                break
        usernames.append(name)
        sockets.append(str(sock))
 
server = ChatServer('localhost', 5050)
 
print 'Serving on localhost:5050'
asyncore.loop(map=chat_room)