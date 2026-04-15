#!/usr/bin/env python3
"""
Test Treqe Backend Import
Created: 2026-03-19 12:56 PM
Purpose: Test if Treqe backend imports correctly after dependency installation
"""

import sys
import os

# Add src directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), "projects", "Treqe", "backend")
src_dir = os.path.join(backend_dir, "src")

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print("=" * 50)
print("TREQE BACKEND IMPORT TEST")
print("=" * 50)
print(f"Backend directory: {backend_dir}")
print(f"Source directory: {src_dir}")
print(f"Python path includes src: {src_dir in sys.path}")
print()

# Test importing main module
print("1. Testing main module import...")
try:
    import main
    print("   ✅ SUCCESS - Main module imported")
    print(f"   App title: {main.app.title}")
    print(f"   App version: {main.app.version}")
    print(f"   Environment: Development (should show docs)")
except ImportError as e:
    print(f"   ❌ IMPORT ERROR: {e}")
    print("   Possible issues:")
    print("   - Missing __init__.py files")
    print("   - Incorrect Python path")
    print("   - Missing dependencies")
except Exception as e:
    print(f"   ❌ OTHER ERROR: {e}")
    print(f"   Error type: {type(e).__name__}")

print()

# Test importing key modules
print("2. Testing key module imports...")
key_modules = [
    ("auth", "Authentication module"),
    ("users", "User management"),
    ("items", "Item management"),
    ("preferences", "Preferences management"),
    ("matching", "Matching engine"),
    ("proposals", "Transaction system")
]

for module_name, description in key_modules:
    try:
        module = __import__(f"api.{module_name}", fromlist=[""])
        print(f"   ✅ {module_name}: {description}")
    except ImportError as e:
        print(f"   ❌ {module_name}: Failed - {e}")

print()

# Check FastAPI app structure
print("3. Checking FastAPI app structure...")
try:
    import main
    print(f"   Routes registered: {len(main.app.routes)}")
    
    # Check for key endpoints
    endpoint_patterns = ["/api/v1/users", "/api/v1/items", "/api/v1/preferences", 
                        "/api/v1/matching", "/api/v1/proposals", "/health", "/docs"]
    
    route_paths = [route.path for route in main.app.routes if hasattr(route, 'path')]
    print(f"   Total routes: {len(route_paths)}")
    
    for pattern in endpoint_patterns:
        matching = [p for p in route_paths if pattern in p]
        if matching:
            print(f"   ✅ {pattern}: {len(matching)} route(s)")
        else:
            print(f"   ⚠️  {pattern}: Not found")
            
except Exception as e:
    print(f"   ❌ Error checking app structure: {e}")

print()
print("=" * 50)
print("TEST SUMMARY")
print("=" * 50)

# Final assessment
try:
    import main
    if hasattr(main, 'app') and hasattr(main.app, 'title'):
        print("✅ TREQE BACKEND IMPORT SUCCESSFUL")
        print(f"   Ready for: uvicorn main:app --reload")
        print(f"   Docs at: http://localhost:8000/docs")
        print(f"   Health at: http://localhost:8000/health")
    else:
        print("⚠️  Partial success - app structure incomplete")
except:
    print("❌ TREQE BACKEND IMPORT FAILED")
    print("   Next steps:")
    print("   1. Check all __init__.py files exist")
    print("   2. Verify dependencies: pip install -r requirements.txt")
    print("   3. Test from correct directory: cd projects\\Treqe\\backend\\src")
    print("   4. Check for syntax errors in Python files")

print("=" * 50)