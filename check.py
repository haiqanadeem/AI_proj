import os
import time

frontend_dir = r"c:\Users\MuBeeN\Desktop\haiqa\frontend"
now = time.time()

# 24 hours in seconds
time_limit = 24 * 60 * 60

print(f"Checking for files modified in the last 24 hours in {frontend_dir}...")

count = 0
for root, dirs, files in os.walk(frontend_dir):
    if ".next" in root or "node_modules" in root or ".git" in root:
        continue

    for file in files:
        filepath = os.path.join(root, file)
        try:
            mtime = os.path.getmtime(filepath)
            elapsed = now - mtime

            if elapsed < time_limit:
                print(f"Modified {elapsed/3600:.2f} hours ago: {filepath}")
                count += 1
        except Exception:
            pass

print(f"Done. Found {count} modified files.")