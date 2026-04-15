@echo off
echo ========================================
echo TREQE - DEPLOY AUTOMÁTICO NETLIFY
echo ========================================
echo.
echo PASO 1: Ve a https://app.netlify.com
echo.
echo PASO 2: Arrastra la carpeta completa:
echo    C:\Users\Shadow\.openclaw\workspace\projects\Treqe\treqe-netlify-deploy
echo.
echo PASO 3: Suelta en el área "Drag and drop"
echo.
echo PASO 4: Espera 30 segundos
echo.
echo PASO 5: Configura dominio:
echo    1. Clic en "Domain settings"
echo    2. Añade: treqe.es
echo    3. Añade también: www.treqe.es
echo    4. Espera 5-15 minutos para SSL
echo.
echo ========================================
echo ARCHIVOS INCLUIDOS:
echo - index.html (landing page profesional)
echo - netlify.toml (configuración automática)
echo - README.md (instrucciones)
echo ========================================
echo.
echo Presiona cualquier tecla para abrir Netlify...
pause >nul
start "" "https://app.netlify.com"
echo.
echo Presiona cualquier tecla para abrir la carpeta...
pause >nul
start "" "C:\Users\Shadow\.openclaw\workspace\projects\Treqe\treqe-netlify-deploy"
echo.
echo ¡Listo! Arrastra la carpeta a Netlify.
pause >nul