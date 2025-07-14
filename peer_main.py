import socket
import threading
import os
from peer_server import start_server
from peer_client import download_file
from utils import hash_file

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

PEER_IP = get_local_ip()
PEER_PORT = int(input("Enter port for this peer (e.g. 10000): "))

shared_folder = "shared"
download_folder = "downloads"

os.makedirs(shared_folder, exist_ok=True)
os.makedirs(download_folder, exist_ok=True)

threading.Thread(target=start_server, args=(PEER_IP, PEER_PORT, shared_folder), daemon=True).start()

DHT_SERVER_IP = "192.168.113.89"
DHT_SERVER_PORT = 9000

def register_file(filename):
    s = socket.socket()
    s.connect((DHT_SERVER_IP, DHT_SERVER_PORT))
    cmd = f"REGISTER|{filename}|{PEER_IP}|{PEER_PORT}"
    s.send(cmd.encode())
    print(s.recv(1024).decode())
    s.close()

def search_file(filename):
    s = socket.socket()
    s.connect((DHT_SERVER_IP, DHT_SERVER_PORT))
    cmd = f"SEARCH|{filename}"
    s.send(cmd.encode())
    response = s.recv(1024).decode()
    s.close()
    if response == "NOTFOUND":
        return None
    return response.split('|')

while True:
    print("\n1. Register File\n2. Download File\n3. Exit")
    ch = input("Choose: ")
    if ch == "1":
        fname = input("Filename in shared folder: ")
        if os.path.exists(os.path.join(shared_folder, fname)):
            register_file(fname)
        else:
            print("File does not exist.")
    elif ch == "2":
        fname = input("Enter filename to search: ")
        location = search_file(fname)
        if location:
            ip, port = location
            save_path = os.path.join(download_folder, fname)
            download_file(ip, int(port), fname, save_path)
            print("Download complete.")
        else:
            print("File not found.")
    elif ch == "3":
        break
