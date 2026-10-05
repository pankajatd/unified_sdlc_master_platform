"""
LangGraph Multi-Agent Workflow Definition for Medical Image Analysis SDLC
Equipped with dual-mode runtime: Native LangGraph StateGraph when available,
and robust zero-dependency native fallback engine for Python 3.8/Anaconda environments.
"""
import sys
from pathlib import Path
from typing import Literal, Dict, Any, Generator

BASE_DIR = str(Path(__file__).resolve().parent.parent)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.state import SDLCState
from agents import (
    pm_agent_node,
    architect_agent_node,
    planner_agent_node,
    developer_agent_node,
    reviewer_agent_node,
    qa_agent_node,
    healer_agent_node
)

# Try importing LangGraph; if absent (e.g. Python 3.8 environment), use built-in runner
try:
    from langgraph.graph import StateGraph, START, END
    LANGGRAPH_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    LANGGRAPH_AVAILABLE = False
    StateGraph = None
    START = None
    END = None

def route_reviewer_decision(state: SDLCState) -> Literal["qa", "developer"]:
    if state.get("review_passed", False):
        return "qa"
    return "developer"

def route_qa_decision(state: SDLCState) -> Literal["healer", "__end__"]:
    if state.get("test_passed", False):
        return "__end__"
    return "healer"

def route_healer_decision(state: SDLCState) -> Literal["qa", "__end__"]:
    if state.get("status") == "FAILED":
        return "__end__"
    return "qa"


class FallbackMedicalSDLCGraph:
    """
    High-reliability native Python workflow runner for the 7 SDLC Agents.
    Executes the exact state graph lifecycle without requiring external LangGraph binaries.
    """
    def stream(self, initial_state: Dict[str, Any]) -> Generator[Dict[str, Dict[str, Any]], None, None]:
        state = dict(initial_state)

        # 1. PM Agent
        pm_out = pm_agent_node(state)
        state.update(pm_out)
        yield {"pm": pm_out}

        # 2. Architect Agent
        arch_out = architect_agent_node(state)
        state.update(arch_out)
        yield {"architect": arch_out}

        # 3. Planner Agent
        plan_out = planner_agent_node(state)
        state.update(plan_out)
        yield {"planner": plan_out}

        # 4. Developer Agent
        dev_out = developer_agent_node(state)
        state.update(dev_out)
        yield {"developer": dev_out}

        # 5. Reviewer Agent
        rev_out = reviewer_agent_node(state)
        state.update(rev_out)
        yield {"reviewer": rev_out}

        # Reviewer feedback loop if needed
        dev_retries = 0
        while not state.get("review_passed", False) and dev_retries < 2:
            dev_retries += 1
            dev_out = developer_agent_node(state)
            state.update(dev_out)
            yield {"developer": dev_out}

            rev_out = reviewer_agent_node(state)
            state.update(rev_out)
            yield {"reviewer": rev_out}

        # 6. QA Agent
        qa_out = qa_agent_node(state)
        state.update(qa_out)
        yield {"qa": qa_out}

        # 7. Self-Healing Agent loop
        max_heal = state.get("max_healing_iterations", 3)
        heal_count = 0
        while not state.get("test_passed", False) and heal_count < max_heal:
            heal_count += 1
            heal_out = healer_agent_node(state)
            state.update(heal_out)
            yield {"healer": heal_out}

            if state.get("status") == "FAILED":
                break

            qa_out = qa_agent_node(state)
            state.update(qa_out)
            yield {"qa": qa_out}


def build_medical_sdlc_graph():
    """Assembles and compiles the Medical SDLC multi-agent StateGraph."""
    if LANGGRAPH_AVAILABLE:
        builder = StateGraph(SDLCState)

        # 1. Add all 7 agent nodes
        builder.add_node("pm", pm_agent_node)
        builder.add_node("architect", architect_agent_node)
        builder.add_node("planner", planner_agent_node)
        builder.add_node("developer", developer_agent_node)
        builder.add_node("reviewer", reviewer_agent_node)
        builder.add_node("qa", qa_agent_node)
        builder.add_node("healer", healer_agent_node)

        # 2. Add sequential planning edges
        builder.add_edge(START, "pm")
        builder.add_edge("pm", "architect")
        builder.add_edge("architect", "planner")
        builder.add_edge("planner", "developer")

        # 3. Add development & verification edges
        builder.add_edge("developer", "reviewer")
        builder.add_conditional_edges(
            "reviewer",
            route_reviewer_decision,
            {
                "qa": "qa",
                "developer": "developer"
            }
        )
        
        # 4. Add QA and Self-Healing loop edges
        builder.add_conditional_edges(
            "qa",
            route_qa_decision,
            {
                "__end__": END,
                "healer": "healer"
            }
        )
        builder.add_conditional_edges(
            "healer",
            route_healer_decision,
            {
                "qa": "qa",
                "__end__": END
            }
        )

        return builder.compile()
    else:
        return FallbackMedicalSDLCGraph()
