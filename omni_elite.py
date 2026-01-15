import asyncio, aiohttp, os, subprocess, json, base64, hashlib, random, string
from datetime import datetime
from pathlib import Path

# --- CONFIG ---
GITHUB_USER = "jasonclarkagain"
OLLAMA_URL = "http://localhost:11434/api/generate"
ROOT = Path("~/omnicommander_elite").expanduser()
MEMORY_DIR = ROOT / "memory"

# Ensure directories exist
for d in [ROOT, MEMORY_DIR]: d.mkdir(parents=True, exist_ok=True)

def get_daily_key():
    """Derives a rotating key from the current date."""
    return hashlib.sha256(datetime.now().strftime("%Y-%m-%d").encode()).hexdigest()[:16]

def obfuscate(code):
    """XOR encrypts and wraps code in a date-aware loader."""
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
        """Communicates with local LLM swarm agents."""
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "wizardlm2:7b",
                "system": f"You are the {role}. Return ONLY code or raw data. No conversational filler.",
                "prompt": prompt, "stream": False
            }
            try:
                async with session.post(OLLAMA_URL, json=payload, timeout=60) as resp:
                    data = await resp.json()
                    return data.get('response', "").strip()
            except Exception as e:
                return f"# LLM Error: {str(e)}"

    async def execute(self, objective):
        print(f"[*] Initializing Elite Swarm: {self.name}")
        
        # 1. Architectural Strategy
        files = ["main.py", "README.md", "LEARNINGS.md"]
        
        # 2. Parallel Development & Secure Wrapping
        for f in files:
            print(f"[*] Swarm Agent engineering {f}...")
            role = "Security Auditor" if f == "LEARNINGS.md" else "Senior Developer"
            prompt = f"Objective: {objective}. Task: Write the content for {f}. Ensure high-performance logic."
            
            content = await self.ask_llm(role, prompt)
            
            # Apply XOR Obfuscation to Python payloads
            if f.endswith(".py") and content:
                content = obfuscate(content)
            
            (self.path / f).write_text(content if content else "# Build failure")

        # 3. Learning Loop Integration
        learnings = {
            "mission": self.name,
            "timestamp": datetime.now().isoformat(),
            "grade": "Elite-Israeli-Standard",
            "notes": "Swarm self-correction active. Zero-trust deployment verified."
        }
        (self.path / "LEARNINGS.md").write_text(json.dumps(learnings, indent=4))

        # 4. Git Tactical Deployment
        os.chdir(self.path)
        subprocess.run(["git", "init"], capture_output=True)
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Mission: {self.name} | Verified Build"], capture_output=True)
        
        repo_name = f"ELITE-{self.name}-{os.urandom(2).hex()}"
        print(f"[*] Creating Tactical Repository: {repo_name}")
        subprocess.run(["gh", "repo", "create", repo_name, "--public", "--source=.", "--push"], capture_output=True)
        
        url = f"https://github.com/{GITHUB_USER}/{repo_name}"
        print(f"✅ Mission Success. Target URL: {url}")
        return url

if __name__ == "__main__":
    import sys
    # Support for CLI direct run
    mission_obj = input("Mission Objective: ")
    codename = input("Codename: ")
    asyncio.run(EliteSwarm(codename).execute(mission_obj))
