import subprocess, os, time

class P4AWorker:
    def __init__(self):
        self.venv_python = "/home/unknown/omnicommander_elite/venv/bin/python"
        self.project_dir = "/home/unknown/omnicommander_elite/deploy"
        
    def log(self, msg):
        print(f"[{time.strftime('%H:%M:%S')}] {msg}")

    def run_direct_build(self):
        self.log("Starting RAW python-for-android build...")
        
        # We define the command explicitly to avoid Buildozer's loop
        cmd = [
            self.venv_python, "-m", "pythonforandroid.toolchain", "apk",
            "--sdk-dir", "/home/unknown/.buildozer/android/platform/android-sdk",
            "--ndk-dir", "/home/unknown/.buildozer/android/platform/android-ndk-r25b",
            "--dist_name", "omnicommander",
            "--requirements", "python3,kivy==2.0.0rc2,pyjnius",
            "--arch", "arm64-v8a",
            "--bootstrap", "sdl2",
            "--package", "org.test.omnicommander",
            "--name", "OmniCommander",
            "--version", "1.0",
            "--private", self.project_dir,
            "--color=always",
            "--storage-dir=./.p4a_storage"
        ]
        
        return subprocess.run(cmd)

    def run(self):
        while True:
            # Step 1: Force the Cython fix
            subprocess.run(["pip", "install", "Cython==0.29.33"])
            
            # Step 2: Attempt the build
            result = self.run_direct_build()
            
            if result.returncode == 0:
                self.log("✅ SUCCESS! APK generated.")
                break
            
            self.log("❌ Build failed. Purging storage and retrying in 30s...")
            subprocess.run(["rm", "-rf", "./.p4a_storage"])
            time.sleep(30)

if __name__ == "__main__":
    P4AWorker().run()
