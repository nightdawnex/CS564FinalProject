import subprocess
import os
import sys
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def main():
    exe = resource_path("bin/rclone.exe")
    conf = resource_path("bin/rclone.conf")
    cmd = [exe, "--config", conf, "lsd","cloud:"]
    
    print(cmd)

    p = subprocess.Popen(" ".join(cmd),stdout=sys.stdout, stderr=sys.stderr, shell=True)
    
    p.wait()

if __name__ == "__main__":
    main()
