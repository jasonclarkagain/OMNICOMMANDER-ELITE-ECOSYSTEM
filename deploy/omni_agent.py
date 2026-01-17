import subprocess
import os
import time

class OmniBuildAgent:
    def __init__(self):
        self.attempts = {}
        self.max_retries_per_error = 2
        self.project_path = os.getcwd()

    def repair_strategy(self, error_type):
        count = self.attempts.get(error_type, 0)
        
        if count >= self.max_retries_per_error:
            print("\n[!] STRATEGY FAILED: Already tried repairing {} {} times.".format(error_type, count))
            print("[!] ESCALATING: Switching to Deep Clean mode...")
            subprocess.run(["buildozer", "android", "clean"])
            return False

        if error_type == "hostpython_fail":
            print("\n[+] REPAIRING: Wiping hostpython (Attempt {})".format(count + 1))
            target = ".buildozer/android/platform/build-arm64-v8a/build/other_builds/hostpython3"
            subprocess.run(["rm", "-rf", target])
            
        self.attempts[error_type] = count + 1
        return True

    def run(self):
        print("[-] Omni-Commander Autonomous Agent Engaged.")
        
        while True:
            # Setting environment variables within the agent's process
            env = os.environ.copy()
            env["CFLAGS"] = "-I/usr/include -I/usr/include/x86_64-linux-gnu"
            env["LDFLAGS"] = "-L/usr/lib/x86_64-linux-gnu"

            cmd = ["buildozer", "-v", "android", "debug"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
            
            error_detected = None
            for line in process.stdout:
                print(line, end='')
                
                if "hostpython3/native-build/python3 failed" in line:
                    error_detected = "hostpython_fail"
                    process.terminate()
                    break
            
            process.wait()
            
            if error_detected:
                if not self.repair_strategy(error_detected):
                    print("\n[!!!] FATAL: Agent cannot resolve this issue autonomously.")
                    break
                print("[-] Repair applied. Cooling down for 5s before restart...")
                time.sleep(5)
            elif process.returncode == 0:
                print("\n[OK] APK successfully built!")
                break
            else:
                print("\n[?] Unknown failure code: {}".format(process.returncode))
                break

if __name__ == "__main__":
    agent = OmniBuildAgent()
    agent.run()
