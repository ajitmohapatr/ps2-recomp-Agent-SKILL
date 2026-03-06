import subprocess
import sys
import threading
import time
import os
import signal

# Usage: python log_reaper.py <path_to_ps2xruntime.exe> <path_to_ISO_or_ELF> [timeout_seconds]
# Example: python log_reaper.py build/Debug/ps2xRuntime.exe "games/SW_EP3.iso" 15

# Keywords that indicate a fatal emulation state where we should stop immediately
CRASH_KEYWORDS = [
    "Unimplemented PS2 stub",
    "[Syscall TODO]",
    "Function not found",
    "Segfault",
    "panic:",
    "fatal error:"
]

def run_headless_test(exe_path, game_path, timeout_sec=15):
    print(f"[Log-Reaper] Starting {exe_path} with {game_path} (Timeout: {timeout_sec}s)")
    
    # We want to kill the whole process tree if needed, standard Popen on Windows 
    # needs specific creation flags to be terminated cleanly if it spawns children.
    creationflags = 0
    if os.name == 'nt':
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

    process = subprocess.Popen(
        [exe_path, game_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Merge stderr into stdout
        text=True,
        encoding='utf-8',
        errors='replace',
        creationflags=creationflags
    )

    def timeout_killer():
        time.sleep(timeout_sec)
        if process.poll() is None:
            print(f"\n[Log-Reaper] TIMEOUT ({timeout_sec}s) reached. Killing process...")
            if os.name == 'nt':
                os.kill(process.pid, signal.CTRL_BREAK_EVENT)
            process.kill()

    timer_thread = threading.Thread(target=timeout_killer, daemon=True)
    timer_thread.start()

    print("[Log-Reaper] --- Output Start ---")
    
    crash_detected = False
    
    try:
        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            if not line:
                continue
                
            print(line)
            
            # Check for crash keywords
            for kw in CRASH_KEYWORDS:
                if kw in line:
                    print(f"\n[Log-Reaper] 💥 FATAL KEYWORD DETECTED: '{kw}'. Aborting early!")
                    crash_detected = True
                    break
            
            if crash_detected:
                try:
                    if os.name == 'nt':
                        os.kill(process.pid, signal.CTRL_BREAK_EVENT)
                        time.sleep(0.5) # Give process time to handle the break event
                    process.kill()
                except OSError:
                    pass # Process already exited
                break
                
    except Exception as e:
        print(f"\n[Log-Reaper] Exception while reading output: {e}")

    process.wait()
    print("[Log-Reaper] --- Output End ---")
    
    # Standard exit code on Windows for killed console apps is usually 0xC000013A (-1073741510) or similar,
    # or just standard negative signals on Unix.
    # If the app exited on its own with a non-zero code before timeout, it's a silent crash.
    silent_crash = False
    if process.returncode != 0 and process.returncode is not None:
        # Ignore the exit code if we forcefully killed it ourselves after a known crash or timeout
        if not crash_detected and timer_thread.is_alive():
            print(f"[Log-Reaper] 💥 SILENT CRASH: Process exited prematurely with code {process.returncode}")
            silent_crash = True

    if crash_detected or silent_crash:
        print("[Log-Reaper] Test ended early due to crash.")
        sys.exit(1)
    else:
        print("[Log-Reaper] Test completed (survived until timeout or exited gracefully).")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python log_reaper.py <exe_path> <game_path> [timeout]")
        sys.exit(1)
        
    exe = sys.argv[1]
    rom = sys.argv[2]
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    
    run_headless_test(exe, rom, duration)
