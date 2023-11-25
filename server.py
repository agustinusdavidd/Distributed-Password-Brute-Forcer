import threading
import socket

localhost = '127.0.0.1'
port = 6969

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((localhost, port))
server.listen()

clients = []
job = [[]]
result = [[]]

def sendJob(job):
    for client in clients:
        client.send(job.encode())

def clientHandler(client):
    while True:
        try:
            for j in job:
                sendJob(j)
        except Exception:
            index = clients.index(client)
            print(f"{clients[index]} is disconnected to the server")
            clients.remove(client)
            client.close()
            break
            
def receive():
    while True:
        print("Server running")
        client, addr = server.accept()
        print(f"connection is established with {addr}")
        clients.append(client)
        thread = threading.Thread(target=clientHandler, args=(client, ))
        thread.start()

receive()