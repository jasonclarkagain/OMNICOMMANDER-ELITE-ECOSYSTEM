import subprocess, os, time

def apply_middleware_patches():
    print("[*] Applying middleware patches...")
    # Fix 1: Ensure Cython is pinned in the current environment
    subprocess.run(["pip", "install", "Cython==0.29.33"])
    
    # Fix 2: Patch buildozer.spec for Ubuntu 22.04 compatibility
    if os.path.exists("buildozer.spec"):
        with open("buildozer.spec", "r") as f:
            lines = f.readlines()
        with open("buildozer.spec", "w") as f:
            for line in lines:
                # Force Kivy version to rc2 which is more stable on 22.04
                if line.startswith("requirements ="):
                    line = "requirements = python3,kivy==2.0.0rc2,pyjnius\n"
                # Ensure we are targeting a compatible NDK API
                if line.startswith("android.api ="):
                    line = "android.api = 31\n"
                f.write(line)

def relentless_build():
    while True:
        apply_middleware_patches()
        print("[+] Starting Buildozer...")
        
        # We run with -v to see progress, but we catch the fail
        proc = subprocess.run(["buildozer", "-v", "android", "debug"])
        
        if proc.returncode == 0:
            print("✅ BUILD SUCCESSFUL! You can wake up now.")
            break
        
        print("❌ Build failed. Cleaning 'hostpython3' cache and retrying...")
        # This is the 'Middleware' cleaning part - only kills the broken part
        subprocess.run("rm -rf .buildozer/android/platform/build-arm64-v8a/build/other_builds/hostpython3", shell=True)
        time.sleep(5)

if __name__ == "__main__":
    relentless_build()
