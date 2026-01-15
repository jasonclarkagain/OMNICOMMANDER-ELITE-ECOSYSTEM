#!/bin/bash
export DOCKER_HOST=unix:///var/run/docker.sock
cd ~/omnicommander_elite
source venv/bin/activate
streamlit run omni_dash.py
