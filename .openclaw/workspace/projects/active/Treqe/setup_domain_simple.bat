@echo off
echo ========================================
echo CONFIGURAR DOMINIO TREQE.ES EN NETLIFY
echo ========================================
echo.

echo 1. Abriendo Netlify Domain Management...
start https://app.netlify.com/sites/sparkling-sawine-898bad/domains
echo.

echo 2. Verificando DNS actual...
echo treqe.es:
nslookup treqe.es 2>nul | findstr "Address"
echo.
echo www.treqe.es:
nslookup www.treqe.es 2>nul | findstr "Address"
echo.

echo 3. INSTRUCCIONES:
echo.
echo En la pagina de Netlify:
echo - Busca "Add custom domain"
echo - Escribe: treqe.es
echo - Marca: "Add www.treqe.es as alias"
echo - Clic: "Verify"
echo.
echo 4. Espera 5-15 minutos para SSL.
echo.
echo 5. Verificar despues:
echo   curl -I https://treqe.es
echo.
echo ========================================
echo URLs utiles:
echo ========================================
echo Netlify: https://app.netlify.com/sites/sparkling-sawine-898bad/domains
echo Sitio temporal: https://sparkling-sawine-898bad.netlify.app
echo Verificador DNS: https://www.whatsmydns.net/#A/treqe.es
echo ========================================
pause