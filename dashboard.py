import streamlit as st
import subprocess
import os
import requests
import datetime
from PIL import Image, ImageDraw

PROJECT_DIR = "/home/unknown/omnicommander_elite"
BUILD_DIR = os.path.join(PROJECT_DIR, "deploy")
OLLAMA_API = "http://localhost:11434/api/generate"

st.set_page_config(page_title="OMNICOMMANDER ELITE", layout="wide")
st.title("🛡️ OMNICOMMANDER ELITE: ICON & BUILD ENGINE")

# --- UI ---
with st.sidebar:
    st.header("🎯 Target")
    platform = st.selectbox("Platform", ["Android (APK)", "Windows (EXE)"])
    if st.button("Generate Default Icon"):
        img = Image.new('RGB', (512, 512), color = (14, 17, 23))
        draw = ImageDraw.Draw(img)
        draw.text((150, 230), "ELITE", fill=(255, 255, 255))
        img.save(os.path.join(BUILD_DIR, "icon.png"))
        st.success("Icon Saved!")

# --- BUILD LOGIC ---
directive = st.text_area("What app shall we build with an icon?")

if st.button("🚀 Build APK"):
    sys_msg = f"Generate ONLY the Python Kivy code for an Android app that: {directive}"
    payload = {"model": "wizardcoder-uncensored:latest", "prompt": sys_msg, "stream": False}
    
    with st.spinner("AI Architecting..."):
        res = requests.post(OLLAMA_API, json=payload).json()
        code = res.get("response", "")
        with open(os.path.join(BUILD_DIR, "main.py"), "w") as f:
            f.write(code)
    
    with st.spinner("Compiling APK... This will take 10+ mins first time."):
        # Run buildozer in the deploy folder
        subprocess.run([f"{PROJECT_DIR}/venv/bin/buildozer", "android", "debug"], cwd=BUILD_DIR)
        st.success("Build Finished! Check the Gallery below.")

# --- GALLERY ---
st.divider()
st.header("📦 Finished Apps")
for root, dirs, files in os.walk(BUILD_DIR):
    for file in files:
        if file.endswith('.apk'):
            st.download_button(f"⬇️ Download {file}", open(os.path.join(root, file), 'rb'), file_name=file)
