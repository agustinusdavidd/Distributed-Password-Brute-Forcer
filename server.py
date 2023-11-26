import threading
import socket
# fast api modules
import fastapi as api
from pydantic import BaseModel
import json
# modules for logic
from random import randint
import hashlib

# running versi API => uvicorn server:app --reload

# encode string dengan sha256
def encode256(string: str) -> str :
    
    h = hashlib.new('sha256')
    h.update(string.encode())
    return h.hexdigest()

# encode angka ke row of char
def encodeChar(x: int) -> str :
    result = ""
    if x == 0:
        return chr(64 + (x % 26))
    while (x > 0) :
        result += chr(64 + (x % 26) )
        x = x // 26
    return result[::-1]

# TODO : split job ke N buah client
# def getWorkload(N: int, iter: int) -> str :


def generateJob(n: int):
    global jobs
    global passwords
    for i in range(n):
        # generate password untuk job i

        password = ""
        password = password.join([chr(randint(65,90)) for i in range(3)])
        password = encode256(password)
        passwords.append({
            'enc' : password,
            'solution'  : ""
        })

        # TODO
        # generate jumlah listing untuk job i 
        # nJobs = randint(5,26)
        # step = (26**3) // nJobs


        # for j in range(nJobs):

        #     jobs.append({
        #         'name' : 'job' + str(i+1),
        #         'enc' : password,
        #         '' 
        #     })

        # (temp fix) generate semua kemungkinan kombinasi untuk job i
        for j in range(750):
            sequence = encodeChar(j)
            if not ( "@" in sequence ) :
                jobs.append({
                    'name' : 'job' + str(i+1),
                    # 'enc' : password,
                    'enc' : encode256("AA"),
                    'seq' : encodeChar(j)
                })

# local database
jobs = []
result = []
passwords = []

# generate N buah job (N buah password)
N = 1
generateJob(N)

# implementasi dengan membuat API
app = api.FastAPI()

# path root, menampilkan semua path yang ada
@app.get('/')
async def root():
    return {
        'paths' : {
            'get' : [
                {'/job' : {
                    'input' : ['None'],
                    'return' : ['name', 'enc', 'seq']
                }},
                {'/result' : {
                    'input' : ['None'],
                    'return' : ['result']
                }}
            ],
            'post' : [
                {'/result' : {
                    'input' : ['seq', 'name'],
                    'return' : ['None']
                }}
            ]
        }
    }

# path untuk request job
@app.get('/job')
async def getJob():
    global jobs
    if len(jobs) > 0:
        return jobs.pop()
    else:
        return {
            'name' : 'Empty',
            'enc' : None,
            'seq' : None,
        }

# format body message yang diterima
class Result(BaseModel):
    name: str
    seq: str

# mengembalikan list result yang sudah terkumpul
@app.get('/result')
async def getResults():
    global result
    return result

# path untuk menerima result dari client
@app.post('/result')
async def receiveResult(res : Result):
    global result
    result.append({
        'name' : res.name,
        'seq'  : res.seq
    })

# implementasi socket

# localhost = '127.0.0.1'
# port = 6969

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((localhost, port))
# server.listen()

# clients = []
# job = [[]]
# result = [[]]

# def sendJob(job):
#     for client in clients:
#         client.send(job.encode())

# def clientHandler(client):
#     while True:
#         try:
#             for j in job:
#                 sendJob(j)
#         except Exception:
#             index = clients.index(client)
#             print(f"{clients[index]} is disconnected to the server")
#             clients.remove(client)
#             client.close()
#             break
            
# def receive():
#     while True:
#         print("Server running")
#         client, addr = server.accept()
#         print(f"connection is established with {addr}")
#         clients.append(client)
#         thread = threading.Thread(target=clientHandler, args=(client, ))
#         thread.start()

# receive()