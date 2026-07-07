"""
DBIP Backup Script
Creates a complete backup of the project
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
import json
import sys

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
BACKUP_DIR = PROJECT_ROOT / "backups"

# Files and directories to exclude
EXCLUDE_PATTERNS = [
    "__pycache__",
    ".pytest_cache",
    ".git",
    "venv",
    ".vscode",
    ".idea",
    "*.pyc",
    "*.pyo",
    "*.log",
    "*.db",
    "*.sqlite",
    ".env",
    "server_manifest.json",
    "backups",
]

EXCLUDE_DIRS = [
    "__pycache__",
    ".pytest_cache",
    ".git",
    "venv",
    ".vscode",
    ".idea",
    "backups",
    "logs",
    "data",
]

EXCLUDE_FILES = [
    "*.pyc",
    "*.pyo",
    "*.log",
    "*.db",
    "*.sqlite",
    "server_manifest.json",
]

def should_exclude(path: Path) -> bool:
    """Check if a path should be excluded from backup"""
    # Check directory names
    for pattern in EXCLUDE_DIRS:
        if pattern in path.parts:
            return True
    
    # Check file patterns
    if path.is_file():
        for pattern in EXCLUDE_FILES:
            if pattern.startswith("*") and path.suffix == pattern[1:]:
                return True
            if path.name == pattern:
                return True
    
    # Check file extensions
    if path.suffix in ['.pyc', '.pyo', '.log', '.db', '.sqlite']:
        return True
    
    return False

def get_all_files(root: Path) -> list:
    """Get all files to backup"""
    files = []
    for path in root.rglob("*"):
        if should_exclude(path):
            continue
        if path.is_file():
            files.append(path)
    return files

def create_backup():
    """Create a backup of the project"""
    
    # Create backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"dbip_backup_{timestamp}"
    backup_path = BACKUP_DIR / backup_name
    
    print("=" * 60)
    print("📦 DBIP Backup System")
    print("=" * 60)
    print(f"\n📁 Source: {PROJECT_ROOT}")
    print(f"📁 Backup: {backup_path}")
    
    # Create backup directory
    backup_path.mkdir(parents=True, exist_ok=True)
    
    # Get all files to backup
    files = get_all_files(PROJECT_ROOT)
    print(f"\n📄 Found {len(files)} files to backup")
    
    # Copy files
    print("\n📋 Copying files...")
    for src_path in files:
        rel_path = src_path.relative_to(PROJECT_ROOT)
        dst_path = backup_path / rel_path
        
        # Create parent directories
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(src_path, dst_path)
        
        # Progress indicator
        print(f"   ✓ {rel_path}")
    
    # Create manifest
    manifest = {
        "backup_name": backup_name,
        "timestamp": datetime.now().isoformat(),
        "project": "DBIP",
        "version": "6.0.0",
        "total_files": len(files),
        "files": [str(f.relative_to(PROJECT_ROOT)) for f in files],
        "excluded": EXCLUDE_PATTERNS
    }
    
    manifest_path = backup_path / "BACKUP_MANIFEST.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    # Create ZIP archive
    print("\n📦 Creating ZIP archive...")
    zip_path = BACKUP_DIR / f"{backup_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in backup_path.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(backup_path)
                zipf.write(file_path, arcname)
    
    # Calculate size
    size_bytes = zip_path.stat().st_size
    size_mb = size_bytes / (1024 * 1024)
    
    print("\n" + "=" * 60)
    print("✅ Backup Complete!")
    print("=" * 60)
    print(f"📁 Backup Location: {backup_path}")
    print(f"📦 ZIP Archive: {zip_path}")
    print(f"📊 Size: {size_mb:.2f} MB")
    print(f"📄 Files: {len(files)}")
    print(f"🕐 Timestamp: {timestamp}")
    print("=" * 60)

if __name__ == "__main__":
    create_backup()