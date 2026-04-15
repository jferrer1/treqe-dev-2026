# CONFIGURAR DOMINIO TREQE.ES EN NETLIFY - SCRIPT INTERACTIVO
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 CONFIGURACIÓN DOMINIO TREQE.ES EN NETLIFY" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Abrir Netlify Domain Management
Write-Host "PASO 1: Abriendo Netlify Domain Management..." -ForegroundColor Yellow
$netlifyUrl = "https://app.netlify.com/sites/sparkling-sawine-898bad/domains"
Start-Process $netlifyUrl
Write-Host "✅ Netlify abierto en navegador" -ForegroundColor Green
Write-Host ""

# 2. Instrucciones paso a paso
Write-Host "PASO 2: Sigue estos pasos en Netlify:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. En la página que se abrió, busca:" -ForegroundColor White
Write-Host "   'Add custom domain' o 'Add domain alias'" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Escribe el dominio:" -ForegroundColor White
Write-Host "   treqe.es" -ForegroundColor Magenta
Write-Host ""
Write-Host "3. Marca la opción (si aparece):" -ForegroundColor White
Write-Host "   [✓] Add www.treqe.es as an alias" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Clic en 'Verify' o 'Continue'" -ForegroundColor White
Write-Host ""
Write-Host "5. Netlify verificará DNS (ya está configurado ✅)" -ForegroundColor Gray
Write-Host ""
Write-Host "6. Espera 5-15 minutos para SSL automático" -ForegroundColor Gray
Write-Host ""

# 3. Verificar DNS actual
Write-Host "PASO 3: Verificando configuración DNS actual..." -ForegroundColor Yellow
Write-Host ""
try {
    $dnsTreqe = Resolve-DnsName -Name "treqe.es" -Type A -ErrorAction SilentlyContinue
    $dnsWww = Resolve-DnsName -Name "www.treqe.es" -Type A -ErrorAction SilentlyContinue
    
    if ($dnsTreqe) {
        Write-Host "✅ treqe.es → $($dnsTreqe.IPAddress)" -ForegroundColor Green
    } else {
        Write-Host "❌ treqe.es: No resuelve" -ForegroundColor Red
    }
    
    if ($dnsWww) {
        Write-Host "✅ www.treqe.es → $($dnsWww.IPAddress)" -ForegroundColor Green
    } else {
        Write-Host "❌ www.treqe.es: No resuelve" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️  No se pudo verificar DNS" -ForegroundColor Yellow
}
Write-Host ""

# 4. Verificar sitio temporal Netlify
Write-Host "PASO 4: Verificando sitio temporal Netlify..." -ForegroundColor Yellow
$tempUrl = "https://sparkling-sawine-898bad.netlify.app"
Write-Host "URL temporal: $tempUrl" -ForegroundColor Gray
Write-Host ""

# 5. Abrir verificación SSL después de 15 minutos
Write-Host "PASO 5: Después de configurar dominio:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Abre PowerShell y ejecuta:" -ForegroundColor White
Write-Host "curl -I https://treqe.es" -ForegroundColor Cyan
Write-Host ""
Write-Host "Debe devolver '200 OK' y SSL válido" -ForegroundColor Gray
Write-Host ""

# 6. Opciones de ayuda
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "¿NECESITAS AYUDA?" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Si no ves 'Add custom domain':" -ForegroundColor White
Write-Host "   - Ve a: https://app.netlify.com" -ForegroundColor Gray
Write-Host "   - Clic en 'sparkling-sawine-898bad'" -ForegroundColor Gray
Write-Host "   - En barra lateral: 'Domain management'" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Si DNS no verifica:" -ForegroundColor White
Write-Host "   - Espera 5 minutos" -ForegroundColor Gray
Write-Host "   - O contacta soporte Netlify" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Para verificar manualmente:" -ForegroundColor White
Write-Host "   https://www.whatsmydns.net/#A/treqe.es" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Pausa para leer
Write-Host ""
Write-Host "Presiona Enter para continuar..." -ForegroundColor Gray
$null = Read-Host

# Abrir todas las URLs útiles
Write-Host "Abriendo recursos útiles..." -ForegroundColor Yellow
Start-Process "https://www.whatsmydns.net/#A/treqe.es"
Start-Process "https://sparkling-sawine-898bad.netlify.app"

Write-Host ""
Write-Host "✅ Script completado. Sigue los pasos en Netlify." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan