# Treqe Backend Import Fix Guide
**Issue:** Relative imports fail when running FastAPI app  
**Diagnosed:** 2026-03-19 1:56 PM  
**Root Cause:** Python relative imports require proper package context

---

## 📋 QUICK SUMMARY

### **Problem:**
- `ImportError: attempted relative import with no known parent package`
- Occurs when running `uvicorn main:app` from `projects\Treqe\backend\src\`
- Uvicorn subprocesses lose Python package context

### **Root Cause:**
Treqe backend uses relative imports (`from .database.connection`, `from .api import`) which only work when:
1. Module is part of an installed Python package
2. Running with correct Python path setup
3. Subprocesses inherit package context

### **Tested & Confirmed:**
- ✅ Dependencies installed (FastAPI, SQLAlchemy, Pydantic)
- ✅ Package structure created (`__init__.py` files)
- ✅ Uvicorn starts but subprocess fails
- ✅ Issue: Reloader spawns subprocess that loses context

---

## 🔧 FIX OPTIONS (Ranked by Preference)

### **OPTION 1: Install as Editable Package (RECOMMENDED)**
**Best for:** Development environment, preserves original code structure

```powershell
# 1. Navigate to backend directory
cd projects\Treqe\backend

# 2. Create setup.py if missing
@"
from setuptools import setup, find_packages

setup(
    name="treqe-backend",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        line.strip() for line in open("requirements.txt").readlines()
        if line.strip() and not line.startswith("#")
    ],
)
"@ | Out-File -FilePath setup.py -Encoding UTF8

# 3. Install in development mode
pip install -e .

# 4. Run from anywhere
uvicorn treqe.backend.src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Pros:**
- Preserves all relative imports
- Package available system-wide
- Professional development setup
- Easy to run from anywhere

**Cons:**
- Requires `setup.py` creation
- Modifies Python environment

---

### **OPTION 2: Modify Imports to Absolute**
**Best for:** Quick fix, minimal environment changes

```python
# In main.py, change:
from .database.connection import get_db, init_db
from .api import users, items, preferences, matching, proposals
from .utils.config import settings
from .utils.logger import setup_logging

# To:
from database.connection import get_db, init_db
from api import users, items, preferences, matching, proposals
from utils.config import settings
from utils.logger import setup_logging

# Also ensure all other files use absolute imports
```

**Apply fix:**
```powershell
# Backup original
Copy-Item projects\Treqe\backend\src\main.py projects\Treqe\backend\src\main.py.backup

# Apply changes (simplified - would need proper sed/editor)
(Get-Content projects\Treqe\backend\src\main.py) -replace 'from \.', 'from ' | Set-Content projects\Treqe\backend\src\main.py
```

**Pros:**
- Quick to implement
- No environment changes
- Works with current structure

**Cons:**
- Modifies source code
- Need to update all relative imports
- Less portable

---

### **OPTION 3: Python Path Workaround**
**Best for:** Temporary testing, no code/environment changes

```powershell
# Method A: Set PYTHONPATH
$env:PYTHONPATH = "C:\Users\Shadow\.openclaw\workspace\projects\Treqe\backend\src"
cd projects\Treqe\backend\src
uvicorn main:app --host 0.0.0.0 --port 8000

# Method B: Run with python -m and path
cd projects\Treqe\backend
python -c "import sys; sys.path.insert(0, 'src'); import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)"

# Method C: Create runner script
@"
import sys
import os

# Add src to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(backend_dir, 'src')
sys.path.insert(0, src_dir)

# Import and run
import uvicorn
uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
"@ | Out-File -FilePath run_treqe.py -Encoding UTF8

python run_treqe.py
```

**Pros:**
- No code/environment changes
- Flexible testing
- Multiple approaches

**Cons:**
- Hacky workaround
- Not production-ready
- Manual setup each time

---

### **OPTION 4: Uvicorn Configuration**
**Best for:** Production deployment, controlled environments

```python
# Create uvicorn_config.py
import sys
import os

# Setup paths before import
backend_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(backend_dir, 'src')
sys.path.insert(0, src_dir)

# Now import the app
from main import app

# Export for uvicorn
application = app
```

```powershell
# Run with config
cd projects\Treqe\backend
uvicorn uvicorn_config:application --host 0.0.0.0 --port 8000
```

**Pros:**
- Clean separation
- Production-ready
- Configurable

**Cons:**
- Extra configuration file
- Slightly more complex

---

## 🧪 TESTING THE FIX

### **Verification Steps:**
1. **Check imports work:**
   ```powershell
   cd projects\Treqe\backend
   python -c "import sys; sys.path.insert(0, 'src'); import main; print(f'Success: {main.app.title}')"
   ```

