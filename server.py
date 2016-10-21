import socket
import select
import inet
 
def broadcast(sock, message):

    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)
                index = CONNECTION_LIST.index(socket)
                NAMES_LIST.remove(index)
 

if __name__ == '__main__':
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    NAMES_LIST      = []
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', inet.PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
    NAMES_LIST.append('Server')
 
    print('\r' + '<SYSTEM> ' + 'Chat server started on port ' + str(inet.PORT))
 
    while True:
        # Get the list sockets which are ready to be read through select
        rx_sockets, tx_sockets, error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in rx_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)

                sockfd.send('<SYSTEM> Enter a nickname: ')
                name = sockfd.recv(inet.RX_BUF_SZ)
                NAMES_LIST.append(name)
                '''
                while True:
                    sockfd.send('<SYSTEM> Enter a nickname: ')
                    name = sockfd.recv(inet.RX_BUF_SZ)
                    if name in NAMES_LIST:
                        sockfd.send('<SYSTEM> This nickname is already in use.')
                        continue
                    else:
                        NAMES_LIST.append(name)
                        sockfd.send('valid')
                        break
                '''

                print('\r' + '<SYSTEM> ' + '{0} connected'.format(name))
                 
                broadcast(sockfd, '<SYSTEM> {0} entered room\n'.format(name))
             
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
            	index = CONNECTION_LIST.index(sock)
                # try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                data = sock.recv(inet.RX_BUF_SZ)
                if data:
                    broadcast(sock, '\r' + '<' + NAMES_LIST[index] + '> ' + data)
                else:
                	CONNECTION_LIST.remove(sock)
                	# NAMES_LIST.remove(index)
                	broadcast(sock, '\r' + '<SYSTEM> ' + NAMES_LIST[index] + ' has left the chat room.\n')  
                	print('\r' + '<SYSTEM> ' + NAMES_LIST[index] + ' has left the chat room.')             
                ''' 	
                except:
                    broadcast(sock, '{0} has left the room'.format(NAMES_LIST[index]))
                    print('{0} has left the room'.format(NAMES_LIST[index]))
                    sock.close()
	                CONNECTION_LIST.remove(sock)
	                NAMES_LIST.remove(index)
                    continue
     			'''
    server_socket.close()