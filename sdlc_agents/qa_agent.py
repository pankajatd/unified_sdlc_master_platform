"""
QA Test Engineer and Pytest Runner Agent Node
"""

from typing import Dict, Any
from sdlc_core.state import SDLCState, add_log_entry
from tools.test_runner_tools import run_pytest_suite

def qa_agent_node(state: SDLCState) -> Dict[str, Any]:
    """
    QA Test Engineer Agent:
    Executes automated unit tests via Pytest and evaluates pass/fail status.
    """
    target_dir = state.get("target_directory", "")
    
    # Run test suite
    test_report = run_pytest_suite(target_dir)
    
    all_passed = test_report["all_passed"]
    state["test_results"] = test_report
    state["test_passed"] = all_passed
    state["current_agent"] = "QA Test Engineer"
    
    if all_passed:
        state["status"] = "COMPLETED"
        msg = f"QA PASSED: 100% of unit tests passed ({test_report['passed_count']}/{test_report['total_count']}) in {test_report['duration_sec']}s."
        log_status = "SUCCESS"
    else:
        state["status"] = "HEALING"
        msg = f"QA FAILED: {test_report['failed_count']} failed, {test_report['passed_count']} passed out of {test_report['total_count']} tests."
        log_status = "ERROR"
        
    add_log_entry(
        state,
        agent_name="QA Test Engineer",
        message=msg,
        status=log_status
    )
    
    return {
        "test_results": test_report,
        "test_passed": all_passed,
        "current_agent": "QA Test Engineer",
        "status": state["status"],
        "execution_log": state["execution_log"]
    }
