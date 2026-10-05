"""
Subprocess and shell execution tools for SDLC multi-agent operations
"""

import subprocess
import time
from typing import Dict, Any, Optional

def execute_shell_command(
    cmd: str,
    cwd: str,
    timeout: int = 45,
    env: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Executes a shell command safely inside a given directory.
    Returns returncode, stdout, stderr, and execution duration.
    """
    start_time = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            encoding="utf-8",
            errors="replace"
        )
        duration = round(time.time() - start_time, 3)
        return {
            "cmd": cmd,
            "cwd": cwd,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "duration_sec": duration,
            "timed_out": False,
            "status": "SUCCESS" if proc.returncode == 0 else "FAILED"
        }
    except subprocess.TimeoutExpired as e:
        duration = round(time.time() - start_time, 3)
        return {
            "cmd": cmd,
            "cwd": cwd,
            "returncode": -1,
            "stdout": e.stdout or "",
            "stderr": (e.stderr or "") + f"\nCommand timed out after {timeout} seconds",
            "duration_sec": duration,
            "timed_out": True,
            "status": "TIMEOUT"
        }
    except Exception as e:
        duration = round(time.time() - start_time, 3)
        return {
            "cmd": cmd,
            "cwd": cwd,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "duration_sec": duration,
            "timed_out": False,
            "status": "ERROR"
        }
