"""
Local Knowledge Server for DBIP Project
Serves all project files and maintains context
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
import json
from datetime import datetime
import mimetypes

app = FastAPI(
    title="DBIP Knowledge Server",
    description="Serves DBIP project files and context",
    version="1.0.0"
)

# Enable CORS for chat access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Project root
PROJECT_ROOT = Path(__file__).parent

# Files and directories to serve
SERVE_DIRS = [
    "src",
    "memory",
    "docs",
    "config",
    "scripts",
    "tests",
    "requirements",
    "docker"
]

# Files to serve from root
ROOT_FILES = [
    ".env",
    ".gitignore",
    "README.md",
    "Makefile",
    "pyproject.toml",
    "test_server.py"
]


@app.get("/")
async def root():
    """Root endpoint - return project overview"""
    return {
        "name": "DBIP Project Knowledge Server",
        "version": "1.0.0",
        "base_path": str(PROJECT_ROOT),
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/files": "List all files in the project",
            "/files/{path}": "Get content of a specific file",
            "/tree": "Get full directory tree",
            "/context": "Get project context (memory/ files)",
            "/docs": "Get all documentation",
            "/status": "Get project status"
        }
    }


@app.get("/files")
async def list_files():
    """List all files in the project"""
    all_files = []
    
    # Get files from directories
    for dir_name in SERVE_DIRS:
        dir_path = PROJECT_ROOT / dir_name
        if dir_path.exists():
            for file_path in dir_path.rglob("*"):
                if file_path.is_file():
                    # Skip pycache files
                    if "__pycache__" in str(file_path):
                        continue
                    if file_path.suffix == ".pyc":
                        continue
                    rel_path = file_path.relative_to(PROJECT_ROOT)
                    all_files.append({
                        "path": str(rel_path),
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        "type": "code" if file_path.suffix in [".py", ".js", ".ts", ".html", ".css"] else "document"
                    })
    
    # Get root files
    for filename in ROOT_FILES:
        file_path = PROJECT_ROOT / filename
        if file_path.exists():
            all_files.append({
                "path": filename,
                "size": file_path.stat().st_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "type": "config" if filename.startswith(".") else "document"
            })
    
    return {
        "total_files": len(all_files),
        "files": all_files,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/tree")
async def get_tree():
    """Get full directory tree"""
    tree = []
    
    def build_tree(dir_path, level=0):
        items = []
        for item in sorted(dir_path.iterdir()):
            if item.name.startswith("__pycache__"):
                continue
            if item.name.endswith(".pyc"):
                continue
            if item.name in ["venv", ".git", ".vscode", ".idea", "node_modules"]:
                continue
            
            if item.is_dir():
                items.append({
                    "name": item.name,
                    "type": "directory",
                    "children": build_tree(item, level + 1)
                })
            else:
                items.append({
                    "name": item.name,
                    "type": "file",
                    "size": item.stat().st_size,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })
        return items
    
    for item in sorted(PROJECT_ROOT.iterdir()):
        if item.name in ["venv", ".git", ".vscode", ".idea", "__pycache__"]:
            continue
        if item.is_dir():
            tree.append({
                "name": item.name,
                "type": "directory",
                "children": build_tree(item, 1)
            })
        else:
            if item.name not in ["knowledge_server.py", "sync_server.py", "update_server.py"]:
                tree.append({
                    "name": item.name,
                    "type": "file",
                    "size": item.stat().st_size,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })
    
    return {"tree": tree}


@app.get("/files/{path:path}")
async def get_file(path: str):
    """Get content of a specific file"""
    file_path = PROJECT_ROOT / path
    
    # Security check - prevent path traversal
    try:
        file_path.relative_to(PROJECT_ROOT)
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    if file_path.is_dir():
        raise HTTPException(status_code=400, detail="Path is a directory")
    
    # Read file content
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = "Binary file (not displayed)"
    
    return {
        "path": path,
        "name": file_path.name,
        "content": content,
        "size": file_path.stat().st_size,
        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
        "suffix": file_path.suffix
    }


@app.get("/context")
async def get_context():
    """Get all context files from memory/ directory"""
    context_files = {}
    memory_dir = PROJECT_ROOT / "memory"
    
    if not memory_dir.exists():
        return {"error": "memory/ directory not found"}
    
    for file_path in memory_dir.glob("*.md"):
        context_files[file_path.name] = {
            "content": file_path.read_text(encoding="utf-8"),
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        }
    
    return {
        "context_files": context_files,
        "total_files": len(context_files),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/docs")
async def get_docs():
    """Get all documentation files"""
    docs = {}
    docs_dir = PROJECT_ROOT / "docs"
    
    if not docs_dir.exists():
        return {"error": "docs/ directory not found"}
    
    for file_path in docs_dir.glob("*"):
        if file_path.is_file():
            try:
                docs[file_path.name] = {
                    "content": file_path.read_text(encoding="utf-8"),
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                }
            except UnicodeDecodeError:
                docs[file_path.name] = {
                    "content": "Binary file (not displayed)",
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                }
    
    return docs


@app.get("/status")
async def get_status():
    """Get project status"""
    from datetime import datetime
    
    # Check if core files exist
    core_files = {
        "main.py": (PROJECT_ROOT / "src" / "main.py").exists(),
        "routes.py": (PROJECT_ROOT / "src" / "routes.py").exists(),
        "models.py": (PROJECT_ROOT / "src" / "models.py").exists(),
        "orchestrator.py": (PROJECT_ROOT / "src" / "orchestrator.py").exists(),
        "config.py": (PROJECT_ROOT / "src" / "config.py").exists()
    }
    
    # Check memory files
    memory_files = {}
    memory_dir = PROJECT_ROOT / "memory"
    if memory_dir.exists():
        for file in memory_dir.glob("*.md"):
            memory_files[file.name] = True
    
    # Check docs files
    docs_files = {}
    docs_dir = PROJECT_ROOT / "docs"
    if docs_dir.exists():
        for file in docs_dir.glob("*"):
            if file.is_file():
                docs_files[file.name] = True
    
    return {
        "project": "DBIP v6.0",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "core_files": core_files,
        "memory_files": memory_files,
        "docs_files": docs_files,
        "all_core_present": all(core_files.values())
    }


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 DBIP Knowledge Server Starting...")
    print("=" * 60)
    print(f"📁 Project Root: {PROJECT_ROOT}")
    print(f"🌐 Server: http://localhost:3000")
    print("=" * 60)
    print("\n📋 Available Endpoints:")
    print("  GET /          - Project overview")
    print("  GET /files     - List all files")
    print("  GET /tree      - Directory tree")
    print("  GET /files/{path} - Get file content")
    print("  GET /context   - Get memory/ files")
    print("  GET /docs      - Get docs/ files")
    print("  GET /status    - Project status")
    print("\n🔄 Update Server: python update_server.py")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=3000)