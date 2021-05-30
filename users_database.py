import sqlite3


class Users:

    def __init__(self, tablename="users", username="username", password="password", email="email", score = "score", in_the_game = "in_the_game"):
        self.__tablename = tablename #the table's name
        self.__username = username #the user's username
        self.__password = password #the user's password
        self.__email = email #the user's email
        self.__score = score #the user's current score
        self.__in_the_game = in_the_game #is the user playing right now
        conn = sqlite3.connect('database_users.db')
        print("Opened database successfully")
        query_str = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + self.__username + " " + \
                    " TEXT PRIMARY KEY NOT NULL UNIQUE ,"
        query_str += " " + self.__password + " TEXT    NOT NULL ,"
        query_str += " " + self.__email + " TEXT    NOT NULL    UNIQUE  ,"
        query_str += " " + self.__score + " INTEGER     NOT NULL    DEFAULT 0  ,"
        query_str += " " + self.__in_the_game + " INTEGER     NOT NULL    DEFAULT 0);"

        conn.execute(query_str)
        print("Table created successfully")
        conn.commit()
        conn.close()


    def check_username(self, name):
        """
        The function checks if the username exists
        :param name: User's username
        :return: False if the username exists otherways True
        """
        conn = sqlite3.connect('database_users.db')
        str1 = "select * from users;"
        cursor = conn.execute(str1)
        for row in cursor:
            if row[0] == name:
                return False
        return True

    def check_email(self, email):
        """
        The function checks if the user's email exists
        :param email: User's email
        :return: False if the email exists otherways True
        """
        conn = sqlite3.connect('database_users.db')
        str1 = "select * from users;"
        cursor = conn.execute(str1)
        for row in cursor:
            if row[2] == email:
                return False
        return True

    def get_email_of_user(self, username):
        """
        The function returns the user's email
        :param username: User's username
        :return: The user's email
        """
        conn = sqlite3.connect('database_users.db')
        str1 = "select * from users;"
        cursor = conn.execute(str1)
        for row in cursor:
            if row[0] == username:
                return row[2]
        return ""

    def get_user_password(self, username):
        """
        The function returns the user's password
        :param username: User's username
        :return: The user's password
        """
        conn = sqlite3.connect('database_users.db')
        str1 = "select * from users;"
        cursor = conn.execute(str1)
        for row in cursor:
            if row[0] == username:
                return row[1]
        return ""


    def insert_user(self, username, password, email, score, in_the_game):
        """
        This function inserts a new user into the table
        :param username: User's username
        :param password: User's passowrd
        :param email: User's email
        :param score: User's current score
        :param in_the_game: Is the user in the game right now
        """
        conn = sqlite3.connect('database_users.db')
        insert_query = "INSERT INTO " + self.__tablename + " (" + self.__username + "," + self.__password +"," + self.__email +"," +self.__score +","+self.__in_the_game +") VALUES " \
                                                                                                            "(" + "'" + username + "'" + "," + "'" + password + "'" +  "," + "'" + email + "'" +  "," + "'" + str(score) +"'" +  "," + "'" +str(in_the_game) + "'" +");"
        print(insert_query)
        conn.execute(insert_query)
        conn.commit()
        conn.close()
        print("Record created successfully")

    def print_table(self):
        """
        This function prints all of the records in the table
        """
        conn = sqlite3.connect('database_users.db')
        print("Opened database successfully")
        str1 = "select * from users;"

        """strsql = "SELECT username, password, email  from " +  self.__tablename + " where " + self.__username + "=" \
            + str(username)
        """
        print(str1)
        cursor = conn.execute(str1)
        for row in cursor:
            print("username = ", row[0])
            print("password = ", row[1])
            print("email = ", row[2])
            print("score = ", row[3])
            print("in_the_game = ", row[4])

        print("Operation done successfully")
        conn.close()



    def update(self, username_, score_to_add):
        """
        This function updates the player's score
        :param username_: User's username
        :param score_to_add: User's score to add
        :return:
        """
        conn = sqlite3.connect('database_users.db')
        current_score = 0
        cursor = conn.execute("select * from users;")
        for row in cursor:
            if row[0] == username_:
                current_score+=row[3]
        final_score = score_to_add + current_score
        conn.execute('update users set score = ? where username = ?', (final_score, username_))
        conn.commit()
        print('updated')


    def update_password(self, username, new_password):
        """
        This function updates the user's password with new one
        :param username: User's username
        :param new_password: User's new password
        """
        conn = sqlite3.connect('database_users.db')
        conn.execute('update users set password = ? where username = ?', (new_password, username))
        conn.commit()
        print('updated password')


    def sort_with(self, name_and_score):
        """
        This function returns the score of the player in the list
        :param name_and_score: List of usernames and their scores
        :return: Score of the player in the list
        """
        return name_and_score[1]

    def cahnge_user_position(self, username):
        """
        This function changes the user's position at the end of the game from 1 to 0
        :param username: User's username
        """
        conn = sqlite3.connect('database_users.db')
        conn.execute('update users set in_the_game = ? where username = ?', (0, username))
        conn.commit()
        print('updated')

    def change_user_position_start(self, username):
        """
        This function changes the user's position at the beginning of the game from 0 to 1
        :param username: User's username
        """
        conn = sqlite3.connect('database_users.db')
        conn.execute('update users set in_the_game = ? where username = ?', (1, username))
        conn.commit()
        print('updated')


    def sort_score(self):
        """
        This function stores the players scores after everu question
        :return: Sorted List of players and their scores
        """
        conn = sqlite3.connect('database_users.db')
        print("Opened database successfully")
        str1 = "select * from users;"

        print(str1)
        cursor = conn.execute(str1)
        scores = []
        for row in cursor:
            if row[4] == 1:
                name_and_score = []
                name_and_score.append(row[0])
                name_and_score.append(row[3])
                scores.append(name_and_score)
            else:
                pass
        scores.sort(key = self.sort_with)
        scores.reverse()
        conn.close()
        return scores

    def reset_score(self, username):
        """
        This function resets the user's score at the beginning of the game
        :param username: User's username
        """
        conn = sqlite3.connect('database_users.db')
        conn.execute('update users set score = ? where username = ?', (0, username))
        conn.commit()
        print('score was reset')

    def is_user_in_the_game(self, username):
        """
        This function returns True if the user is the game right now and False otherways
        :param username: User's username
        :return: True if the user is the game right now and False otherways
        """
        conn = sqlite3.connect('database_users.db')
        str1 = "select * from users;"
        cursor = conn.execute(str1)
        for row in cursor:
            if row[0] == username:
                if row[4] == 1:
                    return True
        return False

    def get_users_position(self, username):
        conn = sqlite3.connect('database_users.db')
        str1 = "select * from users;"
        cursor = conn.execute(str1)
        for row in cursor:
            if row[0] == username:
                #print("the users position is:   ",row[4])
                return row[4]
        return None
        conn.close()




# u = Users()
# u.print_table()
# u.get_users_position('eden')
# print('------------------------------------------------')
# u.print_table()