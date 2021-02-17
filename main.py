from sqlite3.dbapi2 import Connection
from PIL import ImageTk,Image
from tkinter import *
from tkinter import messagebox
# import mysql.connector as mysql
from tkinter import ttk
import subprocess
import datetime
# import tksheet
import sqlite3
import re
import sys
import requests
import json
import os
import random
from registration import Login, Register


os.system("clear")

root = Tk()
def style1():
    combostyle = ttk.Style()
    combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'black',
                                       'fieldbackground': 'white',
                                       'background': 'grey'
                                       }}}
                         )
    style1=combostyle.theme_use('combostyle')
style1()

#-----------------------------main window function called home-------------------------
def home():
    root.title("Artisan Bakery's Vouchers")
    root.geometry('530x600')
    root.configure(background='grey23')
    #-------------------------create global variables---------------------------------
    global id
    global series
    global name
    global value
    global valid_id
    global x
    global authenticated
    global current_oid
    max_pk = ""
    go_print = False
    max_pk = "ATZ0"

    #
    # def login_menu():
    #     login = Login()
    #     login.run()
    #
    # def register():
    #  register = Register()
    #  register.run()
    #
    # def logout_menu():
    #     pass

    #--------------------------create input table---------------------------------
    def ledger():
        try:
            # --------------------create mysql database---------------------------------------
            conn = sqlite3.connect('voucher_list.db')
            # ---------------------cursor designation------------------------------------
            cursor1 = conn.cursor()
            # ---------------------create database table----------------------------------
            cursor1.execute("""CREATE TABLE IF NOT EXISTS ledger (
                voucher_id text,
                name text,
                value integer,
                action text,
                date text)""")
            # ----------------------commit changes---------------------------------------
            conn.commit()
            # ----------------------close database connection (not100% necessary)--------
            conn.close()
        except sqlite3.Error as error:
            messagebox.showwarning("Error!", "Failed to create voucher list sql table!", parent=root)
    ledger()
    #--------------------------create remaining amounts table---------------------------------
    def balance_table():
        try:
            # -----------------------------connect to database-----------------------------
            conn = sqlite3.connect('voucher_list.db')
            # ---------------------cursor designation---------------------------------------
            cursor1 = conn.cursor()
            #---------------------create database table----------------------------------
            cursor1.execute("""CREATE TABLE IF NOT EXISTS remaining (
                id text,
                amount_left integer
            )""")
            # ----------------------commit changes---------------------------------------
            conn.commit()
            # ----------------------close database connection (not100% necessary)--------
            conn.close()
        except sqlite3.Error as error:
            messagebox.showwarning("Error!", "Failed to create balance sql table!", parent=root)
    balance_table()
    #------------------------another separate table where you find the modifications done on voucher data if needed, including deletion--------
    def modifications_table():
        try:
            # -----------------------------connect to database-----------------------------
            conn = sqlite3.connect('voucher_list.db')
            # ---------------------cursor designation---------------------------------------
            cursor1 = conn.cursor()
            #---------------------create database table----------------------------------
            cursor1.execute("""CREATE TABLE IF NOT EXISTS modifications (
                voucher_id text,
                old_name text,
                new_name text,
                old_value text,
                new_value text,
                action text,
                date text
            )""")
            # ----------------------commit changes---------------------------------------
            conn.commit()
            # ----------------------close database connection (not100% necessary)--------
            conn.close()
        except sqlite3.Error as error:
            messagebox.showwarning("Error!", "Failed to create modifications sql table / {}!".format(error), parent=root)
    modifications_table()


    #--------------------------------logic to get the current PK in the entry box--------
    conn = sqlite3.connect('voucher_list.db')
    # ---------------------cursor designation------------------------------------
    cursor1 = conn.cursor()
    # ---------------------fetch last primary key----------------------------------
    try:
        date_selection = cursor1.execute("SELECT MAX(oid) FROM ledger WHERE action =:action", {'action': "Credit"})
        max_oid = date_selection.fetchone()[0]
        c_selection = cursor1.execute("SELECT * FROM ledger WHERE oid=:max_oid", {'max_oid': max_oid})
        row = c_selection.fetchone()
        if row:
            if len(row) > 0:
                max_pk = row[0]


    except sqlite3.Error as error:
        messagebox.showwarning("Error!", error, parent=root)
    # ----------------------commit changes---------------------------------------------
    conn.commit()

    #--------------------------------save entry box data into database -----------------

    def save():

        valid_id = True
        new_id = id.get()
        new_series = str(series.get()) + str(id.get())
        new_name = name.get()
        new_value = value.get()
        new_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        action = 'Credit'




        #--------------------------functions that validate entries-------------------------
        def validate_value():
            if new_value.isdigit():
                return True
            else:
                messagebox.showwarning("Attention!", "Only digits in value!", parent=root)
                return False
        A = validate_value()
        def validate_name():
            if new_name == "":
                messagebox.showwarning("Attention!", "Name cannot be empty!", parent=root)
                return False
            else:
                return True
        B = validate_name()
        def validate_id():
            if new_id.isdigit():
                return True
            elif not new_id.isdigit():
                messagebox.showwarning("Attention!", "Only digits in ID!", parent=root)
                return False
            elif new_id == "":
                messagebox.showwarning("Attention!", "ID cannot be empty!", parent=root)
                return False
        C = validate_id()
        if A == True and B == True and C == True:
            go_print = True

            #----------using register function to use the hand made validation function---------
            a = root.register(validate_name)
            name.configure(validate="key",validatecommand=(a,'%P'))

            try:
                #----------using register function to use the hand made validation function---------
                c = root.register(validate_value)
                value.configure(validate="key",validatecommand=(c,'%P'))

                # --------------------create mysql database---------------------------------------
                conn = sqlite3.connect('voucher_list.db')
                # ---------------------cursor designation------------------------------------
                cursor1 = conn.cursor()
                #-------------------------check if id exists already-----------------------------
                check = cursor1.execute("SELECT voucher_id FROM ledger WHERE voucher_id= :new_id", {'new_id': new_series})

                if check.fetchone():
                    #--------------------------cancel insert and show alert---------------------
                    valid_id = False
                    messagebox.showwarning("Attention!", "ID exists already!", parent=root)
                else:
                    #-----------------------insert data into db--------------------------------------
                    cursor1.execute("INSERT INTO ledger(voucher_id, name, value, action, date) VALUES (:voucher_id, :name, :value, :action, :date)", (new_series, new_name, new_value, action, new_time))
                    messagebox.showinfo("Info", "Voucher {} saved!".format(str(current_series[0]) + str(int(current_series[1]) + 1)), parent=root)
                #-----------------------------close connection----------------------------------
                conn.commit()

                conn.close()

            except sqlite3.Error as error:
                messagebox.showwarning("Error!", "Failed to save voucher!", parent=root)




    def print():
        #--------------------------------voucher design visualisation and print---------
        voucher_design = Toplevel(root)
        voucher_design.title("Voucher" + " " + "current ID")
        voucher_design.geometry('700x300')
        voucher_design.configure(background='grey23')
        menubar = Menu(voucher_design)
        file = Menu(menubar, tearoff=0)
        file.add_command(label="New")
        file.add_command(label="Open")
        file.add_command(label="Save")
        file.add_command(label="Save as...")
        file.add_command(label="Close")


        file.add_separator()

        file.add_command(label="Exit", command=voucher_design.quit)

        menubar.add_cascade(label="File", menu=file)

        help = Menu(menubar, tearoff=0)
        help.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help)

        voucher_design.config(menu=menubar)

        if go_print == False:
            voucher_design.withdraw()
    #---------------------if data validation passed then print!---------------------------
        elif go_print == True:
            pass


    #----------------automatic insert of current id in entry box--------------------------
    series = 'ATZ'

    id_label = Label(root, text="Voucher ID", bg='grey23', fg='white')
    id_label.place(x=10, y=20, height=30, width=100)
    id_label.config(font=("Courier", 11))

    series = Entry(root)
    series.insert(END, "ATZ")
    series.configure(state=DISABLED)
    series.place(x=200, y=20, height=30, width=70)
    series.config(font=("Courier", 11))


    id = Entry(root)
    temp = re.compile("([a-zA-Z]+)([0-9]+)")
    current_series = temp.match(str(max_pk)).groups()
    if max_pk == None:
        id.insert(1, 1)
    elif len(max_pk) > 0:
        id.insert(1, int(current_series[1])+1)

    id.configure(state=DISABLED)
    id.place(x=270, y=20, height=30, width=250)
    id.config(font=("Courier", 11))



    # -----------person first name-----------------------------
    name_label = Label(root, text="Add person name", bg='grey23', fg='white')
    name_label.place(x=10, y=60, height=30, width=140)
    name_label.config(font=("Courier", 11))
    name = Entry(root)
    name.place(x=200, y=60, height=30, width=320)
    placeholder = "Unknown"
    name.insert(0,placeholder)

    # -----------voucher value-----------------------------

    # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox

    value_label = Label(root, text="Choose voucher value", bg='grey23', fg='white')
    value_label.place(x=10, y=100, height=30, width=180)
    value_label.config(font=("Courier", 11))
    value = ttk.Combobox(root, values=(50, 100, 150, 200))
    value['state'] = 'readonly'
    value.place(x=200, y=100, height=30, width=320)

    # ----------------------close database connection (not100% necessary)----------------
    # conn.close()





    def spending_window():
        spend_window = Toplevel(root)
        spend_window.title("Voucher" + " " + "current ID")
        spend_window.geometry('600x200')
        spend_window.configure(background='grey23')

        def spend():
            funds = False
            action1 = 'Debit'
            action2 = 'Credit'
            spent_amount = -int(amount_to_spend.get())
            spend_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            try:
                #--------------------sqlite3 database ID query---------------------------------------
                conn = sqlite3.connect('voucher_list.db')
                # ---------------------cursor designation------------------------------------
                cursor1 = conn.cursor()
                # ---------------------select desired ID from database-------------------------------------
                name_check = cursor1.execute("SELECT name FROM ledger WHERE voucher_id= :withdraw_id", {'withdraw_id': str(voucher_ser.get()) + str(spend_voucher_id.get())})
                name = name_check.fetchone()[0]
                cs = cursor1.execute("SELECT voucher_id FROM ledger WHERE (voucher_id=:withdraw_id AND action=:action)", {'withdraw_id': str(series) + str(spend_voucher_id.get()), 'action': action2})
                selected_id = cs.fetchone()[0]
                if len(selected_id) > 0:
                    try:
                        # ---------------------group and sum ledger by id-------------------------------------
                        row = cursor1.execute("SELECT voucher_id, SUM(value) value_left FROM ledger WHERE voucher_id = :selected_id GROUP BY voucher_id", {'selected_id': selected_id}).fetchone()
                        #-------------------------logic to check if there are enough funds---------------
                        # for row in rows:
                        if row[1] + spent_amount >= 0:
                            funds = True
                            #-----------------------insert data into ledger db--------------------------------------
                            cursor1.execute("INSERT INTO ledger(voucher_id, name, value, action, date) VALUES (:voucher_id, :name, :value, :action, :date)", (str(voucher_ser.get()) + str(spend_voucher_id.get()), name, spent_amount, action1, spend_time))
                            spend_window.withdraw()
                        else:
                            messagebox.showwarning("Error!", "Not enough funds!", parent=spend_window)
                            spend_window.withdraw()
                            funds=False

                    except sqlite3.Error as error:
                        messagebox.showwarning("Error!", error, parent=spend_window)
                else:
                    messagebox.showwarning("Error!", "Voucher ID does not exist!", parent=spend_window)
                # ----------------------commit changes---------------------------------------
                conn.commit()
                # ----------------------close database connection (not100% necessary)--------
                conn.close()

            except sqlite3.Error as error:
                messagebox.showwarning("Error!", error, parent=spend_window)

        #----------------------------entry boxex in withdraw window----------------------
        series = 'ATZ'
        voucher_ser_label = Label(spend_window, text="Voucher ID", bg='grey23', fg='white')
        voucher_ser_label.grid(column=1, row=2)
        voucher_ser_label.config(font=("Courier", 11))

        voucher_ser = Entry(spend_window)
        voucher_ser.insert(END, "ATZ")
        voucher_ser.configure(state=DISABLED)
        voucher_ser.grid(column=2, row=2)
        voucher_ser.config(font=("Courier", 11))

        spend_voucher_id = Entry(spend_window)
        spend_voucher_id.grid(column=3, row=2)
        amount_to_spend = Label(spend_window, text="Value to spend", bg='grey23', fg='white')
        amount_to_spend.grid(column=1, row=3)
        amount_to_spend = Entry(spend_window, width=20)
        amount_to_spend.grid(column=2, row=3, columnspan=3)
        #----------------------------delete button---------------------------------------
        spend_btn = Button(spend_window, text="Spend", command=spend, bg='goldenrod2', relief=RAISED)
        spend_btn.grid(column=2, row=4, columnspan=2, pady=10)


    #---------------------------------Voucher remaining amount---------------------------------
    def get_balance():
        remaining_window = Toplevel(root)
        remaining_window.title("See remaining amounts")
        remaining_window.geometry('470x500')
        remaining_window.configure(background='grey23')
        #-----------------------Menu bar-----------------------------------------------------
        menubar = Menu(remaining_window,  bg='grey23', fg='white')
        file = Menu(menubar, tearoff=0, relief=FLAT,bd=0, bg='grey23', fg='white')
        file.add_command(label="New")
        file.add_command(label="Open")
        file.add_command(label="Save")
        file.add_command(label="Save as...")
        file.add_command(label="Close")

        file.add_separator()

        file.add_command(label="Exit", command=remaining_window.quit)

        menubar.add_cascade(label="File", menu=file)

        help = Menu(menubar, tearoff=0, relief=FLAT,bd=0, bg='grey23', fg='white')
        help.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help)

        remaining_window.config(menu=menubar)

        try:
            # -----------------------------connect to database-----------------------------
            conn = sqlite3.connect('voucher_list.db')
            # ---------------------cursor designation---------------------------------------
            cursor1 = conn.cursor()
            #-----------------------insert the amounts left into table----------------------
            sum = cursor1.execute("SELECT voucher_id, SUM(value) value_left FROM ledger GROUP BY voucher_id", {'credit': 'Credit', 'debit': 'Debit'})
            rows = sum.fetchall()

            # for row in rows:
                # id = row[0]
                # amount = row[1]
                # cursor1.execute("INSERT INTO remaining(id, amount_left) VALUES (:id, :amount)", (id, amount))

            # ----------------------commit changes---------------------------------------
            conn.commit()
            # ----------------------close database connection (not100% necessary)--------
            conn.close()
        except sqlite3.Error as error:
            messagebox.showwarning("Error!", "Failed calculating remaining amount!", parent=remaining_window)
        #----------------------------------table view--------------------------------------
        tree_cols3 = ("id", "amount")

        tree = ttk.Treeview(remaining_window, column=tree_cols3, show='headings')

        for i in range(len(tree_cols3)):
            tree.column('#' + str(i), anchor=CENTER, minwidth=100, stretch=0)
            tree.heading(i, text=tree_cols3[i])

        tree.place(x=10, y=120, width=450)

        for row in rows:
            tree.insert("", END, values=row, tags = ('oddrow',))
            tree.tag_configure('oddrow', background='orange')
            tree.tag_configure('evenrow', background='purple')



    #-------------------------------activity ledger----------------------------------------
    def ledger():
        ledger_window = Toplevel(root)
        ledger_window.title("Ledger")
        ledger_window.geometry('1070x500')
        ledger_window.configure(background='grey23')
        #-----------------------Menu bar-----------------------------------------------------
        menubar = Menu(ledger_window,  bg='grey23', fg='white')
        file = Menu(menubar, tearoff=0, relief=FLAT,bd=0, bg='grey23', fg='white')
        file.add_command(label="New")
        file.add_command(label="Open")
        file.add_command(label="Save")
        file.add_command(label="Save as...")
        file.add_command(label="Close")

        file.add_separator()

        file.add_command(label="Exit", command=ledger_window.quit)

        menubar.add_cascade(label="File", menu=file)

        help = Menu(menubar, tearoff=0, relief=FLAT,bd=0, bg='grey23', fg='white')
        help.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help)

        ledger_window.config(menu=menubar)

        #----------------------------------table view--------------------------------------
        tree_cols1 = ("voucher_id", "amount", 'action', "date", "oid")

        tree = ttk.Treeview(ledger_window, column=tree_cols1, show='headings')

        for i in range(len(tree_cols1)):
            tree.column('#' + str(i), anchor=W, minwidth=100, stretch=0)
            tree.heading(i, text=tree_cols1[i])

        tree.place(x=10, y=120, width=1050)

        try:
            #--------------------sqlite3 database---------------------------------------
            conn = sqlite3.connect('voucher_list.db')
            # ---------------------cursor designation------------------------------------
            cursor1 = conn.cursor()
            # ---------------------query the database-------------------------------------
            cursor1.execute("SELECT *, oid FROM ledger")

            rows = cursor1.fetchall()
            for row in rows:
                tree.insert("", END, values=row, tags = ('oddrow',))
                tree.tag_configure('oddrow', background='orange')
                tree.tag_configure('evenrow', background='purple')
            # ----------------------commit changes---------------------------------------
            conn.commit()
            # ----------------------close database connection (not100% necessary)--------
            conn.close()
        except sqlite3.Error as error:
            messagebox.showwarning("Error!", "Failed building ledger!", parent=ledger_window)

    #-------------------------------activity ledger----------------------------------------
    def modifications():
        mods_window = Toplevel(root)
        mods_window.title("Voucher Modifications")
        mods_window.geometry('1400x500')
        mods_window.configure(background='grey23')
        #-----------------------Menu bar-----------------------------------------------------
        menubar = Menu(mods_window,  bg='grey23', fg='white')
        file = Menu(menubar, tearoff=0, relief=FLAT,bd=0, bg='grey23', fg='white')
        file.add_command(label="New")
        file.add_command(label="Open")
        file.add_command(label="Save")
        file.add_command(label="Save as...")
        file.add_command(label="Close")

        file.add_separator()

        file.add_command(label="Exit", command=mods_window.quit)

        menubar.add_cascade(label="File", menu=file)


        help = Menu(menubar, tearoff=0, relief=FLAT,bd=0, bg='grey23', fg='white')
        help.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help)

        mods_window.config(menu=menubar)

        #----------------------------------table view--------------------------------------
        tree_cols4 = ("voucher_id", "old_name", "new_name", "old_value", "new_value", 'action', "date")

        tree = ttk.Treeview(mods_window, column=tree_cols4, show='headings')

        for i in range(len(tree_cols4)):
            tree.column('#' + str(i), anchor=W, minwidth=100, stretch=0)
            tree.heading(i, text=tree_cols4[i])

        tree.place(x=10, y=120, width=1380)

        try:
            #--------------------sqlite3 database---------------------------------------
            conn = sqlite3.connect('voucher_list.db')
            # ---------------------cursor designation------------------------------------
            cursor1 = conn.cursor()
            # ---------------------query the database-------------------------------------
            cursor1.execute("SELECT * FROM modifications")

            rows = cursor1.fetchall()
            for row in rows:
                tree.insert("", END, values=row, tags = ('oddrow',))
                tree.tag_configure('oddrow', background='orange')
                tree.tag_configure('evenrow', background='purple')
            # ----------------------commit changes---------------------------------------
            conn.commit()
            # ----------------------close database connection (not100% necessary)--------
            conn.close()
        except sqlite3.Error as error:
            messagebox.showwarning("Error!", "Failed building modifications table/ {}!".format(error), parent=mods_window)


    #--------------------------------------show/refresh voucher list-----------------
    def voucher_list():
        list_window = Toplevel(root)
        list_window.title("Voucher list")
        list_window.geometry('1000x500')
        list_window.configure(background='grey23')
        #------------Menu bar-----------------------------------------------------
        menubar = Menu(list_window,  bg='grey23', fg='white')
        file = Menu(menubar, tearoff=0, relief=FLAT,bd=0, bg='grey23', fg='white')
        file.add_command(label="New")
        file.add_command(label="Open")
        file.add_command(label="Save")
        file.add_command(label="Save as...")
        file.add_command(label="Close")

        file.add_separator()

        file.add_command(label="Exit", command=list_window.quit)

        menubar.add_cascade(label="File", menu=file)
        edit = Menu(menubar, tearoff=0,relief=FLAT,bd=0, bg='grey23', fg='white')
        edit.add_command(label="Undo")

        edit.add_separator()

        help = Menu(menubar, tearoff=0, relief=FLAT,bd=0, bg='grey23', fg='white')
        help.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help)

        list_window.config(menu=menubar)

        try:
            #--------------------sqlite3 database---------------------------------------
            conn = sqlite3.connect('voucher_list.db')
            # ---------------------cursor designation------------------------------------
            cursor1 = conn.cursor()
            # ---------------------query the database-------------------------------------
            join = cursor1.execute("SELECT * FROM ledger")

            # join = cursor1.execute("SELECT voucher_id, name, amount, amount_left, date FROM ledger INNER JOIN remaining ON ledger.voucher_id = remaining.voucher_id")

            rows = join.fetchall()
            # ----------------------commit changes---------------------------------------
            conn.commit()
            # ----------------------close database connection (not100% necessary)--------
            conn.close()
        except sqlite3.Error as error:
            messagebox.showwarning("Error!", "Failed fetching voucher list!", parent=list_window)
        #----------------------------------table view--------------------------------------
        tree_cols2 = ("voucher_id", "name", "value", "action", "date")

        tree = ttk.Treeview(list_window, column=tree_cols2, show='headings')

        for i in range(len(tree_cols2)):
            tree.column('#' + str(i), anchor=CENTER, minwidth=300, stretch=0)
            tree.heading(i, text=tree_cols2[i])

        for row in rows:
            tree.insert("", END, values=row, tags = ('oddrow',))
            tree.tag_configure('oddrow', background='orange')
            tree.tag_configure('evenrow', background='purple')
        tree.place(x=10, y=120, width=980)



        def select_record():
            id_update.delete(0,END)
        #-----------------------------------------voucher update/edit----------------------------
        def update_voucher():
            global id_series
            update_win = Toplevel(list_window)
            update_win.title("Update a voucher")
            update_win.geometry('600x300')
            update_win.configure(background='grey23')

            #-----------------------entry boxes for updates---------------------------------
            series = 'ATZ'
            id_label = Label(update_win, text="Voucher ID", bg='grey23', fg='white')
            id_label.place(x=10, y=20, height=30, width=180)
            id_label.config(font=("Courier", 11))

            series = Entry(update_win)
            series.insert(END, "ATZ")
            series.configure(state=DISABLED)
            series.place(x=200, y=20, height=30, width=70)
            series.config(font=("Courier", 11))

            id = Entry(update_win)
            id.insert(END, id_to_update.get())
            id.configure(state=DISABLED)
            id.place(x=270, y=20, height=30, width=250)


            # -----------person first name-----------------------------
            name_label = Label(update_win, text="Edit person name", bg='grey23', fg='white')
            name_label.place(x=10, y=60, height=30, width=180)
            name_label.config(font=("Courier", 11))
            nameE = Entry(update_win)
            nameE.place(x=200, y=60, height=30, width=320)


            # -----------voucher value-----------------------------
            style1
            value_label = Label(update_win, text="Edit voucher value", bg='grey23', fg='white')
            value_label.place(x=10, y=100, height=30, width=180)
            value_label.config(font=("Courier", 11))
            valueE = ttk.Combobox(update_win, values=(50, 100, 150, 200))
            valueE['state'] = 'readonly'

            valueE.place(x=200, y=100, height=30, width=320)



            def save_mods():
                new_name = nameE.get()
                new_value = valueE.get()

                new_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                action = 'Edit'
            #--------------------------functions that validate entries-------------------------
                def validate_value():
                    if new_value.isdigit():
                        return True
                    else:
                        messagebox.showwarning("Attention!", "Only digits in value!", parent=update_win)
                        return False
                A = validate_value()
                def validate_name():
                    if new_name == "":
                        messagebox.showwarning("Attention!", "Name cannot be empty!", parent=update_win)
                        return False
                    else:
                        return True
                B = validate_name()



                a = root.register(validate_name)
                name.configure(validate="key",validatecommand=(a,'%P'))

                c = root.register(validate_value)
                value.configure(validate="key",validatecommand=(c,'%P'))

                try:
                    #--------------------sqlite3 database---------------------------------------
                    conn = sqlite3.connect('voucher_list.db')
                    # ---------------------cursor designation------------------------------------
                    cursor1 = conn.cursor()
                    # ---------------------query the database-------------------------------------
                    cs1 = cursor1.execute("SELECT name FROM ledger WHERE voucher_id = :vid", {'vid': series.get() + id_to_update.get()})
                    old_name = cs1.fetchone()[0]

                    cs2 = cursor1.execute("SELECT value FROM ledger WHERE voucher_id = :vid", {'vid': series.get() + id_to_update.get()})
                    old_value = cs2.fetchone()[0]

                    #-------------------------------------------update the voucher list table-----------------------------------------------------------
                    cursor1.execute("UPDATE ledger SET voucher_id = :id, name = :name, value = :value WHERE voucher_id= :vid AND action = 'Credit'", {'id': str(series.get()) + str(id_to_update.get()), 'name': new_name, 'value': new_value, 'vid': series.get() + id_to_update.get()})
                    #-------------------------------------------update the ledger table-----------------------------------------------------------
                    # cursor1.execute("UPDATE ledger SET voucher_id = :id, amount = :value WHERE oid= :oid", {'id': str(series) + str(id_to_update.get()), 'value': new_value, 'oid': id_to_update.get()})
                    # old_value = cs.fetchone()[2]
                    cursor1.execute("INSERT INTO modifications(voucher_id, old_name, new_name, old_value, new_value, action, date) VALUES (:voucher_id, :old_name, :new_name, :old_amount, :new_amount, :action, :date)", ((str(series.get()) + str(id_to_update.get())), old_name, new_name, old_value, new_value, action, new_time))
                    # ----------------------commit changes---------------------------------------
                    conn.commit()
                    # ----------------------close database connection (not100% necessary)--------
                    conn.close()
                    messagebox.showinfo("Success!", "Voucher succesfully updated!", parent=update_win)
                    update_win.withdraw()
                except sqlite3.Error as error:
                    messagebox.showwarning("Error!", error, parent=update_win)

            save_mods = Button(update_win, text="Save", command=save_mods, bg='light sea green')
            save_mods.place(x=10, y=140, height=40, width=510)


        id_to_update_label = Label(list_window, text="Insert the voucher ID to update:", fg='white', bg='grey23')
        id_to_update_label.grid(column=0, row=1, columnspan=2, padx=20, pady=10)

        series_to_update = Entry(list_window, width=15)
        series_to_update.insert(END, "ATZ")

        series_to_update.place(x=40, y=45, width=50)
        series_to_update.configure(state=DISABLED)

        id_to_update = Entry(list_window, width=20)
        id_to_update.place(x=90, y=45, width=120)

        update_btn = Button(list_window, text="Update voucher", command=update_voucher, bg='light sea green', relief=RAISED)
        update_btn.place(x=65, y=80, width=120)



        #-------------------------------------delete vouchers------------------------------
        def delete():

            #-----------------------variables for the deleted rows---------------------------------
            series = 'ATZ'
            id_series = str(series) + str(id_to_delete)
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            action = 'Deleted'
            #----------------------------------get the value of the deleted voucher--------------
            try:
                #--------------------sqlite3 database---------------------------------------
                conn = sqlite3.connect('voucher_list.db')
                # ---------------------cursor designation------------------------------------
                cursor1 = conn.cursor()
                # ---------------------query the database-------------------------------------
                cs = cursor1.execute("SELECT name FROM ledger WHERE voucher_id = :vid", {'vid': series + id_to_delete.get()})
                old_name = cs.fetchone()[0]
                cursor1.execute("INSERT INTO modifications(voucher_id, old_name, new_name, old_value, new_value, action, date) VALUES (:voucher_id, :old_name, :new_name, :old_value, :new_value, :action, :date)", (str(series) + str(id_to_delete.get()), old_name, "----", 10, "----", action, time))

                # ----------------------commit changes---------------------------------------
                conn.commit()
                # ----------------------close database connection (not100% necessary)--------
                conn.close()

            except sqlite3.Error as error:
                messagebox.showwarning("Error!", "Failed deleting voucher!", parent=list_window)


            MsgBox = messagebox.askquestion('Delete Voucher!','Are you sure you want to delete this voucher?', icon = 'warning')
            if MsgBox == 'yes':
                # try:
                    #--------------------sqlite3 database---------------------------------------
                    conn = sqlite3.connect('voucher_list.db')
                    # ---------------------cursor designation------------------------------------
                    cursor1 = conn.cursor()
                    # ---------------------query the database-------------------------------------
                    cursor1.execute("DELETE FROM ledger WHERE voucher_id = :id", {'id': str(series) + str(id_to_delete.get())})
                    # cursor1.execute("UPDATE ledger SET action = :action, date = :date WHERE oid= :oid", {'action': action, 'date': time, 'oid': id_to_delete.get()})


                    # ----------------------commit changes---------------------------------------
                    conn.commit()
                    # ----------------------close database connection (not100% necessary)--------
                    conn.close()
                    messagebox.showinfo("Success!", "Voucher succesfully deleted!", parent=list_window)
                    list_window.withdraw()
                # except sqlite3.Error as error:
                    # messagebox.showwarning("Error!", error, parent=list_window)
            else:
                messagebox.showinfo('Cancel','You will now return to the application screen')

        id_to_delete_label = Label(list_window, text="Insert the voucher ID to delete:", fg='white', bg='grey23')
        id_to_delete_label.grid(column=2, row=1, columnspan=2, padx=20, pady=10)

        series_to_delete = Entry(list_window, width=15)
        series_to_delete.insert(END, "ATZ")

        series_to_delete.place(x=290, y=45, width=50)
        series_to_delete.configure(state=DISABLED)

        id_to_delete = Entry(list_window, width=20)
        id_to_delete.place(x=340, y=45, width=120)
        #----------------------------delete button---------------------------------------
        delete_btn = Button(list_window, text="Delete voucher", command=lambda: [delete(), list_window.withdraw(), voucher_list()], bg='red3')
        delete_btn.place(x=315, y=80, width=120)
        #------------------------------refresh table button-------------------------------
        refresh_btn = Button(list_window, text="Refresh", command=lambda: [list_window.withdraw(), voucher_list()], bg='grey', relief=RAISED)
        refresh_btn.place(x=580, y=15, height=80, width=80)

    #------------Menu bar-----------------------------------------------------
    menubar = Menu(root,  bg='grey23', fg='white')
    file = Menu(menubar, tearoff=0, relief=FLAT,bd=0, bg='grey23', fg='white')

    file.add_separator()

    file.add_command(label="Exit", command=root.quit)

    menubar.add_cascade(label="File", menu=file)

    help = Menu(menubar, tearoff=0, relief=GROOVE,bd=0, bg='grey23', fg='white')
    help.add_command(label="About")
    menubar.add_cascade(label="Help", menu=help)

    help.add_separator()

    registration = Menu(menubar, tearoff=0, relief=GROOVE,bd=0, bg='grey23', fg='white')
    registration.add_command(label="Login")
    registration.add_command(label="Logout")
    registration.add_command(label="Register")
    menubar.add_cascade(label="Registration", menu=registration)

    registration.add_separator()

    history = Menu(menubar, tearoff=0, relief=GROOVE,bd=0, bg='grey23', fg='white')
    history.add_command(label="Vouchers status", command=voucher_list)
    history.add_command(label="Modifications", command=modifications)
    menubar.add_cascade(label="History", menu=history)

    root.config(menu=menubar)



    # ###----------------------------BUTTONS---------------------------------------------###

    #------------------------------save button-----------------------------------------
    save_button = Button(root, text="Save voucher", command=lambda: [save(), print(), home()], bg='seagreen1', relief=RAISED)
    save_button.place(x=10, y=200, height=50, width=510)

    #------------------------------withdraw button-----------------------------------------
    withdraw_button = Button(root, text="Withdraw", command=spending_window, bg='goldenrod2', relief=RAISED)
    withdraw_button.place(x=10, y=260, height=50, width=510)

    #-------------------------spent button----------------------------------------------
    get_balance_btn = Button(root, text="Get balance", command=get_balance, bg='IndianRed2', relief=RAISED)
    get_balance_btn.place(x=10, y=320, height=50, width=510)

home()

root.mainloop()
