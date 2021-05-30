#Server

import socket
import threading
import users_database
import qa_database
import qa_database2
import tkinter as tk
import Screen_Server
from Server_Commands import Commands




global root,list_w, list_all_names, names_of_users


u = users_database.Users() #users database
q1 = qa_database.Questions_and_Answers() #first set of questions ans answers
q2 = qa_database2.Questions_and_Answers() #second set of questions and answers


class Server(object):

    def __init__(self, ip, port):
        self.ip = ip #server's ip
        self.port = port #server's port
        self.count = 0 #number of players at the moment
        self.x_p = 100 #the first x position of a player's name on the screen
        self.y_p = 250 #the first x position of a player's name on the screen
        self.allclients = [] # list of all clients sockets
        self.server_sock = None
        self.flag = True

    def getallclients(self):
        """
        This function returns the list of all clients sockets
        :return: all clients sockets
        """
        return self.allclients

    def start(self):
        """
        This function starts the connection of the server with the clients
        """

        try:
           print('server starts up on ip %s port %s' % (self.ip, self.port))
           sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           sock.bind((self.ip, self.port))
           sock.listen(1)

           self.server_sock = sock

           while self.flag:
                print('waiting for a new client')
                clientSocket, client_address = sock.accept()
                print('new client entered')
                self.count += 1
                self.allclients.append(clientSocket)
                print(self.count)
                self.handleClient(clientSocket, self.count)
        except socket.error as e:
            print(e)

    def handleClient(self, clientSock, current):
        print ("hello")
        client_handler = threading.Thread(target=self.handle_client_connection, args=(clientSock, current,))
        client_handler.demon = True
        client_handler.start()

    def handle_client_connection(self, client_socket, current):
        """
        This function takes care of the users requests
        :param client_socket: The client's socket
        """
        commands = Commands(client_socket)
        while self.flag:
            request = client_socket.recv(1024).decode().lower()
            print(request)

            if request == 'add':
                commands.adding_user( self.x_p, self.y_p, names_of_users, list_w, root, list_all_names)
                self.y_p = self.y_p + 50

            if request == 'answer':
                client_socket.sendall(str.encode('send'))
                client_answer = client_socket.recv(1024).decode().split("#")
                print(client_answer)
                number = int(client_answer[0])
                if number == start_screens.get_correct_answer_num():
                    u.update(client_answer[1],int(client_answer[2]))
                    client_socket.sendall(str.encode('correct'))
                else:
                    client_socket.sendall(str.encode('wrong'))

            if request == 'check':
                commands.checking_user( self.x_p, self.y_p, names_of_users, list_w, root, list_all_names)
                self.y_p = self.y_p + 50

            if request == 'update':
                commands.update_user_password()


            if request == 'log out':
                client_socket.sendall(str.encode('send'))
                client_username = client_socket.recv(1024).decode()
                print(client_username)
                commands.client_log_out(self.allclients, client_username)
                break

    def get_server_socket(self):
        return self.server_sock

    def get_flag(self):
        self.flag = False

    def update_start(self):
        self.x_p = 100
        self.y_p = 250



if __name__ == '__main__':
    ip = '0.0.0.0'
    port = 1740
    server = Server(ip, port)
    list_w = []
    list_all_names = []
    names_of_users = []
    position = ''
    all_questions1 = q1.get_questions_and_answers()
    all_questions2 = q2.get_questions_and_answers()
    root = tk.Tk()
    start_screens = Screen_Server.screen_server(u, server, list_w, all_questions1, names_of_users, all_questions2)
    start_screens.start(root, server, tk, list_w, list_all_names, all_questions1, names_of_users, all_questions2)