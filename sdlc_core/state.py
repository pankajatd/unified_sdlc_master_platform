"""
SDLC State Definition for LangGraph Workflow
"""

from typing import TypedDict, List, Dict, Any, Optional
import datetime

class SDLCState(TypedDict, total=False):
    # Metadata & User Intent
    project_name: str
    user_prompt: str
    target_directory: str
    
    # Requirements & Architecture
    requirements: Dict[str, Any]
    architecture: Dict[str, Any]
    task_plan: List[Dict[str, Any]]
    
    # Code Generation Tracking
    current_task_index: int
    generated_files: Dict[str, str]   # relative_path -> file_content
    
    # Review & QA
    review_feedback: List[Dict[str, Any]]
    review_passed: bool
    test_results: Dict[str, Any]      # total, passed, failed, failures: List[dict], stdout, stderr
    test_passed: bool
    
    # Self-Healing Control
    iteration_count: int
    max_iterations: int
    healing_history: List[Dict[str, Any]]
    
    # Live Audit & Orchestration
    current_agent: str
    execution_log: List[Dict[str, Any]]
    status: str                       # PLANNING, CODING, REVIEWING, TESTING, HEALING, COMPLETED, FAILED
    error: Optional[str]


def create_initial_state(project_name: str, user_prompt: str, target_directory: str, max_iterations: int = 3) -> SDLCState:
    """Creates a clean initial SDLC state."""
    return {
        "project_name": project_name,
        "user_prompt": user_prompt,
        "target_directory": str(target_directory),
        "requirements": {},
        "architecture": {},
        "task_plan": [],
        "current_task_index": 0,
        "generated_files": {},
        "review_feedback": [],
        "review_passed": False,
        "test_results": {},
        "test_passed": False,
        "iteration_count": 0,
        "max_iterations": max_iterations,
        "healing_history": [],
        "current_agent": "system",
        "execution_log": [
            {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "agent": "System",
                "message": f"Initialized SDLC pipeline for project '{project_name}'.",
                "status": "INIT"
            }
        ],
        "status": "PLANNING",
        "error": None
    }


def add_log_entry(state: SDLCState, agent_name: str, message: str, status: str = "INFO") -> None:
    """Helper to append an audit entry to the execution log."""
    if "execution_log" not in state or state["execution_log"] is None:
        state["execution_log"] = []
    state["execution_log"].append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent_name,
        "message": message,
        "status": status
    })
