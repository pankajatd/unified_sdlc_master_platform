"""
Product Manager / Requirements Agent Node
"""

from typing import Dict, Any
from sdlc_core.state import SDLCState, add_log_entry
from sdlc_core.llm import LLMClient

def pm_agent_node(state: SDLCState) -> Dict[str, Any]:
    """
    Requirements Analysis & SRS Agent:
    Parses the user prompt and generates a structured specification.
    """
    user_prompt = state.get("user_prompt", "")
    project_name = state.get("project_name", "Generated_App")
    
    llm = LLMClient()
    system_instruction = (
        "You are an expert Agile Product Manager and Business Analyst. "
        "Analyze the user's software project prompt and produce a comprehensive "
        "Software Requirements Specification (SRS) in valid JSON format. "
        "Include: project_title, summary, user_stories, functional_requirements, acceptance_criteria."
    )
    
    prompt = f"Project: {project_name}\nPrompt: {user_prompt}\nGenerate SRS in JSON format."
    req_json = llm.generate_json(prompt, system_instruction=system_instruction)
    
    state["requirements"] = req_json
    state["current_agent"] = "PM Agent"
    state["status"] = "PLANNING"
    add_log_entry(
        state,
        agent_name="PM Agent",
        message=f"Formulated Software Requirements Specification with {len(req_json.get('functional_requirements', []))} functional requirements.",
        status="DONE"
    )
    
    return {
        "requirements": req_json,
        "current_agent": "PM Agent",
        "status": "PLANNING",
        "execution_log": state["execution_log"]
    }
