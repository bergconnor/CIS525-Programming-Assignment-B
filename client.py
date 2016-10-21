import sys
import socket
import select
import string
import inet

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()
 
if __name__ == "__main__":
    try:
        name          = ''
        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE    = '\x1b[2K'
    
        while True:
            response = raw_input('\r' + '<SYSTEM> ' + 'Would you like to connect to the chat room? Enter (Y)es or (N)o: ')
            if len(response) > 0:
                response = response.lower()[0]
            else:
                print('\r' + '<SYSTEM> ' + 'Invalid input.')
                continue
            if response == 'y':
                print('\r' + '<SYSTEM> ' + 'Connecting...')
                break
            elif response == 'n':
                print('\r' + '<SYSTEM> ' + 'Exiting...')
                sys.exit(0)
            else:
                print('\r' + '<SYSTEM> ' + 'Invalid input.') 
                continue
         
        host = socket.gethostname()
        port = int(inet.PORT)
    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
         
        try :
            s.connect((host, port))
        except :
            print('\r' + '<SYSTEM> ' + 'Unable to connect')
            sys.exit()
         
        # print('Connected to remote host. Start sending messages')
        print('\r' + '<SYSTEM> ' + 'Connected to chat room.')
        message = s.recv(inet.RX_BUF_SZ)
    	name = raw_input(message)
    	s.send(name)
        '''
        while True:
        	message = s.recv(inet.RX_BUF_SZ)
        	name = raw_input(message)
        	s.send(name)
    		response = s.recv(inet.RX_BUF_SZ)

    		if response == 'valid':
    			break
    		else:
    			print('\r' + response)
    			continue
    	'''

        prompt()
         
        while True:
            socket_list = [sys.stdin, s]
    
            rx_sockets, tx_sockets, error_sockets = select.select(socket_list , [], [])
             
            for sock in rx_sockets:
                #incoming message from remote server
                if sock == s:
                    data = sock.recv(inet.RX_BUF_SZ)
                    if not data :
                        print('\r' + '<SYSTEM> ' + 'Disconnected from chat server')
                        sys.exit()
                    else :
                        #print data
                        print(ERASE_LINE + CURSOR_UP_ONE)
                        sys.stdout.write(data)
                        prompt()
                 
                #user entered a message
                else :
                    msg = sys.stdin.readline()
                    s.send(msg)
                    prompt()
    except KeyboardInterrupt:
        print('\r' + '<SYSTEM> ' + 'KeyboardInterrupt bitches')
                