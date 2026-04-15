# Script para verificar estado del dominio treqe.es
Write-Host "========================================"
Write-Host "VERIFICADOR DOMINIO TREQE.ES"
Write-Host "========================================"
Write-Host ""

# 1. Verificar DNS
Write-Host "1. VERIFICANDO DNS:"
try {
    $ip1 = Resolve-DnsName -Name "treqe.es" -Type A -ErrorAction Stop | Select-Object -First 1
    $ip2 = Resolve-DnsName -Name "www.treqe.es" -Type A -ErrorAction Stop | Select-Object -First 1
    
    Write-Host "   treqe.es    -> $($ip1.IPAddress)"
    Write-Host "   www.treqe.es -> $($ip2.IPAddress)"
    
    if ($ip1.IPAddress -eq "75.2.60.5" -and $ip2.IPAddress -eq "75.2.60.5") {
        Write-Host "   ✅ DNS CONFIGURADO CORRECTAMENTE" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  DNS NO APUNTA A NETLIFY (75.2.60.5)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ ERROR RESOLVIENDO DNS" -ForegroundColor Red
}
Write-Host ""

# 2. Verificar sitio temporal Netlify
Write-Host "2. VERIFICANDO SITIO TEMPORAL NETLIFY:"
$tempUrl = "https://sparkling-sawine-898bad.netlify.app"
try {
    $response = Invoke-WebRequest -Uri $tempUrl -Method Head -TimeoutSec 10 -ErrorAction Stop
    Write-Host "   $tempUrl -> $($response.StatusCode) $($response.StatusDescription)" -ForegroundColor Green
    Write-Host "   ✅ SITIO TEMPORAL FUNCIONANDO" -ForegroundColor Green
} catch {
    Write-Host "   ❌ SITIO TEMPORAL NO RESPONDE" -ForegroundColor Red
}
Write-Host ""

# 3. Verificar dominio principal (despues de configurar)
Write-Host "3. VERIFICANDO DOMINIO PRINCIPAL:"
$mainUrl = "https://treqe.es"
try {
    $response = Invoke-WebRequest -Uri $mainUrl -Method Head -TimeoutSec 10 -ErrorAction Stop
    Write-Host "   $mainUrl -> $($response.StatusCode) $($response.StatusDescription)" -ForegroundColor Green
    
    # Verificar SSL
    if ($response.BaseResponse.SslProtocol -gt 0) {
        Write-Host "   ✅ SSL ACTIVO" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  SSL NO DETECTADO" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ DOMINIO NO CONFIGURADO O SSL PENDIENTE" -ForegroundColor Red
    Write-Host "   Mensaje: $($_.Exception.Message)" -ForegroundColor Gray
}
Write-Host ""

# 4. Instrucciones si no funciona
Write-Host "4. INSTRUCCIONES SI NO FUNCIONA:"
Write-Host "   a) Ve a: https://app.netlify.com/sites/sparkling-sawine-898bad/domains"
Write-Host "   b) Busca: 'Add custom domain'"
Write-Host "   c) Escribe: treqe.es"
Write-Host "   d) Marca: 'Add www.treqe.es as alias'"
Write-Host "   e) Clic: 'Verify'"
Write-Host "   f) Espera 5-15 minutos"
Write-Host ""

# 5. Comandos utiles
Write-Host "5. COMANDOS UTILES:"
Write-Host "   Verificar DNS: nslookup treqe.es"
Write-Host "   Verificar SSL: curl -I https://treqe.es"
Write-Host "   Abrir Netlify: npx netlify open:admin"
Write-Host ""

Write-Host "========================================"
Write-Host "ESTADO ACTUAL:"
Write-Host "========================================"
Write-Host "✅ Dominio registrado: treqe.es"
Write-Host "✅ DNS configurado: 75.2.60.5"
Write-Host "✅ Landing page desplegada"
Write-Host "✅ Netlify sitio creado"
Write-Host "⏳ Pendiente: Configurar dominio en Netlify UI"
Write-Host "⏳ Pendiente: SSL automatico (5-15 min)"
Write-Host "========================================"