import socket, pdb

MAX_USERS = 100
PORT = 55781
QUIT_STRING = '<$quit$>'
SERVER_STRING = '<SYSTEM> '
ERASE_LINE = '\x1b[2K'
START_LINE = '\x1b[0G'

class Room_Manager:
    def __init__(self):
        self.rooms = {}
        self.room_user_map = {}
        self.users = []

    def welcome_new(self, new_user):
        new_user.socket.sendall(b'Enter a username:\n')

    def list_rooms(self, user):
        
        if len(self.rooms) == 0:
            msg = 'Oops, no active rooms currently. Create your own!\n' \
                + 'Use [<join> room_name] to create a room.\n'
            user.socket.sendall(msg.encode())
        else:
            msg = 'Listing current rooms...\n'
            for room in self.rooms:
                msg += room + ': ' + str(len(self.rooms[room].users)) + ' user(s)\n'
            user.socket.sendall(msg.encode())
    
    def handle_msg(self, user, msg):
        
        instructions = b'Instructions:\n'\
            + b'[<list>] to list all rooms\n'\
            + b'[<join> room_name] to join/create/switch to a room\n' \
            + b'[<manual>] to show instructions\n' \
            + b'[<quit>] to quit\n' \
            + b'\n'

        if 'name:' in msg:
            name = msg.split()[1]
            if name in self.users:
                get_username = b'Username already taken.\n' \
                    + b'Enter a username:\n'
                user.socket.sendall(get_username)
            elif name == 'you':
                get_username = b'Invalid username.\n' \
                    + b'Enter a username:\n'
                user.socket.sendall(get_username)  
            else:
                user.name = name
                self.users.append(name)
                print('New connection from:', user.name)
                user.socket.sendall(instructions)

        elif '<join>' in msg:
            same_room = False
            if len(msg.split()) >= 2:
                room_name = msg.split()[1]
                if user.name in self.room_user_map:
                    if self.room_user_map[user.name] == room_name:
                        user.socket.sendall(b'You are already in room: ' + room_name.encode())
                        same_room = True
                    else:
                        old_room = self.room_user_map[user.name]
                        self.rooms[old_room].remove_user(user)
                if not same_room:
                    if not room_name in self.rooms:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].users.append(user)
                    self.rooms[room_name].welcome_new(user)
                    self.room_user_map[user.name] = room_name
            else:
                user.socket.sendall(instructions)

        elif '<list>' in msg:
            self.list_rooms(user) 

        elif '<manual>' in msg:
            user.socket.sendall(instructions)
        
        elif '<quit>' in msg:
            user.socket.sendall(QUIT_STRING.encode())
            self.remove_user(user)

        else:
            if user.name in self.room_user_map:
                self.rooms[self.room_user_map[user.name]].broadcast(user, msg.encode())
            else:
                msg = 'You are currently not in any room! \n' \
                    + 'Use [<list>] to see available rooms! \n' \
                    + 'Use [<join> room_name] to join a room! \n'
                user.socket.sendall(msg.encode())
    
    def remove_user(self, user):
        if user.name in self.room_user_map:
            self.rooms[self.room_user_map[user.name]].remove_user(user)
            del self.room_user_map[user.name]
        if user.name in self.users:
            self.users.remove(user.name)
        print('<' + user.name + '> ' + 'has disconnected\n')

    
class Room:
    def __init__(self, name):
        self.users = []
        self.name = name

    def welcome_new(self, from_user):
        unprompt = ERASE_LINE + START_LINE
        msg = unprompt + '<' + self.name + '> ' + from_user.name + ' joined the room\n'
        for user in self.users:
            if user is not from_user:
                user.socket.sendall(msg.encode())
            else:
                if len(self.users) == 1:
                    msg = unprompt + '<' + self.name + '> You created the room\n'
                else:
                    msg = unprompt + '<' + self.name + '> You joined the room\n'
                user.socket.sendall(msg.encode())
    
    def broadcast(self, from_user, msg):
        unprompt = ERASE_LINE.encode() + START_LINE.encode()
        msg = unprompt + b'<' + from_user.name.encode() + b'> ' + msg
        for user in self.users:
            if user is not from_user:
                user.socket.sendall(msg)
            else:
                user.socket.sendall(START_LINE.encode())

    def remove_user(self, user):
        self.users.remove(user)
        unprompt = ERASE_LINE.encode() + START_LINE.encode()
        leave_msg = unprompt + b'<' + user.name.encode() + b'> has left the room\n'
        self.broadcast(user, leave_msg)

class User:
    def __init__(self, socket, name = 'new'):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

    def fileno(self):
        return self.socket.fileno()
