import threading
import socket

localhost = '127.0.0.1'
port = 6969

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((localhost, port))

def getJob():
    while True:
        try:
            job = client.recv(1024).decode()
        except Exception:
            client.close()

clientThread = threading.Thread(target=getJob)
clientThread.start()