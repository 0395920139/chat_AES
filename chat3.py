
# import all the required  modules
import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
from libary_aes.encrypt import AES_encrypt
from libary_aes.decrypt import AES_decrypt
# import tkinter as tk
 
# import all functions /
#  everything from chat.py file
# from chat import *
 
PORT = 5000
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
 
# Create a new client socket
# and connect to the server
client = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)
client.connect(ADDRESS)
 
# selected = None
# GUI class for the chat
selected = 0
entrykeyWord = None
description = None
class GUI:
    # constructor method
    def __init__(self):
       
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
         
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False,
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        # create a Label
        self.pls = Label(self.login,
                       text = "Please login to continue",
                       justify = CENTER,
                       font = "Helvetica 14 bold")
         
        self.pls.place(relheight = 0.15,
                       relx = 0.2,
                       rely = 0.07)
        # create a Name
        self.labelName = Label(self.login,
                               text = "Name : ",
                               font = "Helvetica 12")
         
        self.labelName.place(relheight = 0.1,
                             relx = 0.1,
                             rely = 0.2)
        # create a  keyWord                    
        self.keyWord = Label(self.login,
                               text = "key Word : ",
                               font = "Helvetica 12")
         
        self.keyWord.place(relheight = 0.1,
                             relx = 0.1,
                             rely = 0.4)
         
        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                             font = "Helvetica 14")
         
        self.entryName.place(relwidth = 0.4,
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
        # global entrykeyWord
        self.entrykeyWord = Entry(self.login,
                             font = "Helvetica 14")
         
        self.entrykeyWord.place(relwidth = 0.4,
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.4)
        # set key
        def in_var():
            global selected
            choose = var.get()
            if choose == 1:
                selected = "128"
            elif choose == 2:
                selected = "192"
            elif choose == 3:
                selected = "256"
            # print(var.get())
        var = IntVar()
        self.keyOne = Radiobutton(self.login,variable=var,font = "Helvetica 12",text="128",
                                value=1, command=in_var)
        self.keyOne.place(relwidth = 0.3,
                             relheight = 0.1,
                             relx = 0.10,
                             rely = 0.57)
        self.keyTwo = Radiobutton(self.login,variable=var,font = "Helvetica 12",text="192",
                                value=2, command=in_var)
        self.keyTwo.place(relwidth = 0.3,
                             relheight = 0.1,
                             relx = 0.35,
                             rely = 0.57)
        self.keyThree = Radiobutton(self.login,variable=var,font = "Helvetica 12",text="256",
                                value=3, command=in_var)
        self.keyThree.place(relwidth = 0.3,
                             relheight = 0.1,
                             relx = 0.6,
                             rely = 0.57)
        self.entryName.focus()
         
        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text = "Login",
                         font = "Helvetica 14 bold",
                         command = lambda: self.goAhead(self.entryName.get()))
         
        self.go.place(relx = 0.4,
                      rely = 0.7)
        self.Window.mainloop()
 
    def goAhead(self, name):
        # print(selected)
        global entrykeyWord
        entrykeyWord = self.entrykeyWord.get()
        self.login.destroy()
        self.layout(name)
         
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()
 
    # The main layout of the chat
    def layout(self,name):
       
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A",
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
         
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
         
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
        
        self.textCons = Text(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14",
                             padx = 5,
                             pady = 5)
         
        self.textCons.place(relheight = 0.745,
                            relwidth = 1,
                            rely = 0.08)
         
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
         
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
        global description
        description = Text(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
         
        # place the given widget
        # into the gui window
        description.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
         
        description.focus()
         
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda :  self.sendButton(description.get("1.0", "end")))
         
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06,
                             relwidth = 0.22)
         
        self.textCons.config(cursor = "arrow")
         
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
         
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
         
        scrollbar.config(command = self.textCons.yview)
         
        self.textCons.config(state = DISABLED)
 
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        # print(entrykeyWord)
        f = open('libary_aes/XauRo.txt',mode = 'w',encoding = 'utf-8')
        f.write(msg)
        f.close()
        #=========================================================
        AES_encrypt.file_encrypt('libary_aes/XauRo.txt','libary_aes/XauMa.txt',entrykeyWord,selected)
        f = open('libary_aes/XauMa.txt',mode = 'r',encoding = 'utf-8')
        msg = f.read()
        self.textCons.config(state = DISABLED)
        self.msg=msg
        
        description.delete(1.0, END)
        snd= threading.Thread(target = self.sendMessage)
        snd.start()
        # snd.join()
 
    # function to receive messages
    def receive(self):
        while True:
            # try:
                message = client.recv(1024).decode(FORMAT)
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    # message = client.recv(1024).decode(FORMAT)
                    # print(message)
                    print("message nhận đc ",message)
                    data = message.find(":")
                    plain_text1 = message[data + 2:]
                    print("Plantet nhận đc:", plain_text1)
                    wf = open('libary_aes/XauMa1.txt',mode = 'w',encoding = 'utf-8')
                    wf.write(plain_text1)
                    wf.close()
                    with open('libary_aes/XauMa1.txt', encoding='utf8', errors='ignore') as myfile:
                        count = sum(1 for line in myfile if line.rstrip('\n'))
                    # print(" đã vào đến ")
                    AES_decrypt.file_decrypt('libary_aes/XauMa1.txt','libary_aes/XauRo1.txt',entrykeyWord,selected)
                    plain_text2 = ""
                    with open('libary_aes/XauRo1.txt', 'r', encoding='utf8', errors='ignore') as f:
                        datalist = f.readlines()
                    for i in range(count):
                        plain_text2 = plain_text2 + datalist[i]
                    # for i in range(count):dfd # plain_text2 = plain_text2 + fileread +"\n"
                    f.close()
                    print("plantext 2",plain_text2)
                    # print("name",message[:data +2])
                    message = message[:data +2] + plain_text2 
                    print("result:===>",message) 
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END,message+"\n")
                        
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
                
            # except:
            #     # an error will be printed on the command line or console if there's an error
            #     print("An error occured!")
            #     client.close()
            #     break
         
    # function to send messages
    def sendMessage(self):
        print(self.textCons.config(state=DISABLED))
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))   
            break   
 
# create a GUI class object
g = GUI()