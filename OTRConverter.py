#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import os
from Tkinter import *
import tkFileDialog

from adiumproperties import AdiumProperties
from gibberbotproperties import GibberbotProperties
from jitsiproperties import JitsiProperties
from irssiproperties import IrssiProperties
from pidginproperties import PidginProperties

class MenuBar(Menu):

    def __init__(self, parent):
        Menu.__init__(self, parent)

        fileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=fileMenu)
        fileMenu.add_command(label='Convert', underline=1, command=parent.convert)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=1, command=self.quit)

    def quit(self):
        sys.exit(0)


class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.setupwindow(self)

    def setupwindow(self, master):
        fromcolor = 'grey'
        tocolor = 'lightblue'

        self.fromframe = LabelFrame(master, text='Convert from:',
                               bg=fromcolor, padx=5, pady=5)
        self.fromframe.pack(side=TOP, padx=5, pady=5, expand=True, fill=BOTH)

        optionslist = self.detectfiles()
        self.fromapp = StringVar(master)
        self.fromapp.set(optionslist[0]) # initial value
        self.option = OptionMenu(self.fromframe, self.fromapp, *optionslist,
                                           command=self.select_app)
        self.option.configure(bg=fromcolor, relief=RAISED, width=20)
        self.option.pack(side=TOP)
        self.option['menu'].add_separator()
        self.option['menu'].add_command(label='Selected Folder...',
                                        command=self.select_folder)

        self.fromfolder = StringVar()
        self.fromfolder.set(self.getpath(optionslist[0]))
        self.fromentry = Entry(self.fromframe, highlightbackground=fromcolor,
                               textvariable=self.fromfolder,
                               state='readonly')
        self.fromentry.pack(side=LEFT, expand=True, fill=X)
        self.fromchoosebutton = Button(self.fromframe, text='Choose...',
                                       highlightbackground=fromcolor,
                                       command=self.choose_fromfolder,
                                       state='disabled')
        self.fromchoosebutton.pack(side=LEFT)

        self.toframe = LabelFrame(master, text='to:',
                        bg=tocolor, padx=5, pady=5)
        self.toframe.pack(side=TOP, padx=5, pady=5, expand=True, fill=BOTH)
        self.wherelabel = Label(self.toframe, text='Your converted keys will be written to:',
                           bg=tocolor)
        self.wherelabel.pack(side=TOP, expand=True, fill=X, anchor=NW)
        self.tofolder = StringVar()
        self.tofolder.set(os.path.expanduser('~/Desktop'))
        self.filenameentry = Entry(self.toframe, highlightbackground=tocolor,
                                   textvariable=self.tofolder)
        self.filenameentry.pack(side=LEFT, expand=True, fill=X)
        self.choosebutton = Button(self.toframe, text='Choose...',
                                   highlightbackground=tocolor,
                                   command=self.choose_tofolder)
        self.choosebutton.pack(side=LEFT)

        self.button = Button(master, text="Convert!", command=self.convert)
        self.button.pack(side=BOTTOM, padx=5, pady=5)

    def select_app(self, app=None):
        self.fromfolder.set(self.getpath(app))
        self.fromentry.configure(state='readonly')
        self.fromchoosebutton.configure(state='disabled')

    def select_folder(self):
        self.fromapp.set('Select Folder...')
        self.fromentry.configure(state='normal')
        self.fromchoosebutton.configure(state='normal')

    def choose_fromfolder(self):
        dirname = tkFileDialog.askdirectory(initialdir=self.fromfolder.get(),
                                            title='Please select a directory')
        if len(dirname) > 0:
            self.fromfolder.set(dirname)

    def choose_tofolder(self):
        dirname = tkFileDialog.askdirectory(initialdir=self.tofolder.get(),
                                            title='Please select a directory')
        if len(dirname) > 0:
            self.tofolder.set(dirname)

    def getpath(self, app):
        '''output the standard path of a given app'''
        if app == 'adium':
            return AdiumProperties.path
        elif app == 'jitsi':
            return JitsiProperties.path
        elif app == 'irssi':
            return IrssiProperties.path
        elif app == 'pidgin':
            return PidginProperties.path
        else:
            return None

    def detectfiles(self):
        '''detect which apps are installed based on the existence of OTR files'''
        haveapps = []
        if os.path.exists(AdiumProperties.path):
            haveapps.append('adium')
        if os.path.exists(JitsiProperties.path):
            haveapps.append('jitsi')
        if os.path.exists(IrssiProperties.path): 
            haveapps.append('irssi')
        if os.path.exists(PidginProperties.path):
            haveapps.append('pidgin')
        return haveapps

    def convert(self):
        '''run the conversion from one file set to another'''
        app = self.fromapp.get()
        keys = None
        print 'Parsing ', app
        if app == 'adium':
            keys = AdiumProperties.parse()
        elif app == 'jitsi':
            keys = JitsiProperties.parse()
        elif app == 'irssi':
            keys = IrssiProperties.parse()
        elif app == 'pidgin':
            keys = PidginProperties.parse()
        else:
            return None
        if keys:
            GibberbotProperties.write(keys, self.tofolder.get())

#------------------------------------------------------------------------------#
# main

root = App()
windowingsystem = root.tk.call('tk', 'windowingsystem')

root.title('OTRConverter')
root.geometry('520x240')
root.minsize(280, 220)
root.mainloop()

