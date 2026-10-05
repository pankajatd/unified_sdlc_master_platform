"""
Software Architect Agent Node for Medical Imaging
"""
from typing import Dict, Any
from core.state import SDLCState, add_log_entry
from core.llm import LLMClient

def architect_agent_node(state: SDLCState) -> Dict[str, Any]:
    reqs = state.get("requirements", {})
    project_name = state.get("project_name", "medical_image_analysis")
    
    llm = LLMClient()
    system_instruction = (
        "You are a Principal Healthcare Software Architect. Design the HIPAA-compliant architecture "
        "for the medical image analysis system. Define directory structure, files to create, tech stack, "
        "and clinical database schema in valid JSON."
    )
    
    prompt = f"Design architecture for project '{project_name}' based on requirements:\n{reqs}"
    arch_json = llm.generate_json(prompt, system_instruction=system_instruction)
    
    state["architecture"] = arch_json
    state["current_agent"] = "Software Architect"
    add_log_entry(
        state,
        agent_name="Software Architect",
        message=f"Designed clinical repository topology: {len(arch_json.get('files_to_create', []))} files planned across {len(arch_json.get('directory_structure', []))} directories.",
        status="DONE"
    )
    
    return {
        "architecture": arch_json,
        "current_agent": "Software Architect",
        "execution_log": state["execution_log"]
    }
