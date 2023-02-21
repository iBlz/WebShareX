import eel
from vnc import VNC
from threading import Thread
import atexit
import sys
from vnc import VNC

status = 'None'
connection = 'None'
vnc = VNC()

eel.init('web')

@eel.expose
def host():
    global status
    global vnc
    global transmit_thread
    print('Hosting...')
    status = 'host'
    transmit_thread = Thread(target=vnc.transmit)
    transmit_thread.daemon = True
    transmit_thread.start()

@eel.expose
def stop_host():
    global status
    status = 'None'
    print("Stopping server...")

@eel.expose
def connect(ip):
    global status
    global vnc
    global connection
    print('Connecting...')
    status = 'client'
    vnc.ip = ip
    try:
        vnc.start_receive()
        connection = 'active'
    except Exception as e:
        print('Connection failed...')

eel.start('index.html', block=False, mode=None, port=80, host="10.42.0.86")

base = vnc.image_serializer()

while True:
    eel.updateScreen(vnc.image_serializer().decode())
    eel.sleep(.01)