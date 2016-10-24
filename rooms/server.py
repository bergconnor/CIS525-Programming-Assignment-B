import select, socket, sys, pdb
from inet import Hall, Room, Player
import inet

READ_BUFFER = 4096

def create_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind((host, port))
    s.listen(inet.MAX_CLIENTS)
    print("Now listening at ", address)
    return s

host = sys.argv[1] if len(sys.argv) >= 2 else ''
listen_sock = create_socket(host, inet.PORT)

hall = Hall()
connection_list = []
connection_list.append(listen_sock)

while True:
    read_players, write_players, error_sockets = select.select(connection_list, [], [])
    for player in read_players:
        if player is listen_sock:
            new_socket, add = player.accept()
            new_player = Player(new_socket)
            connection_list.append(new_player)
            hall.welcome_new(new_player)

        else:
            msg = player.socket.recv(READ_BUFFER)
            if msg:
                msg = msg.decode().lower()
                hall.handle_msg(player, msg)
            else:
                player.socket.close()
                connection_list.remove(player)

    for sock in error_sockets:
        sock.close()
        connection_list.remove(sock)