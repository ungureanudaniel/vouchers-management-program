from tkinter import ttk

def style1():
    combostyle = ttk.Style()
    combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'yellow',
                                       'fieldbackground': 'black',
                                       'background': 'grey'
                                       }}}
                         )
    style1=combostyle.theme_use('combostyle')



def style2():
    combostyle = ttk.Style()
    combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'black',
                                       'fieldbackground': 'white',
                                       'background': 'grey'
                                       }}}
                         )
    style2=combostyle.theme_use('combostyle')


def style3():
    combostyle = ttk.Style()
    combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'black',
                                       'fieldbackground': 'white',
                                       'background': 'grey'
                                       }}}
                         )
    style3=combostyle.theme_use('combostyle')


def style4():
    combostyle = ttk.Style()
    combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'black',
                                       'fieldbackground': 'white',
                                       'background': 'grey'
                                       }}}
                         )
    style4=combostyle.theme_use('combostyle')
