import socket
import queue
from threading import Thread
import hashlib
import random

job_queue = queue.Queue()
result_queue = queue.Queue()
result_storage = {}
job_counter = 1

def generate_random_pass():
    # Generate tiga karakter acak untuk setiap bagian dari AAA-ZZZ
    i = chr(random.randint(ord('A'), ord('Z')))
    j = chr(random.randint(ord('A'), ord('Z')))
    k = chr(random.randint(ord('A'), ord('Z')))

    # Gabungkan bagian-bagian tersebut untuk membentuk string acak
    random_string = f"{i}{j}{k}"

    return random_string

def generate_jobs(n: int):
    global job_counter
    for i in range(n):
        # Buat nama job (identifier job)
        job_name = f"job_{job_counter}"
        

        # Buat password yang sudah di hash untuk job tersebut
        job_hash = sha256_hash(generate_random_pass())

        result_storage[job_name] = {
                "answer" : "",
                "hash"   : job_hash
            }

        # Masukkan semua kombinasi untuk job tersebut
        combinations = [f"{chr(i)}{chr(i)}{chr(i)}" for i in range(ord('A'), ord('Z')+1)]
        for j in range(0, len(combinations)-1, 2):
            start_job = combinations[j]
            end_job = combinations[j+1]
            job_queue.put(f"{job_name};{start_job};{end_job};{job_hash}", block=True)
        job_counter += 1


def handle_client(client_socket):
    try:
        while True:
            # Ambil tugas dari queue job
            job = job_queue.get()

            # Kirim tugas ke client
            client_socket.send(job.encode('utf-8'))

            # Terima ACK dari client
            ack = client_socket.recv(1024).decode('utf-8')

            # Proses ACK dari client
            if "ACK" == ack:
                # Jika password tidak ditemukan, lakukan sesuatu
                print(f"Client {client_socket.getpeername()} selesai tanpa menemukan password")
            else:
                # Jika password ditemukan, masukkan hasil ke queue result
                result_queue.put(ack)
                print(f"Client {client_socket.getpeername()} menemukan password {ack}")
    except Exception as err:
        print(f"Client {client_socket.getpeername()} disconnected")

def main():
    JOBS = 3
    print("[*] Generating jobs...")
    generate_jobs(JOBS)
    print(f"[*] {JOBS} jobs generated")
    print(f"[*] Launching console interface...")
    console_interface = Thread(target=interface)
    console_interface.start()
    print(f"[*] For available commands type HELP in the console")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 6000))
    server.listen(5)

    print("[*] Listening on 127.0.0.1:6000")

    while True:
        client, addr = server.accept()
        print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

        # Legacy
        # Inisiasi queue dengan sequence AAA hingga ZZZ
        # combinations = [f"{chr(i)}{chr(i)}{chr(i)}" for i in range(ord('A'), ord('Z')+1)]

        # for combination in combinations:
        #     job_queue.put(combination)

        client_handler = Thread(target=handle_client, args=(client,))
        client_handler.start()

def sha256_hash(raw_pass):
    # Membuat objek hash SHA-256
    h = hashlib.new('sha256')

    # Mengkonversi string menjadi bytes dan melakukan hashing
    h.update(raw_pass.encode())

    # Mendapatkan nilai hash dalam bentuk hex
    hashed_result = h.hexdigest()

    return hashed_result

def store_result():
    while result_queue.qsize() > 0:
        data = result_queue.get()
        ack, result = data.split()
        answer, job_name = result.split(";")
        if (job_name in result_storage):
            result_storage[job_name]["answer"] = answer
        else:
            print(f"[*] {job_name};{answer} was not stored")

def interface():
    while True:
        command = input()
        print()

        if command == 'HELP':
            print('\"GENERATE {N}\"   generates N amount of new JOBS')
            print('\"JOBS\"             prints job left in the queue')
            print('\"RESULTS\"          imports results_queue into results_storage and displays it')
            print()
        elif 'GENERATE ' in command:
            try:
                print(f"[*] attempting to generate jobs...")
                n = command.split()[1]
                generate_jobs(int(n))
                print(f"[*] generated {n} jobs successfully")
            except Exception as err:
                print(f"[*] failed to generate jobs")
                print(f"{err}")
            finally:
                print()
        elif command == 'JOBS':
            print(f"[*] there are {job_queue.qsize()} jobs in the queue")
            print()
        elif command == 'RESULTS':
            store_result()
            print("  Name \tAnswer\tHash")
            for key, value in result_storage.items():
                print(f"  {key} \t{value['answer']}\t{value['hash']}")
            print()


if __name__ == "__main__":
    main()