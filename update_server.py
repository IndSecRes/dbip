"""
Update Server Script
Refreshes the knowledge server with latest files
"""

import os
import sys
import subprocess
from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent

def get_all_files():
    """Get all files in the project"""
    files = []
    
    # Walk through all directories
    for root, dirs, filenames in os.walk(PROJECT_ROOT):
        # Skip these directories
        skip_dirs = ["venv", ".git", "__pycache__", ".vscode", ".idea", "node_modules"]
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for filename in filenames:
            if filename.endswith(".pyc"):
                continue
            full_path = Path(root) / filename
            rel_path = full_path.relative_to(PROJECT_ROOT)
            files.append({
                "path": str(rel_path),
                "name": filename,
                "modified": datetime.fromtimestamp(full_path.stat().st_mtime).isoformat()
            })
    
    return files

def update_knowledge_server():
    """Update the knowledge server with latest files"""
    print("=" * 60)
    print("🔄 Updating Knowledge Server...")
    print("=" * 60)
    
    # Get all files
    files = get_all_files()
    print(f"📁 Found {len(files)} files")
    
    # Save file list to a manifest
    manifest_path = PROJECT_ROOT / "server_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_files": len(files),
            "files": files
        }, f, indent=2)
    
    print(f"✅ Manifest saved: {manifest_path}")
    
    # Restart server if running
    print("\nℹ️  To restart the server, run:")
    print("   python knowledge_server.py")
    print("   (Or press Ctrl+C in the server terminal and restart)")
    
    print("\n" + "=" * 60)
    print("✅ Update complete!")
    print("📋 To start server: python knowledge_server.py")
    print("=" * 60)

if __name__ == "__main__":
    update_knowledge_server()