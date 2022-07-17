import argparse
import socket
import sys
import terminalpy
import _thread

asciiArt = '''
             $$$$$$\    $$\                     $$\    $$\ 
            $$  __$$\   $$ |                    $$ |   $$ |
 $$$$$$\    $$ /  \__|  $$$$$$$\     $$$$$$\    $$ |   $$ |
$$  __$$\   \$$$$$$\    $$  __$$\   $$  __$$\   $$ |   $$ |
$$ |  \__|   \____$$\   $$ |  $$ |  $$$$$$$$ |  $$ |   $$ |
$$ |        $$\   $$ |  $$ |  $$ |  $$   ____|  $$ |   $$ |
$$ |        \$$$$$$  |  $$ |  $$ |  \$$$$$$$\   $$ |   $$ |
\__|         \______/   \__|  \__|   \_______|  \__|   \__|
'''

class rShell:
    def __init__(self, args):
        self.args = args

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.open:
            self.openListener()
        else:
            self.shell()

    def openListener(self):
        self.socket.bind((socket.gethostbyname(socket.gethostname()), self.args.port))
        print('[*] server open')
        print(f'[*] ip: {socket.gethostbyname(socket.gethostname())}')
        print(f'[*] port: {self.args.port}')
        self.socket.listen(5)

        while True:
            clientSocket, _ = self.socket.accept()
            _thread.start_new_thread(self.handle, (clientSocket,))

    def handle(self, client):
        cmdBuffer = b''

        terminal = terminalpy.Terminal(True)

        while True:
            try:
                client.send(b'CPY:')
                while '\n' not in cmdBuffer.decode():
                    cmdBuffer += client.recv(64)

                try:
                    response = terminal.type((cmdBuffer.decode())[0:-1])
                    response += '\n'
                except:
                    response = f'!!! [Error]: command `{cmdBuffer.decode()}` doesn\'t exists in this environment\n'

                    if cmdBuffer.decode() == 'cd ..\n' or cmdBuffer.decode() == '\n':
                        response = ''

                if response:
                    client.send(response.encode())
                response = ''

                cmdBuffer = b''
            except Exception as e:
                print(f'server killed {e}')
                self.socket.close()
                sys.exit()

    def shell(self):
        self.socket.connect((self.args.target, self.args.port))
        try:
            while True:
                recvLen = 1
                response = ''
                while recvLen:
                    data = self.socket.recv(4096)
                    recvLen = len(data)
                    response += data.decode()
                    if recvLen < 4096:
                        break
                if response:
                    print(response)
                    buffer = input(f'$ ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated')
            self.socket.close()
            sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='rShell tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('-t', '--target', help='Target IP')
    parser.add_argument('-p', '--port', type=int, default=1074 ,help='Specified port')
    parser.add_argument('-o', '--open', action='store_true', help='Open listener')
    parser.add_argument('-i', '--invisible', action='store_true', help='Execute in invisible mode')

    args = parser.parse_args()

    if not args.invisible:
        print(('Welcome to').center(57, ' '))
        print(asciiArt)
        print(("\..{|[<->_<'>]|}../").center(58, ' '))
        print('\nYour options: ')
        print('[1] <-> open rShell listener')
        print('[2] <-> connect to target')
        print('[3] <-> guide')
        mode = input('Select mode: ')
        if mode == '1':
            port = input('  Select port: ')
            args.port = int(port)
            args.target = None
            args.open = True
            rs = rShell(args)
            rs.run()
        elif mode == '2':
            target = input('  Insert target: ')
            port = input('  Insert port: ')
            args.port = int(port)
            args.target = target
            args.open = False
            rs = rShell(args)
            rs.run()
        elif mode == '3':
            print('''
    Mode 1:
        You are required to select a port. After that, rShell will start in listen mode,
        and will accept incoming connections from another rShell session
            
    Mode 2:
        You are required to insert target's ip and port. After that, you will connect to 
        rShell listener (if open), and you'll be able to interact with target's terminal
                
    Mode 3:
        Show this message
        
    Invisible mode examples:
        $ rshell -o -p 1074 -i              # opens listener 
        $ rshell -t 127.0.0.1 -p 1074 -i    # connects to target and access terminal
    
    For invisible mode help:
        $ rshell --help
        
        Output:
            usage: rshell [-h] [-t TARGET] [-p PORT] [-o] [-i]

            rShell tool

            options:
                -h, --help            show this help message and exit
                -t TARGET, --target TARGET
                                      Target IP
                -p PORT, --port PORT  Specified port
                -o, --open            Open listener
                -i, --invisible       Execute in invisible mode
    \..{|[<->_<'>]|}../
''')
    else:
        rs = rShell(args)
        rs.run()
        
#\..{|[<->_<'>]|}../#
