
import threading
from functools import partial
import random
import clock_try
from tkinter import font
import sys
import os

class screen_server:
    def __init__(self, u, s, list_w, all_questiones1, names_of_users, all_questiones2):
        self.index = 0 #Current question number
        self.list_of_widgets = [] #list of widgets on the screen
        self.users = u #users database
        self.correctnum = 0 #correct answer number
        self.all_questions_number = 0 #number of all of the questions
        self.list_all_names = [] #List of the players names


        #for main screen
        self.s = s #The server
        self.list_w = list_w #List of users usernames labels
        self.all_questions1 = all_questiones1 #All of the questions ans answers from the first database
        self.all_questions2 = all_questiones2 #All of the questions ans answers from the second database
        self.names_of_users = names_of_users #Names of users

        self.game_num = 0 #How many games did the server host





    def removing_widget(self):
        """
        This function removes all of the widgets in the list from the screen
        """
        for i in range(len(self.list_of_widgets)):
            self.list_of_widgets[i].destroy()
        del self.list_of_widgets[:]

    def is_empty(self):
        """
        This function check if the widgets list is empty
        :return: If the list is empty it returns True else it returns False
        """
        if len(self.list_of_widgets) == 0:
            return True
        return False


    def get_correct_answer_num(self):
        """
        This function returns the current answer number
        :return: Current answer number
        """
        return self.correctnum

    def points_of_players(self, root, tk, list_all_names, allclients, all_questions):
        """
        This function shows after each question the cueernt score of the players
        :param root: The screen
        :param tk: The module tkinter
        :param list_all_names: The usernames list
        :param allclients: The list of all the clients
        :param all_questions: All of the questions ans answers from the chosen database
        :return:
        """
        if not self.is_empty():
            self.removing_widget()
        scores = self.users.sort_score()
        x_index = 200
        y_index = 190
        for score in scores:
            player = tk.StringVar()
            st = score[0]+"   "+str(score[1])
            player.set(st)
            label = tk.Label(root, textvariable=player, bg = 'white', fg = 'Sienna', font=('Arial Black', 12))
            self.list_of_widgets.append(label)
            label.place(x=x_index, y=y_index)
            y_index += 50

        start_game_ = partial(self.start_game, list_all_names,self.s.getallclients(), root, all_questions, tk)
        start = tk.Button(root, text="NEXT", font=('Arial Black', 16),
                          fg="Sienna", command=start_game_, bg = 'white')
        start.place(x=670, y=10)
        self.list_of_widgets.append(start)


    def start_game(self,list_all_names, allclients, root, all_questions, tk):
        """
        This function shows the game screen after the server starts the game
        :param list_all_names: The usernames list
        :param allclients: The list of all the clients
        :param root: The screen
        :param all_questions: All of the questions ans answers from the chosen database
        :param tk: The module tkinter
        :return:
        """
        root.title("TRIVI Game - Main Window - Server")
        self.all_questions_number = len(all_questions)
        if self.index == 0:
            print(list_all_names)
            if len(list_all_names) != 0:
                for i in range(len(list_all_names)):
                    list_all_names[i].destroy()
        if not self.is_empty():
            self.removing_widget()

        if self.index == self.all_questions_number:
            position_label = tk.Label(root, text="GAME OVER", font=('Arial Black', 30), fg="Sienna", bg = 'white')
            position_label.place(x=250, y=200)
            self.list_of_widgets.append(position_label)
            print(self.list_all_names)
            for name in self.list_all_names:
                self.users.cahnge_user_position(name)

            start = tk.Button(root, text="NEXT", font=('Arial Black', 16),
                              fg="Sienna", command=lambda:self.start(root, self.s, tk, self.list_w,
                                                                     list_all_names, self.all_questions1, self.names_of_users, self.all_questions2), bg='white')
            start.place(x=670, y=10)
            self.list_of_widgets.append(start)

            quit = tk.Button(root, text = 'quit', font = ('Arial Black', 12), fg = 'Sienna', command = lambda:self.log_out(root), bg = 'white')
            quit.place(x = 670, y = 100)
            self.list_of_widgets.append(quit)






        else:
            for i in range(len(self.s.getallclients())):
                self.s.getallclients()[i].sendall(str.encode('game starts'))

            self.correctnum = self.index
            question = all_questions[self.index]
            print(question)
            arr = question.split('#')
            queshtion_ = tk.StringVar()
            queshtion_.set(arr[0])
            label = tk.Label(root, textvariable=queshtion_, bg = "white", font=('Arial Black', 16),
                        fg="Sienna")
            label.place(x = 200, y = 210)
            self.list_of_widgets.append(label)

            x = random.randint(1,4)
            numbers = [1,2,3,4]
            wrong_numbers = []
            correct_answer_number = x
            self.correctnum = x
            first_wrong_num = 0
            second_wrong_num = 0
            third_wrong_num = 0

            for number in numbers:
                if number != correct_answer_number:
                    wrong_numbers.append(number)
            first_wrong_num += wrong_numbers[0]
            second_wrong_num += wrong_numbers[1]
            third_wrong_num += wrong_numbers[2]

            answer_correct = [correct_answer_number ,arr[1]]
            answer_wrong1 = [first_wrong_num, arr[2]]
            answer_wrong2 = [second_wrong_num, arr[3]]
            answer_wrong3 = [third_wrong_num, arr[4]]


            nums_in_order = []
            nums_in_order.append(answer_correct)
            nums_in_order.append(answer_wrong1)
            nums_in_order.append(answer_wrong2)
            nums_in_order.append(answer_wrong3)

            #sorting all of the ansers
            for i in range(len(nums_in_order)-1):
                for j in range(len(nums_in_order)-1):
                    if nums_in_order[j][0] > nums_in_order[j+1][0]:
                        x = nums_in_order[j]
                        nums_in_order[j] = nums_in_order[j+1]
                        nums_in_order[j+1] = x

            #placing the options
            first_answer = tk.StringVar()
            first_answer.set(str(nums_in_order[0][0]) + "  " + nums_in_order[0][1])
            label_for_first = tk.Label(root, textvariable=first_answer, bg = 'white', font=('Arial Black', 16), fg = 'sienna')
            label_for_first.place(x=85, y=400)
            self.list_of_widgets.append(label_for_first)

            second_answer = tk.StringVar()
            second_answer.set(str(nums_in_order[1][0]) + "  " + nums_in_order[1][1])
            label_for_second = tk.Label(root, textvariable=second_answer, bg = 'white', font = ('Arial Black', 16), fg = 'sienna')
            label_for_second.place(x=85, y=560)
            self.list_of_widgets.append(label_for_second)

            third_answer = tk.StringVar()
            third_answer.set(str(nums_in_order[2][0]) + "  " + nums_in_order[2][1])
            label_for_third = tk.Label(root, textvariable=third_answer, bg = 'white', font = ('Arial Black', 16), fg = 'sienna')
            label_for_third.place(x=550, y=400)
            self.list_of_widgets.append(label_for_third)

            fourth_answer = tk.StringVar()
            fourth_answer.set(str(nums_in_order[3][0]) + "  " + nums_in_order[3][1])
            label_for_fourth = tk.Label(root, textvariable=fourth_answer,  bg = 'white', font = ('Arial Black', 16), fg = 'sienna')
            label_for_fourth.place(x=550, y=560)
            self.list_of_widgets.append(label_for_fourth)
            # creating the clock
            clock = clock_try.clock_try(root)
            clock.start_clock()

            self.index += 1

            points = partial(self.points_of_players, root, tk, list_all_names, self.s.getallclients(), all_questions)
            point = tk.Button(root, text = "POINTS CHART", font = ('Arial Black', 12), fg = 'Sienna', command = points, bg = 'white')
            point.place(x = 600, y = 100)
            self.list_of_widgets.append(point)



            #return


    def first_screen(self, root, s, tk, list_w, list_all_names, all_questions, names_of_usres):
        """
        This function shows the screen where the server can open and start the game
        :param root: The screen
        :param s: The server
        :param tk: The module tkinter
        :param list_w: The list of usernames labels on the screen
        :param list_all_names: The usernames list
        :param all_questions: All of the questions ans answers from the chosen database
        :param names_of_usres: The usernames list
        :return:
        """
        if not self.is_empty():
            self.removing_widget()
        if self.game_num == 1:
            server_thread = threading.Thread(target=s.start)
            server_thread.demon = True
            login = tk.Button(root, text="OPEN THE GAME", command = server_thread.start, font=('Arial Black', 16),
                            fg="Sienna", bg = 'white')
            login.place(x = 200, y = 300)
            list_w.append(login)
        start_game_ = partial(self.start_game, list_all_names,  s.getallclients(), root, all_questions, tk)
        start = tk.Button(root, text="START THE GAME", font=('Arial Black', 16),
                        fg="Sienna", command = start_game_, bg = 'white')
        self.list_all_names = names_of_usres
        start.place(x = 560, y = 300)
        self.list_of_widgets.append(start)



    def ok(self,variable, root, s, tk, list_w, list_all_names, all_questions1, names_of_usres, all_questions2):

        print("value is:" + variable.get())
        set = variable.get()
        if set == 'Capitals':
            self.first_screen(root, s, tk, list_w, list_all_names, all_questions1, names_of_usres)
        else:
            self.first_screen(root, s, tk, list_w, list_all_names, all_questions2, names_of_usres)


    def log_out(self, root):
        for i in range(len(self.s.getallclients())):
            self.s.getallclients()[i].sendall(str.encode('server closed the game'))
        print("quit program 0")
        self.s.get_flag()
        root.destroy()
        print("quit program 1")
        #self.s.get_server_socket().close()
        print('quit program 2')







    def start(self, root, s, tk, list_w, list_all_names, all_questions1, names_of_usres, all_questions2):
        """
        This function shows the main screen of the game for the server
        :param root:The screen
        :param s: The server
        :param tk: The module tkinter
        :param list_w: The list of usernames labels on the screen
        :param list_all_names: The usernames list
        :param all_questions1: All of the questions ans answers from the first database
        :param names_of_usres: The usernames list
        :param all_questions2: All of the questions ans answers from the second database
        """
        self.game_num += 1

        if self.game_num > 1:
            for i in range(len(self.s.getallclients())):
                self.s.getallclients()[i].sendall(str.encode('server decided to continue the game'))
            self.s.update_start()


        self.index = 0
        if not self.is_empty():
            self.removing_widget()

        root.title("TRIVI Game - Main Window - Server")
        root.geometry("1000x700")
        bg = tk.PhotoImage(file="bg_pic.png")
        label_bg = tk.Label(root, image=bg)
        label_bg.place(x=0, y=0)





        OPTIONS = ["choose a set", "Capitals", "Python"]  # etc


        variable = tk.StringVar(root)
        variable.set(OPTIONS[0])  # default value

        w = tk.OptionMenu(root, variable, *OPTIONS[1:])
        f = font.Font(family = 'Arial Black', size = 13)
        w.config(font = f)
        w.pack(pady = 200, padx = 100)
        button = tk.Button(root, text="OK", bg = 'white', fg = 'Sienna', font=('Arial Black', 13), command=lambda: self.ok(variable, root, s, tk,
                                                                    list_w, list_all_names, all_questions1, names_of_usres, all_questions2))
        button.place(x = 475, y = 300)


        self.list_of_widgets.append(w)
        self.list_of_widgets.append(button)

        tk.mainloop()
        print('finish here')
        os._exit(0)
        #raise SystemExit
        #sys.exit()

        #exit()