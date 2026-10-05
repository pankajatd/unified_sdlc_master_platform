"""
Software Architect Agent Node
"""

from typing import Dict, Any
from sdlc_core.state import SDLCState, add_log_entry
from sdlc_core.llm import LLMClient

def architect_agent_node(state: SDLCState) -> Dict[str, Any]:
    """
    Software Architect Agent:
    Transforms requirements into a system architecture, directory topology, and database schemas.
    """
    reqs = state.get("requirements", {})
    project_name = state.get("project_name", "Generated_App")
    
    llm = LLMClient()
    system_instruction = (
        "You are a Principal Software Architect. Design the architecture for the system. "
        "Define directory structure, list of files to create, tech stack, and module interfaces in valid JSON."
    )
    
    prompt = f"Design architecture for project '{project_name}' based on requirements:\n{reqs}"
    arch_json = llm.generate_json(prompt, system_instruction=system_instruction)
    
    state["architecture"] = arch_json
    state["current_agent"] = "Software Architect"
    add_log_entry(
        state,
        agent_name="Software Architect",
        message=f"Designed repository topology: {len(arch_json.get('files_to_create', []))} files planned across {len(arch_json.get('directory_structure', []))} directories.",
        status="DONE"
    )
    
    return {
        "architecture": arch_json,
        "current_agent": "Software Architect",
        "execution_log": state["execution_log"]
    }
