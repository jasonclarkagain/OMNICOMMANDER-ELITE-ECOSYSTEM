import asyncio, aiohttp, os, subprocess, json, base64, hashlib, random, string
from datetime import datetime
from pathlib import Path

# --- CONFIG ---
GITHUB_USER = "jasonclarkagain"
OLLAMA_URL = "http://localhost:11434/api/generate"
ROOT = Path("~/omnicommander_elite").expanduser()
MEMORY_DIR = ROOT / "memory"

for d in [ROOT, MEMORY_DIR]: d.mkdir(parents=True, exist_ok=True)

def get_daily_key():
    return hashlib.sha256(datetime.now().strftime("%Y-%m-%d").encode()).hexdigest()[:16]

def obfuscate(code):
    key = get_daily_key()
    xor_bytes = bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(code)])
    b64 = base64.b64encode(xor_bytes).decode()
    return (
        f"import base64,hashlib,datetime;"
        f"k=hashlib.sha256(datetime.datetime.now().strftime('%Y-%m-%d').encode()).hexdigest()[:16];"
        f"d=base64.b64decode('{b64}');"
        f"exec(''.join([chr(b^ord(k[i%len(k)])) for i,b in enumerate(d)]))"
    )

class EliteSwarm:
    def __init__(self, mission_name):
        self.name = mission_name
        self.path = ROOT / mission_name
        self.path.mkdir(parents=True, exist_ok=True)

    async def ask_llm(self, role, prompt):
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "wizardlm2:7b",
                "system": f"You are the {role}. Return ONLY code or raw data. No talk.",
                "prompt": prompt, "stream": False
            }
            try:
                async with session.post(OLLAMA_URL, json=payload, timeout=90) as resp:
                    data = await resp.json()
                    return data.get('response', "").strip()
            except Exception as e:
                return f"ERROR: {str(e)}"

    async def execute(self, objective):
        print(f"[*] Mission Alpha: {self.name}")
        files_to_build = ["main.py", "README.md"]
        build_report = []

        for f in files_to_build:
            success = False
            attempts = 0
            current_code = ""

            while not success and attempts < 3:
                attempts += 1
                print(f"[*] {f} - Attempt {attempts}...")
                
                # 1. Developer Generation
                current_code = await self.ask_llm("Developer", f"Task: Write {f} for {objective}")
                
                # 2. Red Team Audit
                if f.endswith(".py"):
                    audit_res = await self.ask_llm("Red Team Auditor", f"Audit this code for vulnerabilities: {current_code}. Return 'PASS' or a list of flaws.")
                    if "PASS" in audit_res.upper():
                        print(f"[+] {f} passed Red Team Audit.")
                        success = True
                    else:
                        print(f"[!] {f} FAILED Audit: {audit_res[:100]}... Retrying.")
                else:
                    success = True

            # 3. Obfuscate and Save
            final_content = obfuscate(current_code) if f.endswith(".py") else current_code
            (self.path / f).write_text(final_content)
            build_report.append(f"{f}: Attempt {attempts}")

        # 4. Finalize & Deploy
        learnings = {"mission": self.name, "report": build_report, "date": str(datetime.now())}
        (self.path / "LEARNINGS.md").write_text(json.dumps(learnings, indent=4))
        
        os.chdir(self.path)
        subprocess.run(["git", "init"], capture_output=True)
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Elite Build {self.name}"], capture_output=True)
        
        repo_name = f"ELITE-{self.name}-{os.urandom(2).hex()}"
        subprocess.run(["gh", "repo", "create", repo_name, "--public", "--source=.", "--push"], capture_output=True)
        
        url = f"https://github.com/{GITHUB_USER}/{repo_name}"
        print(f"✅ Mission Success: {url}")
        return url

if __name__ == "__main__":
    import sys
    mission_obj = input("Mission Objective: ")
    codename = input("Codename: ")
    asyncio.run(EliteSwarm(codename).execute(mission_obj))
