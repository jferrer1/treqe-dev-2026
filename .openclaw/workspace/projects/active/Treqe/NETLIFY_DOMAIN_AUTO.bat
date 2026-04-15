@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 CONFIGURADOR AUTOMÁTICO DOMINIO NETLIFY
echo ========================================
echo.

echo 📡 Verificando estado Netlify...
cd /d "%~dp0treqe-netlify-deploy"
call npx netlify status --json > netlify_status.json 2>nul

if exist netlify_status.json (
    echo ✅ Netlify CLI funcionando
    del netlify_status.json
) else (
    echo ❌ Netlify CLI no disponible
    echo Instalando Netlify CLI...
    call npm install -g netlify-cli 2>nul
)

echo.
echo 🔍 Verificando DNS...
echo.

echo treqe.es:
nslookup treqe.es 2>nul | findstr "Address"
echo.

echo www.treqe.es:
nslookup www.treqe.es 2>nul | findstr "Address"
echo.

echo 📋 Abriendo Netlify en navegador...
start "" "https://app.netlify.com/sites/sparkling-sawine-898bad/domains"
start "" "https://app.netlify.com/teams/mvptreqe/sites"
echo.

echo ========================================
echo 📝 INSTRUCCIONES PASO A PASO:
echo ========================================
echo.
echo 1. En la página de Netlify que se abrió:
echo    - Busca "Domain management" o "Add custom domain"
echo.
echo 2. Escribe el dominio:
echo    treqe.es
echo.
echo 3. Marca (si aparece):
echo    [✓] Add www.treqe.es as alias
echo.
echo 4. Clic en:
echo    "Verify" o "Continue"
echo.
echo 5. Netlify verificará DNS (ya configurado ✅)
echo.
echo 6. Espera 5-15 minutos para SSL automático
echo.
echo ========================================
echo 🔧 VERIFICACIÓN DESPUÉS:
echo ========================================
echo.
echo Después de 15 minutos, ejecuta:
echo curl -I https://treqe.es
echo.
echo Debe devolver "200 OK" y SSL válido
echo.
echo ========================================
echo 🌐 URLs IMPORTANTES:
echo ========================================
echo.
echo - Netlify Domain Management:
echo   https://app.netlify.com/sites/sparkling-sawine-898bad/domains
echo.
echo - Sitio temporal Netlify:
echo   https://sparkling-sawine-898bad.netlify.app
echo.
echo - Verificador DNS:
echo   https://www.whatsmydns.net/#A/treqe.es
echo.
echo ========================================
echo ⚡ COMANDOS RÁPIDOS (ejecuta en PowerShell):
echo ========================================
echo.
echo 1. Verificar DNS:
echo    nslookup treqe.es
echo    nslookup www.treqe.es
echo.
echo 2. Verificar sitio temporal:
echo    curl https://sparkling-sawine-898bad.netlify.app
echo.
echo 3. Verificar después de configurar dominio:
echo    curl -I https://treqe.es
echo.
echo ========================================
echo 🎯 ESTADO ACTUAL:
echo ========================================
echo.
echo ✅ Dominio registrado: treqe.es
echo ✅ DNS configurado: Apuntando a Netlify (75.2.60.5)
echo ✅ Landing page creada y desplegada
echo ✅ Netlify sitio creado: sparkling-sawine-898bad
echo ⏳ Pendiente: Configurar dominio en Netlify
echo ⏳ Pendiente: SSL automático (5-15 min después)
echo.
echo ========================================
echo Presiona cualquier tecla para salir...
pause >nul