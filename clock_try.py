from tkinter import *
import time
import threading

class clock_try:
    def __init__(self, root):
        self.root = root #the screen
        self.clock_label =Label(self.root, fg='midnight blue', font=('Eras Bold ITC', 38), bg = 'white') #the label for the timer
        self.sec = 31 #the timer's time


    def tick(self):
        """
        This function presents the timer
        """
        self.sec -= 1
        if self.sec >= 0:
            self.clock_label['text'] = self.sec
            self.clock_label.after(1000, self.tick)
        else:
            pass


    def start_clock(self):
        """
        This function starts the timer on the screen
        """
        self.clock_label.pack(anchor=NW)
        self.tick()
        Thread1 = threading.Thread(target=self.counting_and_removing)
        Thread1.daemon = True
        Thread1.start()

    def get_label_clock(self):
        """
        This function returns the clock's label
        :return: The clock's label
        """
        return self.clock_label


    def counting_and_removing(self):
        """
        This function removes the timer when the time is up
        """
        time.sleep(31)
        self.get_label_clock().pack_forget()