import select, socket, sys
from inet import Room, Room_Manager, User
import inet

RX_BUFFER = 4096

server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_connection.connect((socket.gethostname(), inet.PORT))

def prompt():
    print('<You>', end=' ', flush = True)

print('Connected to server\n')
msg_prefix = ''

socket_list = [sys.stdin, server_connection]

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if s is server_connection:
            msg = s.recv(RX_BUFFER)
            if not msg:
                print('Server down!')
                sys.exit(2)
            else:
                if msg == inet.QUIT_STRING.encode():
                    sys.stdout.write('Bye\n')
                    sys.exit(2)
                else:
                    sys.stdout.write(msg.decode())
                    if 'Enter a username' in msg.decode():
                        msg_prefix = 'name: '
                    else:
                        msg_prefix = ''
                    prompt()

        else:
            msg = msg_prefix + sys.stdin.readline()
            server_connection.sendall(msg.encode())
