#Client

import socket
import Screen_Client


class Client (object):

    def __init__(self, ip, port):
        self.ip = ip #the server's ip
        self.port = port #the server's port

    def start(self):
        """
        This functions starts the connection of the client to the server
        """
        try:
            print('connecting to ip %s port %s' % (ip, port))
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            print('connected to server')
            s = Screen_Client.screen_client(sock)
            s.welcome_screen()

            while True:
                self.handleServerJob(sock)
        except socket.error as e:
            print("No server is waiting...")



    def handleServerJob(self, serverSocket):
        while True:
            pass


if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    #ip = '127.0.0.1'
    #ip = '192.168.1.246'
    port = 1740
    c = Client(ip, port)
    c.start()