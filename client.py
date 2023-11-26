import threading
import requests
import json
import hashlib

def encode256(string: str) -> str :
    h = hashlib.new('sha256')
    h.update(string.encode())
    return h.hexdigest()

# implementasi apabila menggunakan API
def postResult(jobName: str, sequence: str):
    headers = {"Content-Type" : "Application/json"}
    body = {
        'name' : jobName,
        'seq' : sequence
        }
    response = requests.post('http://127.0.0.1:8000/result', headers=headers, json=body)
    print(response)

# Logic dasar aplikasi :
# Ambil request
job = requests.get('http://127.0.0.1:8000/job')

# Parse request
job_line = job.json()
print(job.json())

# Loop hingga job habis
while job_line['name'] != 'Empty':
    
    # Enkripsi sequence ke sha256
    enc = encode256(job_line['seq'])

    # Bandingkan hasil enkripsi
    if enc == job_line['enc'] :
        # Kirim reply ke server apabila benar
        postResult(job_line['name'], job_line['seq'])

    # Request job baru
    job = requests.get('http://127.0.0.1:8000/job')

    # Parse job baru
    job_line = job.json()
    print(job.json())


# implementasi socket

# localhost = '127.0.0.1'
# port = 6969

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((localhost, port))

# def getJob():
#     while True:
#         try:
#             job = client.recv(1024).decode()
#         except Exception:
#             client.close()

# clientThread = threading.Thread(target=getJob)
# clientThread.start()