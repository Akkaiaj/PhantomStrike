# PhantomStrike v2 - Advanced C2 Framework  
**Ethical Penetration Testing Only** | MIT License
██████╗ ██╗  ██╗ █████╗ ███╗   ███╗ ████████╗ ███████╗ ██╔══██╗██║  ██║██╔══██╗████╗ ████║ ╚══██╔══╝ ██╔════╝ ██████╔╝███████║███████║██╔████╔██║    ██║    █████╗
██╔═══╝ ██╔══██║██╔══██║██║╚██╔╝██║    ██║    ██╔══╝
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║    ██║    ███████╗ ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝    ╚══════╝ PhantomStrike - C2 Framework
> **A lightweight, encrypted, stealth-oriented C2 for red team operations.**  
> **Now with Web Panel, RSA+AES encryption, multi-agent, and persistence.**

---

## Features

| Feature | Status |
|-------|--------|
| RSA + AES Key Exchange | Done |
| Web Dashboard (Flask) | Done |
| Multi-Agent Management | Done |
| System Info on Connect | Done |
| Jitter + Auto-Reconnect | Done |
| Linux Persistence | Done |
| Fileless Execution | Done |
| Command History | Done |

---

## Files

- `web_panel.py` → **C2 Server + Web UI** (http://localhost:5000)
- `phantom_agent.py` → **Stealth Implant** (Linux)
- `phantom_c2.py` → **Legacy CLI Server** (deprecated)

---

## Quick Start

### 1. Install Dependencies
```bash
pip install flask pycryptodome
2. Start C2 Web Panel
python3 web_panel.py
→ Open browser: http://YOUR_IP:5000
→ Copy the Public Key from terminal.
3. Configure Agent
Edit phantom_agent.py:
C2_HOST = "YOUR_C2_IP"
Paste the public key into C2_PUB_KEY_PEM.
4. Deploy Agent
python3 phantom_agent.py
5. Control from Web
Click agent → Send commands
View output in real-time 
Commands
whoami
pwd
ls -la
screenshot        [coming]
download file.txt
exit
Screenshots
�
Live agent control with terminal
Security
AES-256-EAX authenticated encryption
RSA-2048 key exchange
No plaintext on wire
Jittered beacons (3–8s)
Self-cleaning 
Persistence (Linux)
# Requires root
sudo python3 phantom_agent.py
→ Installs to /var/tmp/.phantom + @reboot cron
Disclaimer
For authorized security testing only.
Do not use on systems without explicit permission.
The author is not responsible for misuse.
Author
Original: @Akkaiaj

Support the Project
[!["Buy Me A Coffee"](https://img.shields.