2. **Test uvicorn startup:**
   ```powershell
   cd projects\Treqe\backend\src
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Verify API endpoints:**
   - http://localhost:8000/docs (Swagger UI)
   - http://localhost:8000/health (Health check)
   - http://localhost:8000/ (Root endpoint)

### **Expected Success Indicators:**
- ✅ Uvicorn starts without ImportError
- ✅ "Uvicorn running on http://0.0.0.0:8000" message
- ✅ No subprocess crash messages
- ✅ API endpoints respond (test with curl or browser)

---

## 📊 IMPACT ASSESSMENT

### **Current State:**
- **Code:** Complete (6 modules, March 18)
- **Dependencies:** Installed (newer versions)
- **Structure:** Proper package files created
- **Blockers:** Relative import context issue

### **Fix Priority:**
1. **OPTION 1** (Editable package) - Professional, sustainable
2. **OPTION 2** (Absolute imports) - Quick, minimal
3. **OPTION 3** (Path workaround) - Temporary testing
4. **OPTION 4** (Uvicorn config) - Production focus

### **Time Estimates:**
- **Option 1:** 10-15 minutes (setup.py + install)
- **Option 2:** 5-10 minutes (import edits)
- **Option 3:** 2-5 minutes (path setup)
- **Option 4:** 10 minutes (config creation)

---

## 🚀 RECOMMENDED ACTION PLAN

### **Immediate (Today):**
```powershell
# 1. Try Option 3 (quickest test)
cd projects\Treqe\backend
$env:PYTHONPATH = "$pwd\src"
cd src
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 2. If that works, implement Option 1 (professional)
cd ..
# Create setup.py (see Option 1 above)
pip install -e .
uvicorn treqe.backend.src.main:app --host 0.0.0.0 --port 8000 --reload
```

### **If Still Failing:**
1. Check all `__init__.py` files exist in `src/`, `src/api/`, `src/database/`, `src/utils/`
2. Verify Python version compatibility (3.8+)
3. Check for syntax errors in Python files
4. Ensure no circular imports

### **Success Criteria:**
- [ ] Uvicorn starts without errors
- [ ] http://localhost:8000/docs loads
- [ ] All 6 API modules accessible
- [ ] Health endpoint returns `{"status": "healthy"}`

---

## 📝 DOCUMENTATION UPDATES NEEDED

### **Update These Files After Fix:**
1. **`treqe_backend_testing.ps1`** - Update import verification steps
2. **`treqe_backend_setup.ps1`** - Fix PowerShell syntax, add chosen solution
3. **`multi_project_status_tracker.md`** - Update Treqe status to "Testing"
4. **`midday_progress_report_2026-03-19.md`** - Add fix implementation

### **Lessons Learned for MEMORY.md:**
- Relative imports require proper package context
- Uvicorn subprocesses may lose Python path
- Development vs production import strategies differ
- Always test with reload disabled first when debugging imports

---

## 🔍 TROUBLESHOOTING

### **Common Issues & Solutions:**

#### **Issue: "ModuleNotFoundError" after fix**
**Solution:** Ensure `src` directory is in Python path before import.

#### **Issue: Uvicorn starts but endpoints 404**
**Solution:** Check router inclusion in `main.py` - all 6 modules should be included.

#### **Issue: Database connection errors**
**Solution:** Check `.env` file and database configuration in `src/utils/config.py`.

#### **Issue: Version conflicts**
**Solution:** Requirements.txt specifies older versions, newer ones installed. Either:
- Pin versions: `pip install fastapi==0.104.1`
- Test with current versions (likely compatible)

### **Debug Commands:**
```powershell
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Test module import
python -c "import sys; sys.path.insert(0, 'projects/Treqe/backend/src'); import main; print(main.app.title)"

# Check uvicorn availability
uvicorn --version

# Verify all dependencies
pip list | Select-String "fastapi|uvicorn|sqlalchemy|pydantic"
```

---

## ✅ FINAL CHECKLIST

### **Pre-Fix Verification:**
- [ ] All `__init__.py` files exist
- [ ] Dependencies installed (`pip list` shows key packages)
- [ ] No syntax errors in Python files
- [ ] `.env` file exists with configuration

### **Fix Implementation:**
- [ ] Choose and implement one fix option
- [ ] Test import verification
- [ ] Test uvicorn startup
- [ ] Verify API endpoints

### **Post-Fix Validation:**
- [ ] Update project tracker status
- [ ] Document solution in relevant files
- [ ] Test full API functionality
- [ ] Prepare for next phase (testing suite)

---

*Guide created: 2026-03-19 2:26 PM*  
*Based on diagnosis from 1:56 PM heartbeat investigation*  
*Ready for implementation of chosen fix option*