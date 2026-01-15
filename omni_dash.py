import streamlit as st
import subprocess
import psutil
import asyncio
from pathlib import Path
from omni_elite import EliteSwarm

st.set_page_config(page_title="ELITE COMMAND", layout="wide")
ROOT = Path("~/omnicommander_elite").expanduser()

with st.sidebar:
    st.title("📟 STATUS")
    st.metric("VRAM Available", f"{psutil.virtual_memory().available / (1024**3):.2f} GB")
    if st.button("RESET SERVICES"):
        subprocess.run(["sudo", "pkill", "-f", "ollama serve"])
        subprocess.Popen(["ollama", "serve"])

st.title("🛰️ OMNICOMMANDER: ELITE ECOSYSTEM")

c1, c2 = st.columns(2)
with c1:
    mission = st.text_input("Mission Objective:")
with c2:
    codename = st.text_input("Codename:")

if st.button("🚀 DEPLOY SWARM"):
    if mission and codename:
        swarm = EliteSwarm(codename)
        repo_url = asyncio.run(swarm.execute(mission))
        st.success(f"Mission Complete: {repo_url}")
    else:
        st.warning("Input required.")
