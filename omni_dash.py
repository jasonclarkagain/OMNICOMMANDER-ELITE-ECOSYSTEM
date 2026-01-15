import streamlit as st
import subprocess
import psutil
import os
import pandas as pd
import base64
import time
import json
import requests
from pathlib import Path

# --- CONFIG ---
PROJECT_DIR = Path("~/omnicommander_project").expanduser()
KB_DIR = Path("~/.omnicommander/knowledge_base").expanduser()
HISTORY_FILE = PROJECT_DIR / "build_history.csv"
INDEX_FILE = PROJECT_DIR / "indexed_folders.txt"
SECRETS_FILE = PROJECT_DIR / "secrets_vault.json"
PROJECT_MEM_FILE = PROJECT_DIR / "project_memory.json"
GEN_TOOL = PROJECT_DIR / "omni_tool.py"

for d in [PROJECT_DIR, KB_DIR]: d.mkdir(parents=True, exist_ok=True)

# --- UTILS & DATA PERSISTENCE ---
def load_json(path):
    if path.exists():
        with open(path, 'r') as f: return json.load(f)
    return {}

def save_json(path, data):
    with open(path, 'w') as f: json.dump(data, f, indent=4)

def notify_discord(message):
    secrets = load_json(SECRETS_FILE)
    webhook_url = secrets.get('DISCORD_WEBHOOK')
    if webhook_url:
        payload = {"content": f"🛡️ **OMNICOMMANDER STATUS**\n{message}"}
        try: requests.post(webhook_url, json=payload, timeout=5)
        except: pass

def get_hw_stats():
    stats = {}
    try:
        t = psutil.sensors_temperatures()
        if 'coretemp' in t: stats['temp'] = f"{t['coretemp'][0].current}°C"
        elif 'cpu_thermal' in t: stats['temp'] = f"{t['cpu_thermal'][0].current}°C"
        else: stats['temp'] = "N/A"
    except: stats['temp'] = "Locked"
    stats['ram'] = psutil.virtual_memory().percent
    try:
        ssd = psutil.disk_usage('/run/media/unknown/SSD/')
        stats['ssd'] = ssd.percent
    except: stats['ssd'] = "ERR"
    net_1 = psutil.net_io_counters()
    time.sleep(0.1)
    net_2 = psutil.net_io_counters()
    stats['download'] = round((net_2.bytes_recv - net_1.bytes_recv) / 1024, 2)
    stats['upload'] = round((net_2.bytes_sent - net_1.bytes_sent) / 1024, 2)
    return stats

# --- UI SETUP ---
st.set_page_config(page_title="OMNICOMMANDER IDAE", page_icon="🛡️", layout="wide")

# --- SIDEBAR (Hardware & Starlink) ---
with st.sidebar:
    st.title("🛡️ SWARM SYSTEM")
    hw = get_hw_stats()
    st.subheader("📟 Hardware Vitals")
    c1, c2 = st.columns(2)
    c1.metric("CPU Temp", hw['temp'])
    c2.metric("System RAM", f"{hw['ram']}%")
    st.metric("SSD Space", f"{hw['ssd']}%")
    
    st.subheader("📡 Starlink Traffic")
    n1, n2 = st.columns(2)
    n1.metric("Down", f"{hw['download']} KB/s")
    n2.metric("Up", f"{hw['upload']} KB/s")
    
    st.divider()
    try:
        m_raw = subprocess.check_output(["ollama", "list"], text=True).split('\n')[1:]
        models = [line.split()[0] for line in m_raw if line.strip()]
    except: models = ["wizardlm2:7b"]
    model_a = st.selectbox("Primary Model:", models)
    model_b = st.selectbox("Battle Opponent:", ["None"] + models)

    if st.button("🗑️ PURGE VRAM", width="stretch"):
        subprocess.run(["pkill", "-f", "ollama serve"])
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL)
        st.toast("System Reset...")

# --- MAIN PAGE ---
st.title("🛰️ OMNICOMMANDER COMMAND CENTER")
st.markdown("---")

