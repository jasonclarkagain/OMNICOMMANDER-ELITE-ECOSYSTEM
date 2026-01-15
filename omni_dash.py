import streamlit as st
import subprocess
import psutil
import os
import asyncio
from pathlib import Path
from omni_elite import EliteSwarm

st.set_page_config(page_title="ELITE COMMAND CENTER", page_icon="🛰️", layout="wide")

ROOT = Path("~/omnicommander_elite").expanduser()

# --- SIDEBAR: VITALS ---
with st.sidebar:
    st.title("🛡️ SYSTEM VITALS")
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    st.metric("CPU Load", f"{cpu}%")
    st.metric("RAM Usage", f"{ram}%")
    
    st.divider()
    if st.button("🗑️ PURGE VRAM & RESET", use_container_width=True):
        subprocess.run(["sudo", "pkill", "-f", "ollama serve"])
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL)
        st.success("Ollama Service Restarted")

# --- MAIN COMMAND INTERFACE ---
st.title("🛰️ OMNICOMMANDER: ELITE ECOSYSTEM")
st.subheader("Tactical Swarm Orchestration")

col1, col2 = st.columns(2)
with col1:
    mission = st.text_area("Mission Objective:", placeholder="e.g., Build a stealthy file-transfer tool...")
with col2:
    codename = st.text_input("Project Codename:", placeholder="e.g., Iron-Dome-V2")

if st.button("🚀 INITIATE ELITE SWARM", use_container_width=True):
    if mission and codename:
        with st.status("Swarm Deploying...") as s:
            st.write("[*] Activating Architect & Dev Agents...")
            # Run the elite engine logic
            swarm = EliteSwarm(codename)
            repo_url = asyncio.run(swarm.execute(mission))
            
            st.write(f"[✅] Repository Created: {repo_url}")
            st.success("Mission Complete. Check Discord and GitHub.")
            st.balloons()
    else:
        st.error("Missing Mission Parameters.")

st.divider()
st.info("System Note: Every build is XOR-encoded with 24h rotating keys and logged to LEARNINGS.md")import streamlit as st
import subprocess
import psutil
import os
import asyncio
from pathlib import Path
from omni_elite import EliteSwarm

st.set_page_config(page_title="ELITE COMMAND CENTER", page_icon="🛰️", layout="wide")

ROOT = Path("~/omnicommander_elite").expanduser()

# --- SIDEBAR: VITALS ---
with st.sidebar:
    st.title("🛡️ SYSTEM VITALS")
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    st.metric("CPU Load", f"{cpu}%")
    st.metric("RAM Usage", f"{ram}%")
    
    st.divider()
    if st.button("🗑️ PURGE VRAM & RESET", use_container_width=True):
        subprocess.run(["sudo", "pkill", "-f", "ollama serve"])
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL)
        st.success("Ollama Service Restarted")

# --- MAIN COMMAND INTERFACE ---
st.title("🛰️ OMNICOMMANDER: ELITE ECOSYSTEM")
st.subheader("Tactical Swarm Orchestration")

col1, col2 = st.columns(2)
with col1:
    mission = st.text_area("Mission Objective:", placeholder="e.g., Build a stealthy file-transfer tool...")
with col2:
    codename = st.text_input("Project Codename:", placeholder="e.g., Iron-Dome-V2")

if st.button("🚀 INITIATE ELITE SWARM", use_container_width=True):
    if mission and codename:
        with st.status("Swarm Deploying...") as s:
            st.write("[*] Activating Architect & Dev Agents...")
            # Run the elite engine logic
            swarm = EliteSwarm(codename)
            repo_url = asyncio.run(swarm.execute(mission))
            
            st.write(f"[✅] Repository Created: {repo_url}")
            st.success("Mission Complete. Check Discord and GitHub.")
            st.balloons()
    else:
        st.error("Missing Mission Parameters.")

st.divider()
st.info("System Note: Every build is XOR-encoded with 24h rotating keys and logged to LEARNINGS.md")
