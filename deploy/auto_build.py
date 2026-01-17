import subprocess
import time
import os

# Configuration for your specific environment
VENV_PYTHON = "/home/unknown/omnicommander_elite/venv/bin/python"
PROJECT_DIR = "/home/unknown/omnicommander_elite/deploy"

def log_message(msg):
    print(f"\n[AGENT] {msg}")

def run_build():
    os.chdir(PROJECT_DIR)
    # Maintain the environment variables we set
    env = os.environ.copy()
    env["CFLAGS"] = "-I/usr/include -I/usr/include/x86_64-linux-gnu"
    env["LDFLAGS"] = "-L/usr/lib/x86_64-linux-gnu"
    
    cmd = ["buildozer", "-v", "android", "debug"]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    
    last_lines = []
    for line in process.stdout:
        print(line, end='')
        last_lines.append(line)
        if len(last_lines) > 50: last_lines.pop(0)

        # TRIGGER: If we hit the specific HostPython error again
        if "hostpython3/native-build/python3 failed" in line:
            log_message("FAILURE DETECTED: HostPython crash. Initiating repair...")
            process.terminate()
            repair_hostpython()
            return False # Restart loop
            
    process.wait()
    if process.returncode == 0:
        log_message("SUCCESS: APK Generated!")
        return True
    return False

def repair_hostpython():
    log_message("Wiping broken build artifacts...")
    subprocess.run(["rm", "-rf", ".buildozer/android/platform/build-arm64-v8a/build/other_builds/hostpython3"])
    log_message("Clean complete. Restarting build...")

if __name__ == "__main__":
    log_message("Starting Autonomous Build Agent...")
    success = False
    while not success:
        success = run_build()
        if not success:
            log_message("Build failed/interrupted. Retrying in 5 seconds...")
            time.sleep(5)
