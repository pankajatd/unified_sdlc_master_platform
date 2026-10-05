"""
Automated Pytest runner and traceback extraction tool for Medical Image Analysis SDLC
"""
import re
import os
import sys
from typing import Dict, Any, List
from .shell_tools import execute_shell_command

def parse_pytest_output(stdout: str, stderr: str) -> Dict[str, Any]:
    passed = 0
    failed = 0
    errors = 0
    
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
        passed = len(re.findall(r"PASSED", stdout))
        failed = len(re.findall(r"FAILED", stdout))
        errors = len(re.findall(r"ERROR", stdout))

    total = passed + failed + errors

    failures = []
    failure_sections = re.findall(
        r"_{3,}\s*(.*?)\s*_{3,}(.*?)(?=\n_{3,}|\n={3,} short test summary|\Z)",
        stdout,
        re.DOTALL
    )
    
    for test_name, trace in failure_sections:
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
    if python_exe is None:
        python_exe = sys.executable

    cmd = f'"{python_exe}" -m pytest -v --tb=short'
    
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
