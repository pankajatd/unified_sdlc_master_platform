"""
Shell execution tool for Medical Image Analysis SDLC
"""
import subprocess
import time
from typing import Dict, Any, Optional

def execute_shell_command(
    command: str,
    cwd: Optional[str] = None,
    timeout: int = 60,
    env: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    t0 = time.time()
    try:
        proc = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )
        duration = round(time.time() - t0, 3)
        return {
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "exit_code": proc.returncode,
            "duration_sec": duration,
            "timed_out": False
        }
    except subprocess.TimeoutExpired:
        duration = round(time.time() - t0, 3)
        return {
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds.",
            "exit_code": -1,
            "duration_sec": duration,
            "timed_out": True
        }
    except Exception as e:
        duration = round(time.time() - t0, 3)
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "duration_sec": duration,
            "timed_out": False
        }
