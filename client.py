# socket_echo_client.py
import re
import socket
import sys
import tkinter as tk

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

getColorFuncName = "getcolor"
sockCloseFuncName = "closesocket"

def connect_to_server():
    # connect socket to port where server is listening
    server_address = ('192.168.137.123', 18769)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

def request_color():
    message = getColorFuncName.encode()
    sock.sendall(message)

    data = sock.recv(16)
    print(data.decode('utf-8'))

def close_socket():
    message = sockCloseFuncName.encode()
    sock.sendall(message)

root = tk.Tk()
root.geometry("150x100")

label1 = tk.Label(root, text="RGB-Sensor-System")
label1.pack()

schaltf1 = tk.Button(root, text="Connect to server", command=connect_to_server)
schaltf1.pack()

schaltf2 = tk.Button(root, text="Request color", command=request_color)
schaltf2.pack()

root.mainloop()
