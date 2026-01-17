#!/bin/bash
# 1. Temporary "Hide" host headers to prevent leakage
echo "[*] Temporarily isolating host headers..."
sudo mv /usr/include/x86_64-linux-gnu /usr/include/x86_64-linux-gnu.bak

# 2. Setup Environment
export JAVA_HOME="$HOME/.sdkman/candidates/java/current"
export PATH="$JAVA_HOME/bin:$PATH"
source ~/omnicommander_elite/venv/bin/activate

# 3. Run Buildozer
echo "[*] Starting Buildozer build..."
buildozer -v android debug

# 4. Restore headers no matter what happens
echo "[*] Restoring host headers..."
sudo mv /usr/include/x86_64-linux-gnu.bak /usr/include/x86_64-linux-gnu
