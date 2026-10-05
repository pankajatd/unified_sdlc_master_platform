"""
Command Line Interface runner for Medical Image Analysis SDLC Multi-Agent System
"""
import sys
import os
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from config import MAX_HEALING_ITERATIONS
from core.state import create_initial_state
from core.graph import build_medical_sdlc_graph
from tools.file_tools import list_project_files

def main():
    parser = argparse.ArgumentParser(description="Medical Image Analysis SDLC Multi-Agent System")
    parser.add_argument(
        "--prompt",
        type=str,
        default="Build an automated Medical Image Analysis and Clinical Decision Support System with SQLite database, digital image processing for Chest X-Ray findings (Pneumonia, Cardiomegaly CTR, Pulmonary Nodule), composite diagnostic scoring, and unit tests",
        help="Prompt specifying clinical features to build or verify"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=MAX_HEALING_ITERATIONS,
        help="Max self-healing loop attempts"
    )

    args = parser.parse_args()

    print("=" * 70)
    print("[MEDVISION SDLC] AUTONOMOUS CLINICAL MULTI-AGENT SYSTEM (LangGraph)")
    print("=" * 70)
    print(f"Target Directory:  {BASE_DIR}")
    print(f"Clinical Prompt:   {args.prompt}")
    print(f"Max Healing Tries: {args.max_iterations}")
    print("=" * 70)

    initial_state = create_initial_state(
        project_name="medical_image_analysis",
        user_prompt=args.prompt,
        target_directory=str(BASE_DIR),
        max_iterations=args.max_iterations
    )

    graph = build_medical_sdlc_graph()
    
    print("\n[Orchestrator] Executing clinical agent squad workflow...\n")

    current_state = initial_state
    for event in graph.stream(initial_state):
        for node_name, node_update in event.items():
            agent = node_update.get("current_agent", node_name)
            logs = node_update.get("execution_log", [])
            last_msg = logs[-1]["message"] if logs else f"Node {node_name} completed."
            print(f"  [AGENT: {agent.upper():<20}] -> {last_msg}")
            current_state.update(node_update)

    print("\n" + "=" * 70)
    print("CLINICAL SDLC WORKFLOW SUMMARY")
    print("=" * 70)
    print(f"Overall Status:        {current_state.get('status')}")
    print(f"Review Status:         {'APPROVED' if current_state.get('review_passed') else 'REJECTED'}")
    print(f"Unit Tests Passed:     {'YES (100%)' if current_state.get('test_passed') else 'NO'}")
    
    test_res = current_state.get("test_results", {})
    if test_res:
        print(f"Test Statistics:       Passed: {test_res.get('passed_count')}, Failed: {test_res.get('failed_count')}, Total: {test_res.get('total_count')}")
        print(f"Test Duration:         {test_res.get('duration_sec')}s")

    files = list_project_files(str(BASE_DIR))
    print(f"\nFiles in Medical Platform ({len(files)} files on disk):")
    for f in files:
        print(f"   * {f['rel_path']} ({f['size_bytes']} bytes)")

    print("=" * 70)
    print("[SUCCESS] MedVision AI Clinical Decision Support Engine Ready!")
    print("=" * 70)

if __name__ == "__main__":
    main()
