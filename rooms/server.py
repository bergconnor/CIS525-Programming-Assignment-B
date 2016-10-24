import select, socket, sys, pdb
from inet import Hall, Room, User
import inet

READ_BUFFER = 4096

def create_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind((host, port))
    s.listen(inet.MAX_CLIENTS)
    print("Now listening...")
    return s

host = socket.gethostname()
listen_sock = create_socket(host, inet.PORT)

hall = Hall()
connection_list = []
connection_list.append(listen_sock)

while True:
    read_users, write_users, error_sockets = select.select(connection_list, [], [])
    for player in read_users:
        if user is listen_sock:
            new_socket, add = user.accept()
            new_user = User(new_socket)
            connection_list.append(new_user)
            hall.welcome_new(new_user)

        else:
            msg = user.socket.recv(READ_BUFFER)
            if msg:
                msg = msg.decode().lower()
                hall.handle_msg(user, msg)
            else:
                user.socket.close()
                connection_list.remove(user)

    for sock in error_sockets:
        sock.close()
        connection_list.remove(sock)