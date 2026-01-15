import asyncio, aiohttp, os, subprocess, json, base64, hashlib, random, string
from datetime import datetime
from pathlib import Path

# --- CONFIG ---
GITHUB_USER = "jasonclarkagain"
OLLAMA_URL = "http://localhost:11434/api/generate"
ROOT = Path("~/omnicommander_elite").expanduser()
MEMORY_DIR = ROOT / "memory"

# --- ELITE MODULES ---
def get_daily_key():
    return hashlib.sha256(datetime.now().strftime("%Y-%m-%d").encode()).hexdigest()[:16]

def obfuscate(code):
    key = get_daily_key()
    xor_bytes = bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(code)])
    b64 = base64.b64encode(xor_bytes).decode()
    return f"import base64,hashlib,datetime;k=hashlib.sha256(datetime.datetime.now().strftime('%Y-%m-%d').encode()).hexdigest()[:16];d=base64.b64decode('{b64}');exec(''.join([chr(b^ord(k[i%len(k)])) for i,b in enumerate(d)]))"

class EliteSwarm:
    def __init__(self, mission_name):
        self.name = mission_name
        self.path = ROOT / mission_name
        self.path.mkdir(parents=True, exist_ok=True)

    async def ask_llm(self, role, prompt):
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "wizardlm2:7b", # Or any of your 20+ local models
                "system": f"You are the {role}. Return ONLY code or JSON as requested.",
                "prompt": prompt, "stream": False
            }
            async with session.post(OLLAMA_URL, json=payload) as resp:
                data = await resp.json()
                return data.get('response', "").strip()

    async def execute(self, objective):
        # 1. Architect Phase
        blueprint_raw = await self.ask_llm("Architect", f"Create a JSON list of files needed for: {objective}")
        files = ["main.py", "README.md"] # Fallback if LLM halluconates JSON
        
        # 2. Development & Red Team Audit
        for f in files:
            print(f"[*] Engineering {f}...")
            code = await self.ask_llm("Developer", f"Write the code for {f} based on {objective}")
            
            # Obfuscate the core tool only
            if f.endswith(".py"):
                code = obfuscate(code)
            
            (self.path / f).write_text(code)

        # 3. Learning & Metadata
        learnings = {"mission": self.name, "date": str(datetime.now()), "status": "Tactical-Success"}
        (self.path / "LEARNINGS.md").write_text(json.dumps(learnings))

        # 4. Elite Deployment
        os.chdir(self.path)
        subprocess.run(["git", "init"], capture_output=True)
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", "Mission Elite: Initial Push"], capture_output=True)
        repo_name = f"ELITE-{self.name}-{os.urandom(2).hex()}"
        subprocess.run(["gh", "repo", "create", repo_name, "--public", "--source=.", "--push"], capture_output=True)
        return repo_url := f"https://github.com/{GITHUB_USER}/{repo_name}"

if __name__ == "__main__":
    mission = input("Enter Mission Objective: ")
    name = input("Enter Project Codename: ")
    asyncio.run(EliteSwarm(name).execute(mission))
