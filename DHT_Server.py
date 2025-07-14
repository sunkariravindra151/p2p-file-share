import socket
import threading

file_registry = {}  # {filename: (peer_ip, peer_port)}

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            parts = data.split('|')
            cmd = parts[0]

            if cmd == "REGISTER":
                filename = parts[1]
                peer_ip = parts[2]
                peer_port = parts[3]
                file_registry[filename] = (peer_ip, peer_port)
                print(f"Registered file '{filename}' from peer {peer_ip}:{peer_port}")
                conn.send(b"REGISTERED")

            elif cmd == "SEARCH":
                filename = parts[1]
                if filename in file_registry:
                    peer_ip, peer_port = file_registry[filename]
                    response = f"{peer_ip}|{peer_port}"
                    print(f"Search for '{filename}' found at {response}")
                    conn.send(response.encode())
                else:
                    print(f"Search for '{filename}' found nothing")
                    conn.send(b"NOTFOUND")

        except Exception as e:
            print(f"Error: {e}")
            break
    conn.close()
    print(f"Connection closed from {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(("0.0.0.0", 9000))  # Listen on all interfaces
    except Exception as e:
        print(f"Bind failed: {e}")
        return

    server.listen(5)
    print("DHT Server running on port 9000...")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
