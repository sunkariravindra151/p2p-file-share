import socket
import threading
import os

def handle_client(conn, addr, shared_folder):
    filename = conn.recv(1024).decode()
    file_path = os.path.join(shared_folder, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            conn.sendfile(f)
    conn.close()

def start_server(peer_ip, peer_port, shared_folder):
    server = socket.socket()
    server.bind((peer_ip, peer_port))
    server.listen(5)
    print(f"[SERVER] Peer listening on {peer_ip}:{peer_port}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr, shared_folder)).start()
