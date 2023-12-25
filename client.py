import socket
import hashlib

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 6000))

    while True:
        # Terima tugas dari server
        job = client.recv(1024).decode('utf-8')
        print(job)
        job_name, start_job, end_job, hash_password = job.split(';')

        current_job = start_job

        password_found = False

        while current_job <= end_job:

            # Lakukan brute force untuk mencari password
            # (Pada contoh ini, kita hanya mencetak password yang dicoba)
            print(f"Trying password: {current_job}")
            hashed_job = sha256_hash(current_job)

            # Cek apakah password ditemukan
            if hashed_job == hash_password:
                # Set boolean kalo password ditemukan dan break looping
                # (Hanya ada 1 kombinasi yang benar)
                password_found = True
                break

            current_job = increment_sequence(current_job)
        
        if password_found:
            # Kirim ACK dan password ke server jika ditemukan
            print(f"Password found {current_job} on {start_job}-{end_job}")
            client.send(f"ACK {current_job};{job_name}".encode('utf-8'))
        else:
            # Kirim ACK jika password tidak ditemukan
            client.send('ACK'.encode('utf-8'))   

def increment_sequence(sequence):
    # Fungsi ini menangani peningkatan ke nilai berikutnya dalam sequence
    # Misalnya, dari "AAA" ke "AAB", atau dari "ZZZ" ke "AAAA"
    sequence = list(sequence)
    
    # Cek apakah kita perlu menambah digit atau tidak
    for i in range(len(sequence)-1, -1, -1):
        if sequence[i] == 'Z':
            sequence[i] = 'A'
        else:
            sequence[i] = chr(ord(sequence[i]) + 1)
            break

    return ''.join(sequence)

def sha256_hash(raw_pass: str):
    # Membuat objek hash SHA-256
    h = hashlib.new('sha256')

    # Mengkonversi string menjadi bytes dan melakukan hashing
    h.update(raw_pass.encode())

    # Mendapatkan nilai hash dalam bentuk hex
    hashed_result = h.hexdigest()

    return hashed_result

if __name__ == "__main__":
    main()
