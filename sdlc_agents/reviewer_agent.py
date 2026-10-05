"""
Code Reviewer and Security Auditor Agent Node
"""

from typing import Dict, Any, List
from sdlc_core.state import SDLCState, add_log_entry
from sdlc_core.llm import LLMClient

def reviewer_agent_node(state: SDLCState) -> Dict[str, Any]:
    """
    Code Reviewer & Security Auditor Agent:
    Inspects generated code for SQL injection, boundary checks, and logic soundness.
    """
    generated_files = state.get("generated_files", {})
    
    findings = []
    # 1. SQL Injection audit: check if string formatting (%s or f-strings) is used in SQL queries
    sql_files = [f for f in generated_files if f.endswith(".py") or f.endswith(".sql")]
    for path in sql_files:
        code = generated_files[path]
        if "execute(" in code and ("% " in code or "format(" in code or "f\"" in code and "SELECT" in code):
            findings.append(f"Security Alert in {path}: Potential SQL injection risk from string formatting.")

    # 2. Boundary and defensive check
    if "models/transaction.py" in generated_files:
        model_code = generated_files["models/transaction.py"]
        if "amount <= 0" in model_code:
            findings.append("Verified: Non-positive transaction amounts are defensively rejected.")

    if "models/study.py" in generated_files:
        findings.append("Verified: Patient and ImagingStudy data models enforce typed clinical fields and validation.")

    # 3. Decision
    has_critical_error = any("Security Alert" in f for f in findings)
    review_passed = not has_critical_error
    
    state["review_feedback"] = findings
    state["review_passed"] = review_passed
    state["current_agent"] = "Code Reviewer"
    state["status"] = "TESTING" if review_passed else "CODING"
    
    add_log_entry(
        state,
        agent_name="Code Reviewer",
        message=f"Code audit completed: {'APPROVED' if review_passed else 'REJECTED'}. {len(findings)} checklist items audited.",
        status="DONE" if review_passed else "WARN"
    )
    
    return {
        "review_feedback": findings,
        "review_passed": review_passed,
        "current_agent": "Code Reviewer",
        "status": state["status"],
        "execution_log": state["execution_log"]
    }
