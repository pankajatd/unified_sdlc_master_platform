"""
Automated Pytest runner and traceback extraction tool for SDLC QA & Self-Healing
"""

import re
import os
from typing import Dict, Any, List
from .shell_tools import execute_shell_command
import sys

def parse_pytest_output(stdout: str, stderr: str) -> Dict[str, Any]:
    """
    Parses pytest stdout/stderr to extract:
    - passed, failed, errors, total counts
    - failure tracebacks & assertion summaries
    """
    passed = 0
    failed = 0
    errors = 0
    
    # Example summary line: "=== 4 passed, 1 failed in 0.12s ==="
    summary_match = re.search(r"===+\s*(.*?)\s*in\s+[\d\.]+s\s*===+", stdout)
    if summary_match:
        summary_text = summary_match.group(1)
        passed_m = re.search(r"(\d+)\s+passed", summary_text)
        failed_m = re.search(r"(\d+)\s+failed", summary_text)
        error_m = re.search(r"(\d+)\s+error", summary_text)
        
        if passed_m:
            passed = int(passed_m.group(1))
        if failed_m:
            failed = int(failed_m.group(1))
        if error_m:
            errors = int(error_m.group(1))
    else:
        # Fallback counting
        passed = len(re.findall(r"PASSED", stdout))
        failed = len(re.findall(r"FAILED", stdout))
        errors = len(re.findall(r"ERROR", stdout))

    total = passed + failed + errors

    # Extract failure blocks
    failures = []
    failure_sections = re.findall(
        r"_{3,}\s*(.*?)\s*_{3,}(.*?)(?=\n_{3,}|\n={3,} short test summary|\Z)",
        stdout,
        re.DOTALL
    )
    
    for test_name, trace in failure_sections:
        # Extract target file if possible
        file_match = re.search(r"(tests/[^\s:]+\.py):(\d+):", trace)
        failures.append({
            "test_name": test_name.strip(),
            "target_file": file_match.group(1) if file_match else "unknown",
            "line_no": int(file_match.group(2)) if file_match else None,
            "traceback": trace.strip()
        })
        
    return {
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "total": total,
        "all_passed": (total > 0 and failed == 0 and errors == 0),
        "failures": failures
    }


def run_pytest_suite(
    project_dir: str,
    python_exe: str = None,
    timeout: int = 60
) -> Dict[str, Any]:
    """
    Executes pytest inside the project directory and returns structured results.
    """
    if python_exe is None:
        try:
            from config import PYTHON_EXE
            python_exe = PYTHON_EXE
        except ImportError:
            python_exe = sys.executable

    cmd = f'"{python_exe}" -m pytest -v --tb=short'
    
    # Ensure current project directory is in PYTHONPATH so internal modules resolve
    env = os.environ.copy()
    current_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{project_dir};{current_pythonpath}"

    res = execute_shell_command(cmd, cwd=project_dir, timeout=timeout, env=env)
    parsed = parse_pytest_output(res["stdout"], res["stderr"])

    return {
        "status": "PASSED" if parsed["all_passed"] else "FAILED",
        "all_passed": parsed["all_passed"],
        "passed_count": parsed["passed"],
        "failed_count": parsed["failed"],
        "error_count": parsed["errors"],
        "total_count": parsed["total"],
        "failures": parsed["failures"],
        "raw_stdout": res["stdout"],
        "raw_stderr": res["stderr"],
        "duration_sec": res["duration_sec"],
        "timed_out": res["timed_out"]
    }
