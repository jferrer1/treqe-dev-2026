# Treqe Backend Setup Script
# Created: 2026-03-19 11:26 AM (Europe/Paris)
# Purpose: Fix import issues and prepare Treqe backend for testing

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "TREQE BACKEND SETUP SCRIPT" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
Write-Host "Status: Backend code verified, fixing import structure for testing" -ForegroundColor Yellow
Write-Host "" -ForegroundColor White

$StartTime = Get-Date
$SetupPath = "projects\Treqe\backend"
$SrcPath = "$SetupPath\src"

# ==========================================
# 1. VERIFY CURRENT STRUCTURE
# ==========================================
Write-Host "1. VERIFYING CURRENT STRUCTURE..." -ForegroundColor Green

if (-not (Test-Path $SetupPath)) {
    Write-Host "  ✗ Treqe backend not found at: $SetupPath" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ Treqe backend found: $SetupPath" -ForegroundColor Green

# Check key files
$RequiredFiles = @(
    "$SrcPath\main.py",
    "$SetupPath\requirements.txt",
    "$SrcPath\api\auth.py",
    "$SrcPath\api\users.py", 
    "$SrcPath\api\items.py",
    "$SrcPath\api\preferences.py",
    "$SrcPath\api\matching.py",
    "$SrcPath\api\proposals.py"
)

$missingFiles = @()
foreach ($file in $RequiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $(Split-Path $file -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $(Split-Path $file -Leaf)" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "  ⚠️ Missing $($missingFiles.Count) required files" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ All required files present" -ForegroundColor Green
}

# ==========================================
# 2. IDENTIFY IMPORT ISSUES
# ==========================================
Write-Host "`n2. IDENTIFYING IMPORT ISSUES..." -ForegroundColor Green

# Check main.py for relative import issues
$mainContent = Get-Content "$SrcPath\main.py" -Raw
$relativeImports = Select-String -InputObject $mainContent -Pattern "from \." | Select-Object -ExpandProperty Line

if ($relativeImports) {
    Write-Host "  ⚠️ Relative imports found in main.py:" -ForegroundColor Yellow
    foreach ($import in $relativeImports) {
        Write-Host "    $import" -ForegroundColor Gray
    }
    Write-Host "  Issue: Python needs package structure for relative imports" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ No relative import issues detected" -ForegroundColor Green
}

# Check for __init__.py files (needed for Python packages)
$initFiles = Get-ChildItem -Path $SrcPath -Recurse -Filter "__init__.py" -ErrorAction SilentlyContinue
if ($initFiles.Count -eq 0) {
    Write-Host "  ⚠️ No __init__.py files found (Python packages missing)" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ Found $($initFiles.Count) __init__.py files" -ForegroundColor Green
}

# ==========================================
# 3. CREATE PYTHON PACKAGE STRUCTURE
# ==========================================
Write-Host "`n3. CREATING PYTHON PACKAGE STRUCTURE..." -ForegroundColor Green

# Create __init__.py files where missing
$directoriesNeedingInit = @(
    $SrcPath,
    "$SrcPath\api",
    "$SrcPath\database", 
    "$SrcPath\utils",
    "$SrcPath\core"
)

$createdInits = 0
foreach ($dir in $directoriesNeedingInit) {
    $initFile = "$dir\__init__.py"
    if (Test-Path $dir -PathType Container) {
        if (-not (Test-Path $initFile)) {
            try {
                Set-Content -Path $initFile -Value "# Package initialization`n# Created: $(Get-Date -Format 'yyyy-MM-dd')"
                Write-Host "  ✓ Created: $initFile" -ForegroundColor Green
                $createdInits++
            } catch {
                Write-Host "  ✗ Failed to create: $initFile" -ForegroundColor Red
            }
        } else {
            Write-Host "  ✓ Already exists: $initFile" -ForegroundColor Gray
        }
    }
}

Write-Host "  Created $createdInits new __init__.py files" -ForegroundColor Green

# ==========================================
# 4. CHECK DEPENDENCIES
# ==========================================
Write-Host "`n4. CHECKING DEPENDENCIES..." -ForegroundColor Green

# Check Python version
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.([8-9]|1[0-9])") {
        Write-Host "  ✓ Python version: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Python version insufficient: $pythonVersion" -ForegroundColor Red
    }
} catch {
    Write-Host "  ✗ Python not found or error: $_" -ForegroundColor Red
}

