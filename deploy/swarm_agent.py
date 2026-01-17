import subprocess, os, time

class RelentlessFixer:
    def __init__(self):
        self.spec = "buildozer.spec"

    def log(self, msg):
        print(f"[{time.strftime('%H:%M:%S')}] {msg}")

    def enforce_versions(self):
        self.log("!!! ENFORCING VERSION DOWNGRADES !!!")
        # 1. Force Cython 0.29.33
        subprocess.run("pip install Cython==0.29.33", shell=True)
        # 2. Force Kivy rc2 in the spec file
        if os.path.exists(self.spec):
            with open(self.spec, 'r') as f:
                content = f.read()
            # Ensure it's not using rc4
            content = content.replace("kivy==2.0.0rc4", "kivy==2.0.0rc2")
            # If it just says 'kivy', pin it to rc2
            if "requirements = python3,kivy\n" in content:
                content = content.replace("requirements = python3,kivy", "requirements = python3,kivy==2.0.0rc2")
            with open(self.spec, 'w') as f:
                f.write(content)

    def deep_clean(self):
        self.log("Purging all caches to prevent loop...")
        subprocess.run("rm -rf .buildozer/", shell=True)
        subprocess.run("rm -rf ~/.buildozer/", shell=True)

    def run(self):
        while True:
            self.enforce_versions()
            self.log("Starting build... this will take a long time (30-60 mins).")
            
            # Run build and stream to terminal so you can see if it's actually stuck
            p = subprocess.run(["/home/unknown/omnicommander_elite/venv/bin/buildozer", "-v", "android", "debug"])

            if p.returncode == 0:
                self.log("✅ SUCCESS! CHECK bin/ FOLDER.")
                break
            
            self.log("❌ Build Failed. Cleaning and retrying...")
            self.deep_clean()
            time.sleep(10)

if __name__ == "__main__":
    RelentlessFixer().run()
