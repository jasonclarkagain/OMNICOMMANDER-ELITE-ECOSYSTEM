#!/bin/bash

# 1. Force Docker Socket
export DOCKER_HOST=unix:///var/run/docker.sock

# 2. Enter ELITE Directory and Activate Environment
cd ~/omnicommander_elite
if [ -d "venv" ]; then
    source venv/bin/activate
else
    python3 -m venv venv
    source venv/bin/activate
    pip install streamlit psutil pandas requests aiohttp beautifulsoup4
fi

# 3. Clear VRAM
echo "[*] Purging VRAM..."
sudo pkill -f "ollama serve"
nohup ollama serve > /dev/null 2>&1 &
sleep 2

# 4. Launch ELITE Dashboard
echo "[🚀] Starting ELITE COMMAND CENTER..."
streamlit run omni_dash.py
