# Script para actualizar todas las pantallas restantes
# Estándar: quitar hora, estandarizar demo notice, formato moneda, navegación

$screens = @(
    "v7-seguimiento",
    "v8-ajustes", 
    "v9-splash",
    "v10-registro",
    "v11-notificaciones",
    "v12-mis-matches"
)

foreach ($screen in $screens) {
    $file = "$screen/index.html"
    Write-Host "Processing $file..."
    
    if (Test-Path $file) {
        $content = Get-Content $file -Raw -Encoding UTF8
        
        # 1. Quitar hora de status bar
        $content = $content -replace '<span class="time">\d{2}:\d{2}</span>\s*', ''
        
        # 2. Estandarizar demo notice
        $content = $content -replace '<i class="fas fa-paint-brush"></i> Prototipo[^<]*', '<i class="fas fa-flask"></i> Treqe Prototype'
        $content = $content -replace '-- \d{1,2} Abril? \d{4}', '-- Apr 2026'
        $content = $content -replace '-- \d{1,2} Abr \d{4}', '-- Apr 2026'
        
        # 3. Formato moneda (precio€ -> €precio)
        $content = $content -replace '(\d+)\s*<small>€</small>', '€$1'
        $content = $content -replace '(\d+)\s*€(?!</)', '€$1'
        
        Set-Content $file $content -Encoding UTF8 -NoNewline
        Write-Host "  ✓ Updated $file"
    } else {
        Write-Host "  ✗ File not found: $file"
    }
}

Write-Host "`nDone! Run 'git add -A && git commit -m \"feat: Fase 1 complete - all screens standardized\"'"
