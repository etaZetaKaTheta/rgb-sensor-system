# socket_echo_client.py
import socket
import sys
import tkinter as tk

ip_was_false = True

i = 1

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

getColorFuncName = "getcolor"
sockCloseFuncName = "closesocket"

def connect_to_server():
    try:
        print(ip_var.get())
        server_address = (ip_var.get(), 18769)
        print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)
    except Exception:
        global ip_was_false
        if (ip_was_false == True):
            label2 = tk.Label(root, text = "Falsche IP-Adresse!", fg = '#ff0000')
            label2.pack()
            ip_was_false = False

def request_color():
    message = getColorFuncName.encode()
    sock.sendall(message)

    data = sock.recv(16)
    global i
    lb1.insert(i, data.decode('utf-8'))
    i = i + 1
    print(data.decode('utf-8'))

def close_socket():
    message = sockCloseFuncName.encode()
    sock.sendall(message)

root = tk.Tk()
root.geometry("250x170")

ip_var = tk.StringVar()

label1 = tk.Label(root, text="RGB-Sensor-System")
label1.pack()

ip_feld = tk.Entry(root, textvariable = ip_var)
ip_feld.pack()

schaltf1 = tk.Button(root, text="Verbinde zum Server", command=connect_to_server)
schaltf1.pack()

schaltf2 = tk.Button(root, text="Farberkennung", command=request_color)
schaltf2.pack()

lb1 = tk.Listbox()



root.mainloop()
