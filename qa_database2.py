import sqlite3


class Questions_and_Answers:

    def __init__(self, tablename="questions_answers2", question="question", correct_answer="correct_answer", wrong_answer1="wrong_answer1", wrong_answer2="wrong_answer2", wrong_answer3 = "wrong_answer3"):
        self.__tablename = tablename #the table name
        self.__question = question #the question
        self.__correct_answer = correct_answer #the correct answer
        self.__wrong_answer1 = wrong_answer1 #the first wrong answer
        self.__wrong_answer2 = wrong_answer2 #the second wrong answer
        self.__wrong_answer3 = wrong_answer3 #the third wrong answer
        conn = sqlite3.connect('database_qa.db')
        print("Opened database successfully")
        query_str = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + self.__question + " " + \
                    " TEXT PRIMARY KEY NOT NULL  ,"
        query_str += " " + self.__correct_answer + " TEXT    NOT NULL  ,"
        query_str += " " + self.__wrong_answer1 + " TEXT    NOT NULL  ,"
        query_str += " " + self.__wrong_answer2 + " TEXT    NOT NULL  ,"
        query_str += " " + self.__wrong_answer3 + " TEXT    NOT NULL  );"

        conn.execute(query_str)
        print("Table created successfully")
        conn.commit()
        conn.close()


    def get_questions_and_answers(self):
        """
        This function returns all of the questions and answers in the table
        :return: A string of all of the questions and answers in the table
        """
        conn = sqlite3.connect('database_qa2.db')
        str1 = "select * from questions_answers2;"
        print(str1)
        cursor = conn.execute(str1)
        q_a = []
        for row in cursor:
            question = row[0]
            correct_answer = row[1]
            wrong_answer1 = row[2]
            wrong_answer2 = row[3]
            wrong_answer3 = row[4]
            st =  question + "#" + correct_answer + "#" + wrong_answer1 + "#" + wrong_answer2 + "#" + wrong_answer3
            q_a.append(st)

        conn.close()
        return q_a
