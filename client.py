import sys
import socket
import select
import string
from inet import PORT, RX_BUF_SZ, SERVER

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()
 
if __name__ == "__main__":
    try:
        name          = ''
        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE    = '\x1b[2K'
    
        while True:
            response = raw_input(SERVER + 'Would you like to connect to the chat room? Enter (Y)es or (N)o: ')
            if len(response) > 0:
                response = response.lower()[0]
            else:
                print(SERVER + 'Invalid input.')
                continue
            if response == 'y':
                print(SERVER + 'Connecting...')
                break
            elif response == 'n':
                print(SERVER + 'Exiting...')
                sys.exit(0)
            else:
                print(SERVER + 'Invalid input.') 
                continue
         
        host = socket.gethostname()
        port = int(PORT)
    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(30)
         
        try :
            s.connect((host, port))
        except :
            print(SERVER + 'Unable to connect')
            sys.exit()
         
        print(SERVER + 'Connected to chat room.')        
        message = s.recv(RX_BUF_SZ)
        name = raw_input(message)
        s.send(name)

        while True:
            response = s.recv(RX_BUF_SZ)
            if response == 'valid':
                break
            else:
                name = raw_input(response)
                s.send(name)
                continue        

        prompt()
         
        while True:
            socket_list = [sys.stdin, s]
    
            rx_sockets, tx_sockets, error_sockets = select.select(socket_list , [], [])
             
            for sock in rx_sockets:
                #incoming message from remote server
                if sock == s:
                    data = sock.recv(RX_BUF_SZ)
                    if not data :
                        print(ERASE_LINE + CURSOR_UP_ONE)
                        print(SERVER + 'The chat room has closed.')
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
        print(SERVER + 'KeyboardInterrupt bitches')
                