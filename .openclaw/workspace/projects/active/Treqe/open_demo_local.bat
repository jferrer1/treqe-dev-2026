@echo off
echo ========================================
echo TREQE DEMO LOCAL - SOLO PARA TI
echo ========================================
echo.
echo 1. Iniciando backend API (localhost:8000)...
start cmd /k "cd /d "C:\Users\Shadow\.openclaw\workspace\projects\Treqe\backend" && python demo_local.py"

timeout /t 3 /nobreak >nul

echo.
echo 2. Abriendo landing page local...
start "" "C:\Users\Shadow\.openclaw\workspace\projects\Treqe\landing-page\index.html"

echo.
echo 3. Abriendo navegador con la API...
start "" "http://localhost:8000"

echo.
echo ========================================
echo DEMO INICIADA
echo ========================================
echo Backend: http://localhost:8000
echo Landing: file:///C:/Users/Shadow/.openclaw/workspace/projects/Treqe/landing-page/index.html
echo.
echo Login demo: ana_tech / password123
echo.
echo Presiona cualquier tecla para salir...
pause >nul