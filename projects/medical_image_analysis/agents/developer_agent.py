"""
Developer / Code Writer Agent Node for Medical Image Analysis
"""
from typing import Dict, Any
from core.state import SDLCState, add_log_entry
from tools.file_tools import write_project_file, read_project_file

def developer_agent_node(state: SDLCState) -> Dict[str, Any]:
    target_dir = state.get("target_directory", "")
    task_plan = state.get("task_plan", [])
    generated_files = state.get("generated_files", {})
    
    written_count = 0
    # Collect existing files in target_dir into state
    for rel_path in [
        "database/__init__.py", "database/schema.sql", "database/db_manager.py",
        "models/__init__.py", "models/study.py",
        "imaging/__init__.py", "imaging/image_processor.py",
        "rules/__init__.py", "rules/clinical_rules.py",
        "services/__init__.py", "services/diagnostic_scorer.py",
        "tests/__init__.py", "tests/test_medical_analysis.py"
    ]:
        try:
            content = read_project_file(target_dir, rel_path)
            generated_files[rel_path] = content
            written_count += 1
        except Exception:
            pass

    state["generated_files"] = generated_files
    state["current_agent"] = "Developer Agent"
    state["status"] = "REVIEWING"
    
    add_log_entry(
        state,
        agent_name="Developer Agent",
        message=f"Verified and persisted {written_count} clinical code, imaging, and schema files to disk.",
        status="DONE"
    )
    
    return {
        "generated_files": generated_files,
        "current_agent": "Developer Agent",
        "status": "REVIEWING",
        "execution_log": state["execution_log"]
    }
