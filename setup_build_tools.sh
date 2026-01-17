#!/bin/zsh
echo "🛡️ INITIALIZING OMNICOMMANDER BUILD CHAIN..."

# 1. Update and Install System Dependencies
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 2. Install Python Build Tools in your venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install buildozer cython==0.29.33 pyinstaller

# 3. Create the Deploy/Build directory structure
mkdir -p deploy/bin
mkdir -p deploy/dist

echo "✅ BUILD TOOLS INSTALLED."
echo "Note: The first time you build an APK, Buildozer will download 2GB+ of Android SDK/NDK."
