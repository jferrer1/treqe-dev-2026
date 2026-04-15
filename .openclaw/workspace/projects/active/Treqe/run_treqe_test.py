#!/usr/bin/env python3
"""
Run Treqe Backend Test
Try different methods to resolve import issues
"""

import os
import sys
import subprocess
import time

print("=" * 60)
print("TREQE BACKEND RUN TEST")
print("=" * 60)
print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Paths
workspace = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(workspace, "projects", "Treqe", "backend")
src_dir = os.path.join(backend_dir, "src")

print(f"Workspace: {workspace}")
print(f"Backend dir: {backend_dir}")
print(f"Source dir: {src_dir}")
print()

# Method 1: Run uvicorn directly
print("1. Testing: Run uvicorn directly from src directory")
print("   Command: cd src && uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
print()

# First check if we can even import
print("2. Testing import with different methods:")
print()

# Method A: Add src to path and import
print("   Method A: Add src to sys.path")
sys.path.insert(0, src_dir)
try:
    import main
    print("   ✅ Success - main module imported")
    print(f"      App title: {main.app.title}")
except ImportError as e:
    print(f"   ❌ ImportError: {e}")
except Exception as e:
    print(f"   ❌ Other error: {type(e).__name__}: {e}")
print()

# Method B: Try running as module
print("   Method B: Run as Python module")
print("   Command: python -m uvicorn main:app")
print("   (Would need to be in src directory with proper package structure)")
print()

# Method C: Check if we can run the __main__ block
print("   Method C: Check main.py __main__ block")
main_path = os.path.join(src_dir, "main.py")
if os.path.exists(main_path):
    with open(main_path, 'r') as f:
        content = f.read()
        if 'if __name__ == "__main__":' in content:
            print("   ✅ main.py has __main__ block")
            # Extract uvicorn run command
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'uvicorn.run' in line:
                    print(f"   Found: {line.strip()}")
        else:
            print("   ⚠️  main.py has no __main__ block")
else:
    print("   ❌ main.py not found")
print()

# Check environment
print("3. Environment check:")
print(f"   Python version: {sys.version.split()[0]}")
print(f"   Current directory: {os.getcwd()}")
print(f"   src in sys.path: {src_dir in sys.path}")
print()

# Check key imports work
print("4. Testing key imports (without relative imports):")
try:
    import fastapi
    print(f"   ✅ fastapi: {fastapi.__version__}")
except:
    print("   ❌ fastapi: Not available")

try:
    import sqlalchemy
    print(f"   ✅ sqlalchemy: {sqlalchemy.__version__}")
except:
    print("   ❌ sqlalchemy: Not available")

try:
    import pydantic
    print(f"   ✅ pydantic: {pydantic.__version__}")
except:
    print("   ❌ pydantic: Not available")
print()

# Recommendations
print("5. RECOMMENDATIONS:")
print("   A. Run from src directory as module:")
print("      cd projects\\Treqe\\backend\\src")
print("      python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
print()
print("   B. If that fails, modify main.py imports:")
print("      Change 'from .database.connection' to absolute imports")
print("      Or ensure src is a proper Python package")
print()
print("   C. Alternative: Run the __main__ block directly")
print("      cd projects\\Treqe\\backend\\src")
print("      python main.py")
print()

print("=" * 60)
print("READY FOR TEST EXECUTION")
print("=" * 60)
print("Next step: Try running uvicorn from src directory")
print("If successful, API will be available at:")
print("  - http://localhost:8000")
print("  - http://localhost:8000/docs")
print("  - http://localhost:8000/health")
print("=" * 60)