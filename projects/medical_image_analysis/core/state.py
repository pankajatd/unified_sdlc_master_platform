"""
Typed State Definition for Medical Image Analysis SDLC Multi-Agent System
"""
from typing import TypedDict, List, Dict, Any, Optional
import datetime

class SDLCState(TypedDict, total=False):
    # Pipeline Metadata
    project_name: str
    user_prompt: str
    target_directory: str
    status: str
    current_agent: str
    
    # Artifacts Produced by Agents
    requirements: Dict[str, Any]
    architecture: Dict[str, Any]
    task_plan: List[Dict[str, Any]]
    current_task_index: int
    generated_files: Dict[str, str]
    
    # Audit & Verification
    review_feedback: List[str]
    review_passed: bool
    test_results: Dict[str, Any]
    test_passed: bool
    iteration_count: int
    max_iterations: int
    healing_history: List[Dict[str, Any]]
    
    # Complete Chronological Log
    execution_log: List[Dict[str, Any]]

def create_initial_state(
    project_name: str,
    user_prompt: str,
    target_directory: str,
    max_iterations: int = 3
) -> SDLCState:
    return {
        "project_name": project_name,
        "user_prompt": user_prompt,
        "target_directory": target_directory,
        "status": "INITIATED",
        "current_agent": "Orchestrator",
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
        "execution_log": [
            {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "agent": "Orchestrator",
                "message": f"Initialized Medical Image Analysis SDLC pipeline for '{project_name}'",
                "status": "INFO"
            }
        ]
    }

def add_log_entry(state: SDLCState, agent_name: str, message: str, status: str = "INFO"):
    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent_name,
        "message": message,
        "status": status
    }
    if "execution_log" not in state:
        state["execution_log"] = []
    state["execution_log"].append(entry)
