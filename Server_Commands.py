
import users_database
import qa_database
import qa_database2
import tkinter as tk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import hashlib




class Commands:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.u = users_database.Users()  # users database
        self.q1 = qa_database.Questions_and_Answers()  # first set of questions ans answers
        self.q2 = qa_database2.Questions_and_Answers()  # second set of questions and answers

    def encrypt(self, password):
        """
            This function encrypts the given password
            :param password: The password entered by the user
            :return: Encrypted password
        """
        encrypted_pass = hashlib.sha256(str.encode(password)).hexdigest()
        return encrypted_pass

    def adding_user(self, x_p, y_p, names_of_users, list_w, root, list_all_names):
        """
            This function adds new participent to the game
            :param x_p: The user name's x position on the screen
            :param y_p: The user name's y position on the screen
            :param names_of_users: The usernames list
            :param list_w: The list of labels
            :param root: The screen
            :param list_all_names: The usernames list
        """

        self.client_socket.sendall(str.encode('ready'))
        details = self.client_socket.recv(1024).decode().split('#')
        username = details[0]
        password = details[1]
        email = details[2]
        if self.u.check_username(username) == True and self.u.check_email(email) == True:
            self.u.insert_user(username, self.encrypt(password), email, 0, 1)
            names_of_users.append(username)
            if len(list_w) == 1:
                list_w[0].destroy()
            user_label = tk.Label(root, text=username, font=('Arial Black', 16), fg="Sienna", bg='white')
            user_label.place(x=x_p, y=y_p)
            list_all_names.append(user_label)
            print('done with adding current user')
            print()
        else:
            if self.u.check_username(username) == False:
                self.client_socket.sendall(str.encode('username'))
            if self.u.check_email(email) == False:
                self.client_socket.sendall(str.encode('email'))
            print('something went wrong in adding')


    def checking_email_code(self, x_p, y_p, username, names_of_users, list_w, root, list_all_names):
        """
            This function checks if the code that the user inserted is correct
            :param x_p: The user name's x position on the screen
            :param y_p: The user name's y position on the screen
            :param username: The user's username
            :param names_of_users: The usernames list
            :param list_w: The list of labels
            :param root: The screen
            :param list_all_names: The usernames list
            """
        sender_email = "trivi.projectt@gmail.com"
        password = "trivi@pro"
        rec_email = self.u.get_email_of_user(username)

        subject = "TRIVI - Your Login Code"
        first = random.randint(1, 9) * 100
        second = random.randint(1, 9) * 10
        third = random.randint(1, 9)
        sum = first + second + third
        code = str(sum)
        message = "Hi, Your Login code is:  " + code

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = rec_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        print("Login success")

        text = msg.as_string()
        server.sendmail(sender_email, rec_email, text)

        server.quit()

        print("Email has been sent to ", rec_email)

        client_code = self.client_socket.recv(1024).decode()
        if client_code == code:
            names_of_users.append(username)
            if len(list_w) == 1:
                list_w[0].destroy()
            user_label = tk.Label(root, text=username, font=('Arial Black', 16), fg="Sienna", bg='white')
            user_label.place(x=x_p, y=y_p)
            list_all_names.append(user_label)
            self.u.change_user_position_start(username)
            self.u.reset_score(username)
            print('done with adding current user')
            print()
        else:
            self.client_socket.sendall(str.encode('try again'))

    def checking_user(self, x_p, y_p, names_of_users, list_w, root, list_all_names):
        """
            This function checks if the user's sign in details are correct
            :param x_p: The user name's x position on the screen
            :param y_p: The user name's y position on the screen
            :param names_of_users: The usernames list
            :param list_w: The list of labels
            :param root: The screen
            :param list_all_names: The usernames list
            """
        self.client_socket.sendall(str.encode('ready'))
        details = self.client_socket.recv(1024).decode().split('#')
        print("in checking user    ", details)
        username = details[0]
        password = details[1]
        if self.u.check_username(username) == False:
            password_in_database = self.u.get_user_password(username)
            print('users position  ', self.u.get_users_position(username))
            if password_in_database == self.encrypt(password) and not self.u.is_user_in_the_game(username):
                self.client_socket.sendall(str.encode('email'))
                self.checking_email_code(x_p, y_p, username, names_of_users,list_w, root, list_all_names)
            else:
                if self.u.is_user_in_the_game(username):
                    self.client_socket.sendall(str.encode('player'))
                    print('in the game')
                else:
                    self.client_socket.sendall(str.encode('password'))
                    print('wrong password')
        else:
            self.client_socket.sendall(str.encode('username'))
            print('username does not exist')

    def update_user_password(self):
        """
        This function updates the user's password into a new one
        """
        self.client_socket.sendall(str.encode('ready'))
        details = self.client_socket.recv(1024).decode().split('#')
        print(details)
        username = details[0]
        password = details[1]
        self.u.update_password(username, self.encrypt(password))
        self.client_socket.sendall(str.encode('updated'))
        print('the new password:   ', self.u.get_user_password(username))
        print('password updated in server')

    def client_log_out( self, list_all_clients, username):
        """
        This function takes user out of the game
        :param list_all_clients: List of all of the users
        :param username: User's username
        """
        self.u.cahnge_user_position(username)
        print('length of list before removing:  ', len(list_all_clients))
        list_all_clients.remove(self.client_socket)
        print('length of list after removing:  ', len(list_all_clients))
        self.client_socket.sendall(str.encode('operation done successfully'))
        print('username on log out:   ', username)
        self.u.get_users_position(username)
