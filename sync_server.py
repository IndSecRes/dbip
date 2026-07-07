"""
Sync Server - One command to update and restart everything
"""

import os
import sys
import subprocess
from pathlib import Path
import time
import socket

PROJECT_ROOT = Path(__file__).parent

def find_process_on_port(port=3000):
    """Find process using a specific port"""
    try:
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True
        )
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                pid = parts[-1]
                return pid
    except:
        pass
    return None

def kill_process_on_port(port=3000):
    """Kill process on specific port"""
    pid = find_process_on_port(port)
    if pid:
        print(f"🔪 Killing process {pid} on port {port}")
        try:
            subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
            time.sleep(1)
            return True
        except Exception as e:
            print(f"⚠️  Could not kill process: {e}")
            return False
    else:
        print(f"ℹ️  No process found on port {port}")
        return True

def update_and_restart():
    """Update server and restart"""
    print("=" * 60)
    print("🚀 DBIP Sync Server")
    print("=" * 60)
    
    # Kill existing server
    print("\n🛑 Stopping existing server...")
    kill_process_on_port(3000)
    
    # Run update
    print("\n📦 Running update...")
    subprocess.run(['python', 'update_server.py'], capture_output=False)
    
    # Start server
    print("\n🚀 Starting server...")
    subprocess.Popen(
        ['python', 'knowledge_server.py'],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
    time.sleep(2)
    
    # Check if server is running
    if find_process_on_port(3000):
        print("\n" + "=" * 60)
        print("✅ Server running at: http://localhost:3000")
        print("=" * 60)
        print("\n📋 You can now access:")
        print("  http://localhost:3000/status")
        print("  http://localhost:3000/context")
        print("  http://localhost:3000/files")
        print("  http://localhost:3000/tree")
        print("\n💬 In chat window, paste:")
        print('  "Read everything from http://localhost:3000"')
        print("=" * 60)
    else:
        print("\n⚠️  Server may not have started. Run manually:")
        print("   python knowledge_server.py")
    print("=" * 60)

if __name__ == "__main__":
    update_and_restart()