# SECTION 1: PROJECT LIBRARY & SECRETS
col_mem, col_sec = st.columns(2)
with col_mem:
    st.header("📚 Project Library")
    proj_mem = load_json(PROJECT_MEM_FILE)
    
    # Load Existing Projects
    project_list = list(proj_mem.keys()) if proj_mem else ["Default"]
    selected_proj = st.selectbox("Load Project Template:", project_list)
    
    # Project Details
    proj_name = st.text_input("Project / Branch Name:", value=selected_proj)
    proj_notes = st.text_area("Memory & Constraints:", value=proj_mem.get(selected_proj, ""), height=150)
    
    if st.button("💾 Save to Library", width="stretch"):
        proj_mem[proj_name] = proj_notes
        save_json(PROJECT_MEM_FILE, proj_mem)
        st.success(f"Project '{proj_name}' saved and ready.")

with col_sec:
    st.header("🔐 Secrets Vault")
    secrets = load_json(SECRETS_FILE)
    sec_key = st.text_input("Label (e.g. DISCORD_WEBHOOK):")
    sec_val = st.text_input("Key/Value:", type="password")
    if st.button("🔑 Store Secret", width="stretch"):
        secrets[sec_key] = sec_val
        save_json(SECRETS_FILE, secrets)
        st.success("Locked.")
    if st.checkbox("Show Keys List"):
        st.write(list(secrets.keys()))

st.divider()

# SECTION 2: ORCHESTRATOR
st.header("🚀 Swarm Orchestrator")
task = st.text_area("Objective:")
if st.button("🚀 EXECUTE SWARM", width="stretch"):
    full_task = f"PROJECT: {proj_name}\nCONSTRAINTS: {proj_notes}\nTASK: {task}"
    with st.status(f"Deploying {proj_name} Swarm...") as s:
        # Pass branch name to the final script
        cmd = ["python3", "omni_final.py", full_task, "--model", model_a, "--branch", proj_name]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        logs = ""
        log_area = st.empty()
        for line in iter(p.stdout.readline, ""):
            logs += line
            log_area.code(logs)
        p.wait()
    
    if "SUCCESS:" in logs:
        git_url = logs.split("SUCCESS:")[1].strip()
        notify_discord(f"✅ **Build Success**\n**Project:** {proj_name}\n**Branch:** {proj_name}\n**Repo:** {git_url}")
    st.rerun()

st.divider()

# SECTION 3: ENCODER & TERMINAL
c_enc, c_term = st.columns(2)
with c_enc:
    st.header("🔐 Payload Encoder")
    if GEN_TOOL.exists() and st.button("🛡️ Encode Tool", width="stretch"):
        encoded = base64.b64encode(GEN_TOOL.read_text().encode()).decode()
        st.code(f"import base64;exec(base64.b64decode('{encoded}'))")

with c_term:
    st.header("💻 Rapid Terminal")
    cmd_in = st.text_input("Run Command:", value=f"python3 {GEN_TOOL}")
    if st.button("📟 RUN", width="stretch"):
        res = subprocess.run(cmd_in, shell=True, capture_output=True, text=True)
        st.code(res.stdout + res.stderr)

st.divider()

# SECTION 4: DIAGNOSTICS & HISTORY
c_hi, c_dg = st.columns(2)
with c_hi:
    st.header("📜 Build History")
    if HISTORY_FILE.exists():
        st.dataframe(pd.read_csv(HISTORY_FILE)[::-1], hide_index=True, width="stretch")

with c_dg:
    st.header("🩺 System Audit")
    if st.button("🔍 Run Full Audit", width="stretch"):
        audit = subprocess.run(["python3", "omni_test.py"], capture_output=True, text=True)
        st.code(audit.stdout)
        if "❌ FAIL" in audit.stdout:
            notify_discord(f"⚠️ **DIAGNOSTIC FAILURE** on OMNICOMMANDER workstation!")
