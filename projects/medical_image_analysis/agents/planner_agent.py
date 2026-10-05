"""
Tech Lead / Task Planner Agent Node for Medical Imaging
"""
from typing import Dict, Any, List
from core.state import SDLCState, add_log_entry
from core.llm import LLMClient

def planner_agent_node(state: SDLCState) -> Dict[str, Any]:
    arch = state.get("architecture", {})
    reqs = state.get("requirements", {})
    
    llm = LLMClient()
    system_instruction = (
        "You are an Agile Tech Lead for medical systems. Break down the system architecture into an ordered list "
        "of atomic file implementation tasks with dependencies and descriptions in valid JSON format: "
        "{'tasks': [{'task_id': '...', 'file_path': '...', 'description': '...', 'dependencies': []}]}"
    )
    
    prompt = f"Break down into ordered micro-tasks:\nArchitecture: {arch}\nRequirements: {reqs}"
    plan_json = llm.generate_json(prompt, system_instruction=system_instruction)
    tasks = plan_json.get("tasks", [])
    
    state["task_plan"] = tasks
    state["current_task_index"] = 0
    state["current_agent"] = "Tech Lead Planner"
    state["status"] = "CODING"
    
    add_log_entry(
        state,
        agent_name="Tech Lead Planner",
        message=f"Created {len(tasks)} sequenced clinical engineering tickets in the sprint backlog.",
        status="DONE"
    )
    
    return {
        "task_plan": tasks,
        "current_task_index": 0,
        "current_agent": "Tech Lead Planner",
        "status": "CODING",
        "execution_log": state["execution_log"]
    }
