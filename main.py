#!/usr/bin/python3

import cv2 as cv
import socket
import sys

from null_preview import *
from picamera2 import *

currentColor = ""
lastColor = ""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (str(sys.argv[1]), 18769)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
picam2 = Picamera2()
preview = NullPreview(picam2)
picam2.configure(picam2.preview_configuration(main={"size":(640, 480)}))
picam2.start()
sock.listen(100)
connection, client_address = sock.accept()

def evaluate_current_frame():
    img = picam2.capture_array()

    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    Z = img.reshape((-1,3))
    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 1
    ret,label,center=cv.kmeans(Z,K,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))

    

    (b, g, r) = cv.split(res2)

    b_mean = np.mean(b)
    g_mean = np.mean(g)
    r_mean = np.mean(r)
  
    # displaying the most prominent color
    if (b_mean > g_mean and b_mean > r_mean):
        currentColor = "blue"
    elif (g_mean > r_mean and g_mean > b_mean):
        currentColor = "green"
    else:
        currentColor = "red"

    message = currentColor.encode()
    connection.sendall(message)

def close_socket():
    sock.close()

while True:
    try:
        data = connection.recv(16)
        dataBuffer = data.decode('utf-8')
        if(dataBuffer == "getcolor"):
            evaluate_current_frame()
        elif(dataBuffer == "closesocket"):
            close_socket()


    except OSError:
        print("STOPPED")
        sock.close()
        break

    except KeyboardInterrupt:
        print("STOPPED")
        sock.close()
        break

