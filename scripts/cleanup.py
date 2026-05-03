import os
import time
import shutil
from pathlib import Path

# Configuration
STORAGE_DIR = "/tmp/fileconverter"
RETENTION_SECONDS = 10 * 60  # 10 minutes

def cleanup():
    print(f"Starting cleanup of {STORAGE_DIR}...")
    now = time.time()
    count = 0
    
    if not os.path.exists(STORAGE_DIR):
        print("Storage directory does not exist.")
        return

    for job_dir in Path(STORAGE_DIR).iterdir():
        if job_dir.is_dir():
            # Check modification time of the directory
            mtime = job_dir.stat().st_mtime
            if now - mtime > RETENTION_SECONDS:
                try:
                    shutil.rmtree(job_dir)
                    count += 1
                    print(f"Deleted expired job directory: {job_dir.name}")
                except Exception as e:
                    print(f"Error deleting {job_dir.name}: {e}")

    print(f"Cleanup finished. Deleted {count} directories.")

if __name__ == "__main__":
    cleanup()
