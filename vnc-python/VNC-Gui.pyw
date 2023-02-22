from tkinter import *
import subprocess
import pymsgbox
import threading
import getpass
import time
from datetime import datetime
import psutil
import sys
import os
import pyglet

setup_int = 0
check_int = 0
user = getpass.getuser()
configfile = ('C:\\Users\\{}\AppData\\Local\\Temp\\tplink-controler-ip.txt' .format(user))

window = Tk()

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

pyglet.font.add_file(resource_path('font.ttf'))

def setup():
    global setup_int
    if setup_int == 0:
        os.system("deviceinstaller64.exe install usbmmidd.inf usbmmidd")
        os.system("deviceinstaller64.exe enableidd 1")
        setup_int = 1
    else:
        pymsgbox.alert('Screen is already setup!', '⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️')

def start():
    global check_int
    if setup_int == 1:
        if check_int == 0:
            check_int = 1
            os.system("python %s" % resource_path("app.pyw"))
        else:
            pymsgbox.alert('Screen capture is already running!', '⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️')
    else:
        pymsgbox.alert('You have to run the setup before starting the screen capture!', '⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️')

def update_info_box():
    while True:
        time.sleep(2)
        info_box.configure(state='normal',exportselection=0)
        info_box.delete('1.0', END)
        info_box.insert("end","""Time : {}\nCPU : {}\nRAM : {}%""".format(datetime.now().strftime("%H:%M:%S"),psutil.cpu_percent(),psutil.virtual_memory()[2]))
        info_box.configure(state='disabled',exportselection=0)
        info_box.see("end")
 
window.geometry('270x320')
window.resizable('0', '0')
window.title("VNC Gui")
icon = PhotoImage(file=resource_path("images\\icon.png"))
window.iconphoto(False, icon)
window.configure(background='#f8f4f4')

box1_img = PhotoImage(file=resource_path("images\\logo.png"))
box1 = Canvas(window, width = 354, height = 40, highlightthickness=0, bd=0)
box1.create_image(0, 0, anchor=NW, image=box1_img) 
box1.place(x=10,y=10)

setup_img=PhotoImage(file=resource_path("images\\setup.png"))
setup_button = Button(window, highlightthickness=0, bd=0, text='', image=setup_img, command=lambda: setup())
setup_button.pack(ipadx=5, ipady=5, expand=True)
setup_button.place(x=10, y=70)

start_img=PhotoImage(file=resource_path("images\\start.png"))
start_button = Button(window, highlightthickness=0, bd=0, text='', image=start_img, command=lambda: threading.Thread(target=start).start())
start_button.pack(ipadx=5, ipady=5, expand=True)
start_button.place(x=10, y=120)

info_box = Text(window,height=10,width=50,background='#f8f4f4',bd=0,fg='#000000')
info_box.place(x=20,y=170)
info_box.config(font=('Kanit Black', 20))
info_box.configure(state='disabled',exportselection=0)

threading.Thread(target=update_info_box).start()

window.mainloop()