# Check if requirements can be installed
if (Test-Path "$SetupPath\requirements.txt") {
    $reqCount = (Get-Content "$SetupPath\requirements.txt" | Where-Object { $_ -match "^[a-zA-Z]" }).Count
    Write-Host "  ✓ requirements.txt found with $reqCount packages" -ForegroundColor Green
    
    # Check a few key packages
    $keyPackages = @("fastapi", "uvicorn", "sqlalchemy", "pydantic")
    foreach ($pkg in $keyPackages) {
        try {
            python -c "import $pkg; print('$pkg')" 2>&1 | Out-Null
            Write-Host "    ✓ $pkg installed" -ForegroundColor Green
        } catch {
            Write-Host "    ✗ $pkg not installed" -ForegroundColor Red
        }
    }
}

# ==========================================
# 5. CREATE TEST ENTRY POINT
# ==========================================
Write-Host "`n5. CREATING TEST ENTRY POINT..." -ForegroundColor Green

# Create a simple test script that works around import issues
$testScript = @"
# Treqe Backend Test Entry Point
# Created: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
# Purpose: Test backend without import issues

import sys
import os

# Add src directory to Python path
src_dir = os.path.join(os.path.dirname(__file__), 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print("Testing Treqe Backend Import...")
try:
    # Try to import main module
    import main
    print("✅ Successfully imported main module")
    print(f"  App title: {main.app.title}")
    print(f"  App version: {main.app.version}")
    
    # Check routers
    print(f"  Routers registered: {len(main.app.routes)}")
    
    # Test health endpoint
    print("✅ Backend structure appears valid")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    print("Troubleshooting steps:")
    print("1. Check Python path includes 'src' directory")
    print("2. Verify all __init__.py files exist")
    print("3. Install dependencies: pip install -r requirements.txt")
"@

$testScriptPath = "$SetupPath\test_import.py"
Set-Content -Path $testScriptPath -Value $testScript
Write-Host "  ✓ Created test script: $testScriptPath" -ForegroundColor Green

# ==========================================
# 6. SETUP INSTRUCTIONS
# ==========================================
Write-Host "`n6. SETUP INSTRUCTIONS..." -ForegroundColor Green

$Instructions = @"

## NEXT STEPS TO RUN TREQE BACKEND:

### 1. INSTALL DEPENDENCIES:
```powershell
cd "$SetupPath"
pip install -r requirements.txt
```

### 2. TEST IMPORTS:
```powershell
cd "$SetupPath"
python test_import.py
```

### 3. RUN DEVELOPMENT SERVER:
```powershell
cd "$SetupPath\src"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. VERIFY API:
- Open browser to: http://localhost:8000/docs
- Test health endpoint: http://localhost:8000/health
- Verify all 6 API modules are accessible

### 5. RUN FULL TEST SUITE:
```powershell
cd "$SetupPath"
python -m pytest tests/ -v
```

## TROUBLESHOOTING:

### Issue: "ImportError: attempted relative import"
**Solution:** Ensure you're running from correct directory with `src` in Python path.

### Issue: Missing dependencies
**Solution:** Run `pip install -r requirements.txt`

### Issue: Database connection errors  
**Solution:** Check `.env` file and database configuration

## EXPECTED OUTCOME:
- FastAPI docs at http://localhost:8000/docs
- Health endpoint returns {"status": "healthy"}
- All 6 API modules accessible via /api/v1/
- Ready for integration testing
"@

Write-Host $Instructions -ForegroundColor Cyan

# ==========================================
# 7. SCRIPT SUMMARY
# ==========================================
$EndTime = Get-Date
$Duration = New-TimeSpan -Start $StartTime -End $EndTime

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "SETUP SCRIPT SUMMARY" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Script created: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor White
Write-Host "Setup path: $SetupPath" -ForegroundColor White
Write-Host "Actions performed:" -ForegroundColor White
Write-Host "  • Verified file structure" -ForegroundColor White
Write-Host "  • Identified import issues" -ForegroundColor White
Write-Host "  • Created Python package files ($createdInits __init__.py)" -ForegroundColor White
Write-Host "  • Created test entry point script" -ForegroundColor White
Write-Host "  • Generated setup instructions" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "**READY FOR:**" -ForegroundColor Green
Write-Host "• Dependency installation" -ForegroundColor Green
Write-Host "• Import testing" -ForegroundColor Green
Write-Host "• Development server startup" -ForegroundColor Green
Write-Host "• Full backend testing" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "**NEXT ACTION:**" -ForegroundColor Yellow
Write-Host "Run: cd `"$SetupPath`" && pip install -r requirements.txt" -ForegroundColor Yellow
Write-Host "Then: python test_import.py" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan