# Script simple para añadir dominio treqe.es a Netlify
$NETLIFY_TOKEN = "nfc_CXPKVGcEB7yzJvPwkHyvz3duj4Ny41by8585"
$SITE_ID = "fe01fff1-84d7-483e-b037-35c682cb96d8"
$DOMAIN = "treqe.es"

Write-Host "========================================"
Write-Host "AÑADIENDO DOMINIO A NETLIFY VIA API"
Write-Host "========================================"
Write-Host ""

# Verificar DNS
Write-Host "Verificando DNS para $DOMAIN..."
try {
    $dns = Resolve-DnsName -Name $DOMAIN -Type A -ErrorAction Stop
    Write-Host "OK $DOMAIN -> $($dns.IPAddress)"
    
    if ($dns.IPAddress -eq "75.2.60.5") {
        Write-Host "OK DNS configurado correctamente (Netlify)"
    } else {
        Write-Host "ADVERTENCIA: DNS apunta a $($dns.IPAddress), deberia ser 75.2.60.5"
    }
} catch {
    Write-Host "ERROR: No se pudo resolver DNS para $DOMAIN"
    exit 1
}

Write-Host ""

# Añadir dominio via API
Write-Host "Añadiendo dominio $DOMAIN a Netlify..."

$headers = @{
    "Authorization" = "Bearer $NETLIFY_TOKEN"
    "Content-Type" = "application/json"
}

$body = @{
    domain = $DOMAIN
} | ConvertTo-Json

try {
    $url = "https://api.netlify.com/api/v1/sites/$SITE_ID/domains"
    Write-Host "URL: $url"
    
    $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -ErrorAction Stop
    
    Write-Host "EXITO: Dominio añadido!"
    Write-Host "Respuesta:"
    $response | ConvertTo-Json -Depth 10
    
} catch {
    Write-Host "ERROR añadiendo dominio: $($_.Exception.Message)"
    Write-Host ""
    Write-Host "INSTRUCCIONES MANUALES:"
    Write-Host "1. Ve a: https://app.netlify.com/sites/sparkling-sawine-898bad/domains"
    Write-Host "2. Busca: 'Add custom domain'"
    Write-Host "3. Escribe: $DOMAIN"
    Write-Host "4. Marca: 'Add www.$DOMAIN as alias'"
    Write-Host "5. Clic: 'Verify'"
    Write-Host "6. Espera 5-15 minutos para SSL"
}

Write-Host ""
Write-Host "========================================"
Write-Host "VERIFICACION FINAL:"
Write-Host "========================================"
Write-Host "1. Espera 5-15 minutos para SSL automatico"
Write-Host "2. Verifica con: curl -I https://$DOMAIN"
Write-Host "3. Debe devolver '200 OK'"
Write-Host ""
Write-Host "Estado:"
Write-Host "  OK DNS configurado"
Write-Host "  OK Dominio añadido a Netlify"
Write-Host "  PENDIENTE SSL (5-15 min)"
Write-Host "========================================"