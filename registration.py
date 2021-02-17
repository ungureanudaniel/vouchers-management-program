from tkinter import *
from tkinter import messagebox
import bcrypt
import sqlite3
import os

#-------------------NOT WORKING YET!!!------------------------------------------------------------
#---------------------------------------login existing user class-------------------------------

class Login:
    def __init__(self):
        self.login_window = Tk()
        self.login_window.geometry('530x250')
        self.login_window.configure(background='grey23')

        #------------person first name-----------------------------
        self.user_label = Label(self.login_window, text="Enter user name", bg='grey23', fg='white')
        self.user_label.place(x=10, y=60, height=30, width=140)
        self.user_label.config(font=("Courier", 11))
        self.user = Entry(self.login_window)
        self.user.place(x=200, y=60, height=30, width=320)


        # -----------voucher value-----------------------------
        self.pass_label = Label(self.login_window, text="Add voucher value", bg='grey23', fg='white')
        self.pass_label.place(x=10, y=100, height=30, width=160)
        self.pass_label.config(font=("Courier", 11))
        self.password = Entry(self.login_window)
        self.password.place(x=200, y=100, height=30, width=320)


        self.submit_login_btn = Button(self.login_window, text="Login", bg='seagreen1', command=self.validate_login()).place(x=10, y=180, height=50, width=510)
    def validate_login(self):
        # --------------------create mysql database---------------------------------------
        conn = sqlite3.connect('voucher_list.db')
        # ---------------------cursor designation------------------------------------
        cursor1 = conn.cursor()
        user = self.user.get()
        password = self.password.get()
        # ---------------------create database table----------------------------------
        user_check = cursor1.execute("SELECT * FROM users WHERE username=:user AND password=:pass", {"user": user, "pass": password})
        try:
            if user_check:
                authenticated = True
                messagebox.showinfo("Success", "Welcome" + user + "!", parent=self.login_window)
            else:
                messagebox.showerror("Error", "User doesn't exist!", parent=self.login_window)
        except IndexError:
            messagebox.showerror("Error", "Wrong Credentials", parent=self.login_window)
        # ----------------------commit changes---------------------------------------
        conn.commit()
        # ----------------------close database connection (not100% necessary)--------
        conn.close()





    def run(self):
     self.login_window.mainloop()

#---------------------------------------register user class---------------------------------------------------
class Register:
    def __init__(self):
        self.reg_window = Tk()
        self.reg_window.geometry('530x250')
        self.reg_window.configure(background='grey23')
        #------------person first name-----------------------------
        self.user_label = Label(self.reg_window, text="Enter user name", bg='grey23', fg='white')
        self.user_label.place(x=10, y=60, height=30, width=140)
        self.user_label.config(font=("Courier", 11))
        self.user = Entry(self.reg_window)
        self.user.place(x=200, y=60, height=30, width=320)


        # -----------voucher value-----------------------------
        self.pass_label = Label(self.reg_window, text="Add voucher value", bg='grey23', fg='white')
        self.pass_label.place(x=10, y=100, height=30, width=160)
        self.pass_label.config(font=("Courier", 11))
        self.password = Entry(self.reg_window)
        self.password.place(x=200, y=100, height=30, width=320)


        self.submit_login_btn = Button(self.reg_window, text="Login", bg='seagreen1', command=self.validate_new_user).place(x=10, y=180, height=50, width=510)
        def validate_new_user(self):
            user = self.user.get()
            passw = self.password.get()

            # --------------------create mysql database---------------------------------------
            conn = sqlite3.connect('voucher_list.db')
            # ---------------------cursor designation------------------------------------
            cursor1 = conn.cursor()
            # ---------------------create database table----------------------------------

            cursor1.execute("""CREATE TABLE IF NOT EXISTS users(
                username TEXT,
                password TEXT
            )""")
            cursor1.execute("SELECT username FROM users WHERE username=:username",{"username": user.get()})
            find_user = cursor1.fetchone()

            try:
                if user == "":
                    messagebox.showwarning("Attention!", "Username cannot be empty!!", parent=self.reg_window)
                elif len(str(user)) <= 2:
                    messagebox.showwarning("Attention!", "Username cannot be shorter than 3 characters!!", parent=self.reg_window)
                elif len(str(passw)) < 6:
                    messagebox.showwarning("Attention!", "Password must contain min 6 characters!!", parent=self.reg_window)
                elif not any(i.isdigit() for i in (passw)):
                    messagebox.showwarning("Attention!", "Password must contain at least one digit!!", parent=self.reg_window)
                elif find_user == user.get():
                    messagebox.showwarning("Attention!", "Username already taken!!", parent=self.reg_window)
                else:
                    cursor1.execute("INSERT INTO users (username, password) VALUES (:username, :password)", (user, passw))
            except IndexError:
                messagebox.showerror("Error", "Wrong Credentials", parent=self.reg_window)
            # ----------------------commit changes---------------------------------------
            conn.commit()
            # ----------------------close database connection (not100% necessary)--------
            conn.close()





    def run(self):
        self.reg_window.mainloop()
