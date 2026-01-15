import subprocess
import os
import json
import psutil
from pathlib import Path

# --- CONFIG ---
PROJECT_DIR = Path("~/omnicommander_project").expanduser()
GEN_TOOL = PROJECT_DIR / "omni_tool.py"
SECRETS_FILE = PROJECT_DIR / "secrets_vault.json"
PROJECT_MEM_FILE = PROJECT_DIR / "project_memory.json"

def report(name, status, details=""):
    icon = "✅ PASS" if status else "❌ FAIL"
    print(f"[{icon}] {name.ljust(25)} | {details}")

def run_diagnostic():
    print("🛰️  STARTING OMNICOMMANDER SYSTEM AUDIT\n" + "="*50)

    # 1. Test Hardware Sensors
    try:
        ram = psutil.virtual_memory().percent
        report("Hardware: RAM", True, f"Usage at {ram}%")
    except Exception as e:
        report("Hardware: RAM", False, str(e))

    try:
        ssd_path = '/run/media/unknown/SSD/'
        if os.path.exists(ssd_path):
            ssd = psutil.disk_usage(ssd_path).percent
            report("Hardware: SSD", True, f"SSD Space at {ssd}%")
        else:
            report("Hardware: SSD", False, "Path not found")
    except Exception as e:
        report("Hardware: SSD", False, str(e))

    # 2. Test Local LLM (Ollama)
    try:
        res = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if res.returncode == 0:
            report("Process: Ollama", True, "Service is running")
        else:
            report("Process: Ollama", False, "Service unreachable")
    except:
        report("Process: Ollama", False, "Ollama not installed")

    # 3. Test GitHub CLI
    try:
        res = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
        if "Logged in" in res.stdout or "Logged in" in res.stderr:
            report("Module: GitHub CLI", True, "Authenticated")
        else:
            report("Module: GitHub CLI", False, "Not logged in")
    except:
        report("Module: GitHub CLI", False, "GH CLI not found")

    # 4. Test Memory & Secrets Vault
    if SECRETS_FILE.exists():
        report("Vault: Secrets", True, "Vault file exists")
    else:
        report("Vault: Secrets", False, "Vault file missing")

    if PROJECT_MEM_FILE.exists():
        report("Memory: Project", True, "Memory file exists")
    else:
        report("Memory: Project", False, "Memory file missing")

    # 5. Test Python Core Engine (omni_final.py)
    if (PROJECT_DIR / "omni_final.py").exists():
        report("Core: Engine", True, "omni_final.py located")
    else:
        report("Core: Engine", False, "Engine script missing")

    print("="*50 + "\nAUDIT COMPLETE")

if __name__ == "__main__":
    run_diagnostic()
