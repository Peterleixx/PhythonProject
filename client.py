import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from datetime import date

#Assign the port and port of the serser.
Host = '127.0.0.1'
Port = 9999


class Client:
    def __init__(self,host,port):
        self.client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
        login = tkinter.Tk()
        login.withdraw()

        self.username = simpledialog.askstring("User Name","Enter an username: ",parent=login)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.window)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()
    
    def window(self):
        self.win = tkinter.Tk()
        self.board = tkinter.Label(self.win, text="Board")
        self.post_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.subject = tkinter.Label(self.win, text="Subject")
        self.subject_input = tkinter.Text(self.win,height=2)
        self.content = tkinter.Label(self.win, text="Content")
        self.content_input = tkinter.Text(self.win,height=5)

        self.post_button = tkinter.Button(self.win, text="Post",command=self.post)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW ",self.stop)
        self.win.mainloop()

    def post(self):
        subject = f"{self.subject_input.get('1.0','end')}"
        self.subject_input.delete('1.0','end')
        content = f"{self.content_input.get('1.0','end')}"
        self.content_input.delete('1.0','end')
        post = f"From {self.username}:\nSubject: {subject}\nContent: {content}\nDate: {date.today}"

    def stop(self):
        self.running = False
        self.client.close()
        self.win.destroy()
        exit(0)

    def receive(self): 
        while self.running:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'UN':
                    self.client.send(self.username.encode('ascii'))
                else:
                    if self.gui_done:
                        self.post_area.config(state='normal')
                        self.post_area.insert('end',message)
                        self.post_area.yview('end')
                        self.post_area.config(state='disabled')

            except ConnectionAbortedError:
                break

            except:
                print("Error.")
                break


cccc = Client(Host,Port)