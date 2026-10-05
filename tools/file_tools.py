"""
Filesystem tools for SDLC multi-agent operations
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional

def ensure_directory(dir_path: str) -> str:
    """Ensures a directory exists and returns its string path."""
    p = Path(dir_path)
    p.mkdir(parents=True, exist_ok=True)
    return str(p.resolve())

def write_project_file(project_dir: str, rel_path: str, content: str) -> Dict[str, Any]:
    """
    Safely writes a file inside the target project directory.
    Returns metadata about the written file.
    """
    base = Path(project_dir).resolve()
    target = (base / rel_path).resolve()
    
    # Security guard: prevent path traversal outside project_dir
    if not str(target).startswith(str(base)):
        raise ValueError(f"Security error: Attempted file write outside project dir: {target}")
        
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    
    return {
        "rel_path": rel_path.replace("\\", "/"),
        "full_path": str(target),
        "bytes_written": len(content.encode("utf-8")),
        "lines": len(content.splitlines()),
        "status": "SUCCESS"
    }

def read_project_file(project_dir: str, rel_path: str) -> str:
    """Safely reads a file from the project directory."""
    base = Path(project_dir).resolve()
    target = (base / rel_path).resolve()
    
    if not str(target).startswith(str(base)):
        raise ValueError(f"Security error: Attempted file read outside project dir: {target}")
        
    if not target.exists():
        raise FileNotFoundError(f"Project file not found: {rel_path}")
        
    return target.read_text(encoding="utf-8")

def list_project_files(project_dir: str) -> List[Dict[str, Any]]:
    """Recursively lists all files in the project directory, skipping pycache/git."""
    base = Path(project_dir).resolve()
    if not base.exists():
        return []
        
    files = []
    for item in base.rglob("*"):
        if item.is_file():
            rel = item.relative_to(base)
            rel_str = str(rel).replace("\\", "/")
            if any(part.startswith(".") or part == "__pycache__" for part in rel.parts):
                continue
            files.append({
                "rel_path": rel_str,
                "size_bytes": item.stat().st_size,
                "extension": item.suffix
            })
    return sorted(files, key=lambda x: x["rel_path"])
