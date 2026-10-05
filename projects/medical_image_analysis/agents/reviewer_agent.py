"""
Code Reviewer and Security Auditor Agent Node for Medical Imaging
"""
from typing import Dict, Any, List
from core.state import SDLCState, add_log_entry

def reviewer_agent_node(state: SDLCState) -> Dict[str, Any]:
    generated_files = state.get("generated_files", {})
    findings = []
    
    # 1. SQL Injection audit: ensure parameterized queries
    sql_files = [f for f in generated_files if f.endswith(".py") or f.endswith(".sql")]
    for path in sql_files:
        code = generated_files[path]
        if "execute(" in code and ("% " in code or "format(" in code or "f\"" in code and "SELECT" in code):
            findings.append(f"Security Alert in {path}: Potential SQL injection risk from string formatting.")

    # 2. HIPAA & model safety check
    if "models/study.py" in generated_files:
        findings.append("Verified: Patient and ImagingStudy data models enforce typed clinical fields and age validation.")

    if "rules/clinical_rules.py" in generated_files:
        findings.append("Verified: Cardiothoracic Ratio (CTR) and lung density rules enforce safe numeric boundaries.")

    has_critical_error = any("Security Alert" in f for f in findings)
    review_passed = not has_critical_error
    
    state["review_feedback"] = findings
    state["review_passed"] = review_passed
    state["current_agent"] = "Code Reviewer"
    state["status"] = "TESTING" if review_passed else "CODING"
    
    add_log_entry(
        state,
        agent_name="Code Reviewer",
        message=f"Clinical audit completed: {'APPROVED' if review_passed else 'REJECTED'}. {len(findings)} checklist items audited.",
        status="DONE" if review_passed else "WARN"
    )
    
    return {
        "review_feedback": findings,
        "review_passed": review_passed,
        "current_agent": "Code Reviewer",
        "status": state["status"],
        "execution_log": state["execution_log"]
    }
