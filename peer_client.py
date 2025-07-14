import socket

def download_file(from_ip, from_port, filename, save_path):
    s = socket.socket()
    s.connect((from_ip, int(from_port)))
    s.send(filename.encode())
    with open(save_path, 'wb') as f:
        while True:
            data = s.recv(1024)
            if not data:
                break
            f.write(data)
    s.close()
