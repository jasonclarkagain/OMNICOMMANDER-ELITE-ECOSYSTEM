import socket

def start_server(ip="0.0.0.0", port=9999):
    # This creates the listener on your Kali machine
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f"[*] Omnicommander Elite C2 Server active on port {port}...")

    while True:
        client, addr = server.accept()
        print(f"[+] Connection from {addr[0]}:{addr[1]}")
        try:
            data = client.recv(4096)
            if data:
                print(f"[*] Received: {data.decode(errors='ignore')}")
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            client.close()

if __name__ == "__main__":
    start_server()
