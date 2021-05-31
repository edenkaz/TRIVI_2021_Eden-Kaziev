import tkinter as tk
from tkinter.messagebox import *
import time
import clock_try
import threading
import os


class screen_client:

    def __init__(self, serversocket):
        self.root = tk.Tk()  # the screen
        self.list_w = []  # the list of the widgets on the screen
        self.serversocket = serversocket  # the server's socket
        self.username = ""  # the user's username
        self.start_time = 0.0  # the start time
        self.end_time = 0.0  # the end time
        self.current_question_num = 1  # the current question number


    def get_final_score(self, total_time):
        """
        This function returns the player's score after every question according to his time
        :param total_time: The time it takes for a player to choose an answer
        :return: The player's final score after the question
        """
        score = (1 - (total_time / 30 / 2)) * 1000
        print(score)
        arr = str(score).split('.')
        final_score = int(arr[0])
        first_digit = int(arr[1][0])
        if first_digit >= 5 and first_digit <= 9:
            final_score = final_score + 1
        return final_score

    def clock_screen(self):
        """
        This function shows the game screen for the player that dud not answer in the given time
        """
        time.sleep(30)
        if not self.is_empty():
            self.removing_widget()
        if self.end_time == 0.0:
            position_label = tk.Label(self.root, text="TIME IS UP", font=('Eras Bold ITC', 30), fg="Sienna")
            position_label.place(x=300, y=200)
            self.list_w.append(position_label)
            self.placing_buttons()


    def on_quit_end(self):
        self.serversocket.send(str.encode('log out'))

    def placing_buttons(self):
        """
        This function places the buttons and stops the timer after each question
        """
        if self.end_time != 0.0:
            total_time = self.end_time - self.start_time
            time.sleep(30 - total_time)
        if not self.is_empty():
            self.removing_widget()
        self.current_question_num = self.current_question_num + 1
        if self.current_question_num == 11:
            position_label = tk.Label(self.root, text="GAME OVER", font=('Arial Black', 16), fg="Sienna", bg='white')
            position_label.place(x=250, y=200)
            self.list_w.append(position_label)
            self.home_button()
            log_out_b = tk.Button(self.root, text="log out", command=self.on_quit_end, font=('Arial Black', 14),
                           fg="Sienna", bg='white')
            log_out_b.place(x=620, y=70)
            self.list_w.append(log_out_b)
            message = self.serversocket.recv(1024).decode()
            print('After GAME OVER message:    ', message)
            if message == 'server closed the game':
                print('quit program1')
                self.serversocket.close()
                print('quit program2')
                self.root.destroy()
                print('quit program3')

            if message == 'server decided to continue the game':
                pass

            if message == 'send':
                self.serversocket.send(str.encode(self.username))
                reply = self.serversocket.recv(1024).decode()
                print('reply on_quit:    ', reply)
                if reply == 'operation done successfully':
                    self.root.destroy()



        else:
            self.serversocket.send(str.encode('are you ready to start'))
            pos = self.serversocket.recv(1024).decode()
            print(pos)
            if pos == 'game starts':
                if not self.is_empty():
                    self.removing_widget()

                todo_label = tk.Label(self.root, text="Press the correct answer number", font=('Arial Black', 13),
                                      fg="Sienna", bg='white')
                todo_label.place(x=250, y=200)
                self.list_w.append(todo_label)

                # first option button
                btn1 = tk.Button(self.root, text="1", command=self.button_one, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn1.place(x=270, y=250)
                self.list_w.append(btn1)

                # second option button
                btn2 = tk.Button(self.root, text="2", command=self.button_two, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn2.place(x=270, y=380)
                self.list_w.append(btn2)

                # third option button
                btn3 = tk.Button(self.root, text="3", command=self.button_three, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn3.place(x=450, y=250)
                self.list_w.append(btn3)

                # fourth option button
                btn4 = tk.Button(self.root, text="4", command=self.button_four, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn4.place(x=450, y=380)
                self.list_w.append(btn4)

                self.start_time = time.perf_counter()
                self.end_time = 0.0

                # creating the clock
                clock = clock_try.clock_try(self.root)
                clock.start_clock()
                thread_for_clock = threading.Thread(target=self.clock_screen)
                thread_for_clock.daemon = True
                thread_for_clock.start()

    def removing_widget(self):
        """
        This function removes all of the widgets in the list from the screen
        """
        for i in range(len(self.list_w)):
            self.list_w[i].destroy()
        del self.list_w[:]

    def is_empty(self):
        """
        This function check if the widgets list is empty
        :return: If the list is empty it returns True else it returns False
        """
        if len(self.list_w) == 0:
            return True
        return False

    def home_button(self):
        """
        This function shows the main screen for the player
        """
        home = tk.Button(self.root, text="Home", command=self.welcome_screen, font=('Arial Black', 16),
                         fg="Sienna", bg='white')
        home.pack()
        home.place(x=620, y=10)
        self.list_w.append(home)

    def button_one(self, *therest):
        """
        This function sends the user's answer to the server after he pressed the first button
        :param therest: All other parameters
        """
        self.end_time = time.perf_counter()
        total_time = self.end_time - self.start_time
        print(total_time)
        points_to_add = self.get_final_score(total_time)
        self.serversocket.send(str.encode('answer'))
        pos = self.serversocket.recv(1024).decode()
        print(pos)
        if pos == 'send':
            my_answer = "1#" + self.username + "#" + str(points_to_add)
            self.serversocket.send(str.encode(my_answer))
            if self.serversocket.recv(1024).decode() == 'correct':
                if not self.is_empty():
                    self.removing_widget()
                position_label = tk.Label(self.root, text="CORRECT", font=('Arial Black', 30), fg="Sienna", bg='white')
                position_label.place(x=250, y=200)
                self.list_w.append(position_label)

            else:
                if not self.is_empty():
                    self.removing_widget()
                position_label = tk.Label(self.root, text="INCORRECT", font=('Arial Black', 30), fg="Sienna",
                                          bg='white')
                position_label.place(x=250, y=200)
                self.list_w.append(position_label)

            thread_for_buttons = threading.Thread(target=self.placing_buttons, args=())
            thread_for_buttons.demon = True
            thread_for_buttons.start()

        pass

    def button_two(self, *therest):
        """
        This function sends the user's answer to the server after he pressed the second button
        :param therest: All other parameters
        """
        self.end_time = time.perf_counter()
        total_time = self.end_time - self.start_time
        print(total_time)
        points_to_add = self.get_final_score(total_time)
        self.serversocket.send(str.encode('answer'))
        pos = self.serversocket.recv(1024).decode()
        if pos == 'send':
            my_answer = "2#" + self.username + "#" + str(points_to_add)
            self.serversocket.send(str.encode(my_answer))
            if self.serversocket.recv(1024).decode() == 'correct':
                if not self.is_empty():
                    self.removing_widget()
                position_label = tk.Label(self.root, text="CORRECT", font=('Eras Bold ITC', 30), fg="Sienna")
                position_label.place(x=300, y=200)
                self.list_w.append(position_label)
                pass
            else:
                if not self.is_empty():
                    self.removing_widget()
                position_label = tk.Label(self.root, text="INCORRECT", font=('Eras Bold ITC', 30), fg="Sienna")
                position_label.place(x=300, y=200)
                self.list_w.append(position_label)

            Thread_for_buttons = threading.Thread(target=self.placing_buttons, args=())
            Thread_for_buttons.daemon = True
            Thread_for_buttons.start()

        pass

    def button_three(self, *therest):
        """
        This function sends the user's answer to the server after he pressed the third button
        :param therest: All other parameters
        """
        self.end_time = time.perf_counter()
        total_time = self.end_time - self.start_time
        print(total_time)
        points_to_add = self.get_final_score(total_time)
        self.serversocket.send(str.encode('answer'))
        pos = self.serversocket.recv(1024).decode()
        if pos == 'send':
            my_answer = "3#" + self.username + "#" + str(points_to_add)
            self.serversocket.send(str.encode(my_answer))
            if self.serversocket.recv(1024).decode() == 'correct':
                if not self.is_empty():
                    self.removing_widget()
                position_label = tk.Label(self.root, text="CORRECT", font=('Eras Bold ITC', 30), fg="Sienna")
                position_label.place(x=300, y=200)
                self.list_w.append(position_label)
                pass
            else:
                if not self.is_empty():
                    self.removing_widget()
                position_label = tk.Label(self.root, text="INCORRECT", font=('Eras Bold ITC', 30), fg="Sienna")
                position_label.place(x=300, y=200)
                self.list_w.append(position_label)

            Thread_for_buttons = threading.Thread(target=self.placing_buttons, args=())
            Thread_for_buttons.daemon = True
            Thread_for_buttons.start()
        pass

    def button_four(self, *therest):
        """
        This function sends the user's answer to the server after he pressed the fourth button
        :param therest: All other parameters
        """
        self.end_time = time.perf_counter()
        total_time = self.end_time - self.start_time
        print(total_time)
        points_to_add = self.get_final_score(total_time)
        self.serversocket.send(str.encode('answer'))
        pos = self.serversocket.recv(1024).decode()
        if pos == 'send':
            my_answer = "4#" + self.username + "#" + str(points_to_add)
            self.serversocket.send(str.encode(my_answer))
            if self.serversocket.recv(1024).decode() == 'correct':
                if not self.is_empty():
                    self.removing_widget()
                position_label = tk.Label(self.root, text="CORRECT", font=('Eras Bold ITC', 30), fg="Sienna")
                position_label.place(x=300, y=200)
                self.list_w.append(position_label)
                pass
            else:
                if not self.is_empty():
                    self.removing_widget()
                position_label = tk.Label(self.root, text="INCORRECT", font=('Eras Bold ITC', 30), fg="Sienna")
                position_label.place(x=300, y=200)
                self.list_w.append(position_label)

            Thread_for_buttons = threading.Thread(target=self.placing_buttons, args=())
            Thread_for_buttons.daemon = True
            Thread_for_buttons.start()
        pass

    def message_for_exist(self, reply):
        """
        This function handles the communication betweeen the client and the server until game starts
        :param reply: The reply from the server
        """
        if reply == 'try again':
            showinfo("MESSAGE", "Wrong code Please sign in again")
            self.sign_in()
        else:
            print('pos in else')
            if reply == 'game starts':
                title = 'TRIVI Game - ' + self.username
                self.root.title(title)
                # self.root.title("TRIVI Game - Player")
                print('pos in else')
                if not self.is_empty():
                    self.removing_widget()

                self.home_button()
                todo_label = tk.Label(self.root, text="Press the correct answer number", font=('Arial Black', 13),
                                      fg="Sienna",
                                      bg='white')
                todo_label.place(x=250, y=200)
                self.list_w.append(todo_label)

                # first option button
                btn1 = tk.Button(self.root, text="1", command=self.button_one, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn1.place(x=270, y=250)
                self.list_w.append(btn1)

                # second option button
                btn2 = tk.Button(self.root, text="2", command=self.button_two, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn2.place(x=270, y=380)
                self.list_w.append(btn2)

                # third option button
                btn3 = tk.Button(self.root, text="3", command=self.button_three, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn3.place(x=450, y=250)
                self.list_w.append(btn3)

                # fourth option button
                btn4 = tk.Button(self.root, text="4", command=self.button_four, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn4.place(x=450, y=380)
                self.list_w.append(btn4)

                self.start_time = time.perf_counter()

                # creating the clock
                clock = clock_try.clock_try(self.root)
                clock.start_clock()
                thread_for_clock = threading.Thread(target=self.clock_screen)
                thread_for_clock.daemon = True
                thread_for_clock.start()

    def message_for_new(self, answer):
        """
        This function handles the communication betweeen the client and the server until game starts
        :param answer: The answer from the server
        """
        pos = self.serversocket.recv(1024).decode()
        while pos == None:
            pos = self.serversocket.recv(1024).decode()
        print('returns:      ', pos)
        answer += pos
        if answer == 'username':
            print('wrong username')
            showinfo("MESSAGE", "This username exists Try again")
            self.sign_up()
        if answer == 'email':
            print('wrong email')
            showinfo("MESSAGE", "This email exists Try again")
            self.sign_up()

        else:
            title = 'TRIVI Game - ' + self.username
            self.root.title(title)
            # self.root.title("TRIVI Game - Player")
            print('pos in else')
            if answer == 'game starts':
                print('pos in else')
                if not self.is_empty():
                    self.removing_widget()

                # self.home_button()
                todo_label = tk.Label(self.root, text="Press the correct answer number", font=('Arial Black', 13),
                                      fg="Sienna",
                                      bg='white')
                todo_label.place(x=250, y=200)
                self.list_w.append(todo_label)

                # first option button
                btn1 = tk.Button(self.root, text="1", command=self.button_one, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn1.place(x=270, y=250)
                self.list_w.append(btn1)

                # second option button
                btn2 = tk.Button(self.root, text="2", command=self.button_two, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn2.place(x=270, y=380)
                self.list_w.append(btn2)

                # third option button
                btn3 = tk.Button(self.root, text="3", command=self.button_three, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn3.place(x=450, y=250)
                self.list_w.append(btn3)

                # fourth option button
                btn4 = tk.Button(self.root, text="4", command=self.button_four, font=('Arial Black', 16),
                               fg="Sienna", bg='white')
                btn4.place(x=450, y=380)
                self.list_w.append(btn4)

                self.start_time = time.perf_counter()

                # creating the clock
                clock = clock_try.clock_try(self.root)
                clock.start_clock()
                thread_for_clock = threading.Thread(target=self.clock_screen)
                thread_for_clock.daemon = True
                thread_for_clock.start()

    def validatelogin(self, username, password, email):
        """
        This function validates the user's username and password from the sign up screen and when it is approved the game starts
        :param username: The user's username
        :param password: The user's password
        :param email: The user's email
        """
        self.username = username.get()
        print("username entered :", username.get())
        print("password entered :", password.get())
        print("email entered :", email.get())
        self.serversocket.send(str.encode('add'))
        pos = self.serversocket.recv(1024).decode()
        if pos == 'ready':
            details = username.get() + '#' + password.get() + '#' + email.get()
            self.serversocket.send(str.encode(details))
            answer = ""
            connection = threading.Thread(target=self.message_for_new, args=(answer, ), daemon=True)
            connection.start()

    def code_sending(self, code):
        """
        This function shows the screen of the second validation of the user by his email and when it is correct the game starts
        :param code: The code that the user entered
        """
        if not self.is_empty():
            self.removing_widget()

        # number_code = code.get()
        number_code = code
        self.serversocket.send(str.encode(number_code))
        reply = ""
        connection = threading.Thread(target=self.message_for_new, args=(reply,), daemon=True)
        connection.start()


    def validatelogin_forexists(self, username, password, *therest):
        """
        This function validates the user's username and password from the sign in screen
        :param username: The user's username
        :param password: The user's password
        :param therest: All other parameters
        :return:
        """
        self.username = username.get()
        print("username entered :", username.get())
        print("password entered :", password.get())
        print(username, password)
        self.serversocket.send(str.encode('check'))
        pos = self.serversocket.recv(1024).decode()
        if pos == 'ready':
            details = username.get() + '#' + password.get()
            self.serversocket.send(str.encode(details))
            answer = self.serversocket.recv(1024).decode()
            print(answer)
            if answer == 'username':
                print('wrong username')
                showinfo("MESSAGE", "This username does not exist Try again")
                self.sign_in()
            elif answer == 'password' :
                print('wrong password ')
                showinfo("MESSAGE", "wrong password Try again")
                self.sign_in()
            elif answer == 'player':
                print('player is already in the game')
                showinfo("MESSAGE", "Your user is already in the game Please sign in from another user")
                self.sign_in()

            else:
                if not self.is_empty():
                    self.removing_widget()

                self.root.title("TRIVI Game - Code - Player")

                code_label = tk.Label(self.root, text="Enter the code", font=('Arial Black', 13), fg="Sienna",
                                      bg='white')
                code_label.place(x=150, y=200)
                code = tk.StringVar()
                codeEntry = tk.Entry(self.root, textvariable=code, font=('Arial Black', 13), fg="Sienna")
                codeEntry.place(x=300, y=200)
                self.list_w.append(code_label)
                self.list_w.append(codeEntry)

                login = tk.Button(self.root, text="Enter", command=lambda: self.code_sending(codeEntry.get()),
                                  font=('Arial Black', 13),
                                  fg="Sienna", bg='white')
                login.place(x=650, y=300)
                self.list_w.append(login)

    def send_new_password(self, username, password):
        """
        This function sends the user's new password for the server to update it in the database
        :param username: The user's username
        :param password: The user's new password
        """
        self.serversocket.send(str.encode('update'))
        pos = self.serversocket.recv(1024).decode()
        if pos == 'ready':
            # details = username.get() + '#' + password.get()
            details = username + '#' + password
            self.serversocket.send(str.encode(details))
            answer = self.serversocket.recv(1024).decode()
            print(answer)
            if answer == 'updated':
                if not self.is_empty():
                    self.removing_widget()

                position = tk.Label(self.root, text="operation done", font=('Arial Black', 13), fg="Sienna",
                                    bg='white')
                position.place(x=150, y=200)
                self.list_w.append(position)

                login = tk.Button(self.root, text="go to sign in", command=self.sign_in, font=('Arial Black', 13),
                                  fg="Sienna", bg='white')
                login.place(x=650, y=300)
                self.list_w.append(login)

    def create_password(self):
        """
        This function shows the screen for existing users who forgot their password
        """
        if not self.is_empty():
            self.removing_widget()
        self.root.title("TRIVI Game - Update password - Player")

        home_button = tk.Button(self.root, text="Home", command=self.welcome_screen, font=('Arial Black', 13),
                                fg="Sienna", bg='white')
        home_button.place(x=50, y=20)
        self.list_w.append(home_button)

        username_label = tk.Label(self.root, text="User Name", font=('Arial Black', 13), fg="Sienna", bg='white')
        username_label.place(x=150, y=200)
        username = tk.StringVar()
        usernameEntry = tk.Entry(self.root, textvariable=username, font=('Arial Black', 13), fg="Sienna")
        usernameEntry.place(x=300, y=200)
        self.list_w.append(username_label)
        self.list_w.append(usernameEntry)

        password_label = tk.Label(self.root, text="Password", font=('Arial Black', 13), fg="Sienna", bg='white')
        password_label.place(x=150, y=300)
        password = tk.StringVar()
        passwordentry = tk.Entry(self.root, textvariable=password, font=('Arial Black', 13), fg="Sienna",
                                 show='*')
        passwordentry.place(x=300, y=300)
        self.list_w.append(password_label)
        self.list_w.append(passwordentry)

        # self.send_new_password = partial(self.send_new_password, username, password)
        login = tk.Button(self.root, text="Update",
                          command=lambda: self.send_new_password(usernameEntry.get(), passwordentry.get()),
                          font=('Arial Black', 13),
                          fg="Sienna", bg='white')

        login.place(x=650, y=300)
        self.list_w.append(login)

    def sign_in(self):
        """
        This function shows the sign in screen for exists users
        """
        self.current_question_num = 1
        if not self.is_empty():
            self.removing_widget()
        self.root.title("TRIVI Game - Sign In - Player")

        home_button = tk.Button(self.root, text="Home", command=self.welcome_screen, font=('Arial Black', 13),
                                fg="Sienna", bg='white')
        home_button.place(x=50, y=20)
        self.list_w.append(home_button)

        username_label = tk.Label(self.root, text="User Name", font=('Arial Black', 13), fg="Sienna", bg='white')
        username_label.place(x=150, y=200)
        username = tk.StringVar()
        usernameEntry = tk.Entry(self.root, textvariable=username, font=('Arial Black', 13), fg="Sienna")
        print("entry: ", usernameEntry)
        usernameEntry.place(x=300, y=200)
        self.list_w.append(username_label)
        self.list_w.append(usernameEntry)

        password_label = tk.Label(self.root, text="Password", font=('Arial Black', 13), fg="Sienna", bg='white')
        password_label.place(x=150, y=300)
        password = tk.StringVar()
        passwordentry = tk.Entry(self.root, textvariable=password, font=('Arial Black', 13), fg="Sienna",
                                 show='*')
        passwordentry.place(x=300, y=300)
        self.list_w.append(password_label)
        self.list_w.append(passwordentry)

        login = tk.Button(self.root, text="Login",
                          command=lambda: self.validatelogin_forexists(usernameEntry, passwordentry),
                          font=('Arial Black', 13),
                          fg="Sienna", bg='white')
        login.place(x=650, y=300)
        self.list_w.append(login)

        forgot_password = tk.Button(self.root, text="Forgot password", command=self.create_password,
                                    font=('Arial Black', 13),
                                    fg="Sienna", bg='white')
        forgot_password.place(x=600, y=400)
        self.list_w.append(forgot_password)

    def sign_up(self):
        """
        This function shows the sign up screen for new players
        """
        self.current_question_num = 1
        print("in sign up")

        if not self.is_empty():
            self.removing_widget()
        self.root.title("TRIVI Game - Sign Up - Player")

        home_button = tk.Button(self.root, text="Home", command=self.welcome_screen, font=('Arial Black', 13),
                                fg="Sienna", bg='white')
        home_button.place(x=50, y=20)
        self.list_w.append(home_button)

        username_label = tk.Label(self.root, text="User Name", font=('Arial Black', 13), fg="Sienna", bg='white')
        username_label.place(x=150, y=200)
        username = tk.StringVar()
        usernameEntry = tk.Entry(self.root, textvariable=username, font=('Arial Black', 13), fg="Sienna")
        usernameEntry.place(x=300, y=200)
        self.list_w.append(username_label)
        self.list_w.append(usernameEntry)

        password_label = tk.Label(self.root, text="Password", font=('Arial Black', 13), fg="Sienna", bg='white')
        password_label.place(x=150, y=300)
        password = tk.StringVar()
        passwordEntry = tk.Entry(self.root, textvariable=password, font=('Arial Black', 13), fg="Sienna",
                                 show='*')
        passwordEntry.place(x=300, y=300)
        self.list_w.append(password_label)
        self.list_w.append(passwordEntry)

        email_label = tk.Label(self.root, text="Email", font=('Arial Black', 13), fg="Sienna", bg='white')
        email_label.place(x=150, y=400)
        email = tk.StringVar()
        emailEntry = tk.Entry(self.root, textvariable=email, font=('Arial Black', 13), fg="Sienna")
        emailEntry.place(x=300, y=400)
        self.list_w.append(email_label)
        self.list_w.append(emailEntry)

        login = tk.Button(self.root, text='Login',
                          command=lambda: self.validatelogin(usernameEntry, passwordEntry, emailEntry),
                          font=('Arial Black', 13), fg='Sienna', bg='white')
        login.place(x=650, y=300)
        self.list_w.append(login)

    def about_us(self):
        """
        This function shows the information about the game TRIVI
        """
        print("in about us")
        if not self.is_empty():
            self.removing_widget()
        self.root.title("TRIVI Game - About Us - Player")
        home_button = tk.Button(self.root, text="Home", command=self.welcome_screen, font=('Arial Black', 13),
                                fg="Sienna", bg='white')
        home_button.place(x=50, y=20)
        self.list_w.append(home_button)
        label_text = """\n TRIVI is an interactive multiplayer trivia game.\n
            Each question has a time limit, the faster you answer the higher yor score will be.\n
        At the end of the game, the player with the highest number of points wins.        
        """
        about_label = tk.Label(self.root, text=label_text, font=('Arial Black', 11), fg="Sienna", bg='white')
        about_label.place(x=65, y=200)
        self.list_w.append(about_label)

    def on_quit(self):
        """
        This function closes the app
        """
        self.serversocket.send(str.encode('log out'))
        if self.serversocket.recv(1024).decode() == 'send':
            self.serversocket.send(str.encode(self.username))
            reply = self.serversocket.recv(1024).decode()
            print('reply on_quit:    ', reply)
            if reply == 'operation done successfully':
                self.root.destroy()


    def welcome_screen(self):
        """
        This function shows the main screen of the game for the player
        """
        self.root.protocol("WM_DELETE_WINDOW",self.on_quit)

        if not self.is_empty():
            self.removing_widget()

        self.root.title("TRIVI Game - Main Window - Player")
        self.root.geometry("1000x700")
        bg = tk.PhotoImage(file="bg_pic_new.png")
        label_bg = tk.Label(self.root, image=bg)
        label_bg.place(x=0, y=0)

        # sign in button
        signin_label = tk.Label(self.root, text="Log Into Existing Account", font=('Arial Black', 13), fg="Sienna",
                                bg='white')
        signin_label.place(x=150, y=200)
        signin_button = tk.Button(self.root, text="Sign in", command=self.sign_in, font=('Arial Black', 13), fg="Sienna",
                       bg='white')
        signin_button.place(x=230, y=250)
        self.list_w.append(signin_button)
        self.list_w.append(signin_label)

        # sign up button
        signup_label = tk.Label(self.root, text="Create a New Account", font=('Arial Black', 13), fg="Sienna",
                                bg='white')
        signup_label.place(x=600, y=200)
        signup_button = tk.Button(self.root, text="Sign up", command=self.sign_up, font=('Arial Black', 13), fg="Sienna",
                       bg='white')
        signup_button.place(x=650, y=250)
        self.list_w.append(signup_button)
        self.list_w.append(signup_label)

        # about us button
        about_button = tk.Button(self.root, text="About us", command=self.about_us, font=('Arial Black', 13), fg="Sienna",
                       bg='white')
        about_button.place(x=440, y=400)
        self.list_w.append(about_button)

        tk.mainloop()
        print("finish here")
        os._exit(0)
        #exit()