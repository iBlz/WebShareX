from PIL import Image
from io import BytesIO
import socket
import mss
import base64
import struct
import time
import pyautogui
from PIL import Image, ImageDraw


class VNC:
    def __init__(self, ip='10.42.0.86', port=7000):
        self.ip = ip
        self.port = port

    def rgba_to_rgb(self, img):
        # Convert RGBA image to RGB image
        if img.mode == "RGBA":
            r, g, b, a = img.split()
            rgb_img = Image.merge("RGB", (r, g, b))
            return rgb_img
        else:
            return img
        
    def screenshot(self):
        with mss.mss() as sct:
            display = 3
            monitor = sct.monitors[display]
            sct_img = sct.grab(monitor)
            cursor_x, cursor_y = pyautogui.position()
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            draw = ImageDraw.Draw(img)
            cursor_x=cursor_x-1919
            cursor_y=cursor_y+1
            draw.ellipse((cursor_x-5, cursor_y-5, cursor_x+5, cursor_y+5), fill=(255, 0, 0))
        return self.rgba_to_rgb(img)

    def image_serializer(self, resolution=(768, 1360)):
        image = self.screenshot().resize(resolution, Image.ANTIALIAS)
        buffer = BytesIO()
        image.save(buffer, format='jpeg')
        data_string = base64.b64encode(buffer.getvalue())
        return data_string

    def image_deserializer(self, image_string):
        return Image.open(BytesIO(base64.b64decode(image_string)))

    def send_msg(self, sock, msg):
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def recv_msg(self, sock):
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def transmit(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender:
            sender.bind((self.ip, self.port))
            sender.listen()
            print('Waiting for connection...')
            conn, addr = sender.accept()
            with conn:
                print('Connected by', addr)      
                while True:
                    self.send_msg(conn, self.image_serializer())
    
    def start_receive(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.ip, self.port))
        print("Connected to ", self.ip, ":", self.port)

    def receive(self):    
        try:
            data_string = self.recv_msg(self.conn)
            return data_string.decode()
            self.image.show()
        except Exception as e:
            print(e)
        return None
    