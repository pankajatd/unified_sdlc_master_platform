"""
File operations tool for Medical Image Analysis SDLC
"""
import os
from pathlib import Path
from typing import List, Dict, Any

def write_project_file(project_dir: str, rel_path: str, content: str) -> str:
    full_path = (Path(project_dir) / rel_path).resolve()
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return str(full_path)

def read_project_file(project_dir: str, rel_path: str) -> str:
    full_path = (Path(project_dir) / rel_path).resolve()
    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {full_path}")
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()

def list_project_files(project_dir: str) -> List[Dict[str, Any]]:
    p = Path(project_dir).resolve()
    if not p.exists():
        return []
    result = []
    for item in p.rglob("*"):
        rel_parts = item.relative_to(p).parts
        if item.is_file() and not any(part.startswith((".", "__pycache__", "venv")) for part in rel_parts):
            rel = str(item.relative_to(p)).replace("\\", "/")
            result.append({
                "rel_path": rel,
                "size_bytes": item.stat().st_size,
                "abs_path": str(item)
            })
    return sorted(result, key=lambda x: x["rel_path"])
