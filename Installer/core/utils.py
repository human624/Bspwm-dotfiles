import os
import sys
import subprocess

# ── Colors ─────────────────────
RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
GRAY = "\033[90m"

# ── Utilities ───────────────────
def clear():
    os.system("clear")

def pause():
    input(f"\n{GRAY}Press Enter...{RESET}")

def require_root():
    if os.geteuid() != 0:
        print(f"{MAGENTA} Root privileges required, requesting sudo...{RESET}")
        
        # Проверка доступа с sudo
        process = subprocess.run(['sudo', 'echo', ''], capture_output=True)
        if process.returncode != 0:
            log_err("Failed to authenticate with sudo. Exiting.")
            sys.exit(1)  # Завершаем программу, если не удалось получить права
        else:
            print(f"{GREEN}Root privileges granted.{RESET}")

def run(cmd, cwd=None):
    # Проверка на необходимость использования sudo
    if "sudo" not in cmd and os.geteuid() != 0:
        cmd = f"sudo {cmd}"
    
    subprocess.run(cmd, shell=True, cwd=cwd)

# ── Logging ─────────────────────
def log_file(p): print(f"{GREEN}[FILE]{RESET} {p}")
def log_dir(p):  print(f"{BLUE}[DIR ]{RESET} {p}")
def log_skip(p): print(f"{YELLOW}[SKIP]{RESET} {p}")
def log_root(p): print(f"{MAGENTA}[ROOT]{RESET} {p}")
def log_err(p):  print(f"{RED}[ERR ]{RESET} {p}")
