"""
LangGraph Multi-Agent Workflow Definition for SDLC System
"""

import sys
from pathlib import Path
from typing import Literal

# Ensure project root is in sys.path
BASE_DIR = str(Path(__file__).resolve().parent.parent)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from langgraph.graph import StateGraph, START, END
from sdlc_core.state import SDLCState
from sdlc_agents import (
    pm_agent_node,
    architect_agent_node,
    planner_agent_node,
    developer_agent_node,
    reviewer_agent_node,
    qa_agent_node,
    healer_agent_node
)

def route_reviewer_decision(state: SDLCState) -> Literal["qa", "developer"]:
    """Conditional edge from reviewer node."""
    if state.get("review_passed", False):
        return "qa"
    return "developer"

def route_qa_decision(state: SDLCState) -> Literal["healer", "__end__"]:
    """Conditional edge from QA test runner node."""
    if state.get("test_passed", False):
        return "__end__"
    return "healer"

def route_healer_decision(state: SDLCState) -> Literal["qa", "__end__"]:
    """Conditional edge from Self-Healing node."""
    if state.get("status") == "FAILED":
        return "__end__"
    return "qa"

def build_sdlc_graph():
    """Assembles and compiles the SDLC multi-agent StateGraph."""
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
