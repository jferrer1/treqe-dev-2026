# Limpieza agresiva manual de Treqe
Write-Host "=== LIMPIEZA AGRESIVA TREQE ===" -ForegroundColor Cyan
Write-Host "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

# 1. IDENTIFICAR DOCUMENTOS DUPLICADOS
Write-Host "1. IDENTIFICANDO DOCUMENTOS DUPLICADOS..." -ForegroundColor Yellow
$docxFiles = Get-ChildItem -Recurse -Filter "*.docx" -File | Where-Object { $_.DirectoryName -notmatch "_archive" }

Write-Host "   Total documentos .docx: $($docxFiles.Count)"

# Agrupar por nombre base (sin números, versiones, etc.)
$docGroups = @{}
foreach ($file in $docxFiles) {
    $baseName = $file.BaseName -replace '\(\d+\)$', '' -replace '_v\d+', '' -replace '_FINAL', '' -replace '_COMPLETO', '' -replace '_ACTUALIZADO', '' -replace '_HUMANIZADO', '' -replace '_MEJORADO', ''
    $baseName = $baseName.Trim()
    
    if (-not $docGroups.ContainsKey($baseName)) {
        $docGroups[$baseName] = @()
    }
    $docGroups[$baseName] += $file
}

Write-Host "   Grupos identificados: $($docGroups.Count)"

# Mostrar grupos con múltiples archivos
$duplicateGroups = $docGroups.GetEnumerator() | Where-Object { $_.Value.Count -gt 1 }
Write-Host "   Grupos con duplicados: $($duplicateGroups.Count)"

foreach ($group in $duplicateGroups | Select-Object -First 5) {
    Write-Host "   - $($group.Key): $($group.Value.Count) archivos"
    foreach ($file in $group.Value | Sort-Object LastWriteTime -Descending | Select-Object -First 3) {
        Write-Host "     * $($file.Name) ($($file.Length/1KB) KB, $($file.LastWriteTime))"
    }
}

# 2. IDENTIFICAR SCRIPTS TEMPORALES
Write-Host "`n2. IDENTIFICANDO SCRIPTS TEMPORALES..." -ForegroundColor Yellow
$pyFiles = Get-ChildItem -Recurse -Filter "*.py" -File | Where-Object { $_.DirectoryName -notmatch "_archive" }

Write-Host "   Total scripts .py: $($pyFiles.Count)"

# Categorizar scripts
$tempPatterns = @(
    "crear_", "generar_", "actualizar_", "corregir_", "humanizar_",
    "completar_", "integrar_", "reescribir_", "convertir_", "mejorar_",
    "anadir_", "aplicar_", "analizar_", "check_", "test_", "verificar_"
)

$tempScripts = $pyFiles | Where-Object {
    $isTemp = $false
    foreach ($pattern in $tempPatterns) {
        if ($_.Name -match $pattern) {
            $isTemp = $true
            break
        }
    }
    $isTemp
}

Write-Host "   Scripts temporales identificados: $($tempScripts.Count)"

# 3. RECOMENDACIONES DE LIMPIEZA
Write-Host "`n3. RECOMENDACIONES DE LIMPIEZA:" -ForegroundColor Green

Write-Host "   a) DOCUMENTOS .docx a consolidar:" -ForegroundColor Magenta
foreach ($group in $duplicateGroups) {
    $latest = $group.Value | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    $others = $group.Value | Where-Object { $_.FullName -ne $latest.FullName }
    
    Write-Host "   - Mantener: $($latest.Name) ($($latest.Length/1KB) KB, $($latest.LastWriteTime))"
    Write-Host "     Archivar: $($others.Count) versiones antiguas"
}

Write-Host "`n   b) SCRIPTS .py a archivar:" -ForegroundColor Magenta
$tempScripts | Sort-Object LastWriteTime -Descending | Select-Object -First 10 | ForEach-Object {
    Write-Host "   - $($_.Name) ($($_.Length/1KB) KB, $($_.LastWriteTime.ToString('yyyy-MM-dd')))"
}

# 4. PLAN DE ACCIÓN
Write-Host "`n4. PLAN DE ACCIÓN SUGERIDO:" -ForegroundColor Cyan

Write-Host "   FASE A: Consolidar documentos (reducción ~70%)"
Write-Host "   - Mantener solo versión más reciente de cada documento"
Write-Host "   - Archivar: $($docxFiles.Count - $docGroups.Count) documentos duplicados"
Write-Host "   - Resultado: $($docGroups.Count) documentos vs $($docxFiles.Count) actuales"

Write-Host "`n   FASE B: Limpiar scripts (reducción ~80%)"
Write-Host "   - Mantener scripts esenciales:"
Write-Host "     * limpieza_inteligente.py (sistema mantenimiento)"
Write-Host "     * scripts en plan_negocio/PLAN_SEGREGADO_2026/ (generación secciones)"
Write-Host "     * scripts en subagents/ (agentes especializados)"
Write-Host "   - Archivar: $($tempScripts.Count) scripts temporales"
Write-Host "   - Resultado: ~45 scripts vs $($pyFiles.Count) actuales"

Write-Host "`n   FASE C: Organizar estructura"
Write-Host "   - Crear estructura clara:"
Write-Host "     plan_negocio/ (documentos finales)"
Write-Host "     scripts/ (scripts reutilizables)"
Write-Host "     data/ (configuraciones, datos)"
Write-Host "     _archive/ (histórico)"
Write-Host "     subagents/ (agentes especializados)"

# 5. RESUMEN
Write-Host "`n5. RESUMEN ACTUAL vs OBJETIVO:" -ForegroundColor Yellow

$currentStats = @{
    "Total archivos" = (Get-ChildItem -Recurse -File | Where-Object { $_.DirectoryName -notmatch "_archive" }).Count
    "Documentos .docx" = $docxFiles.Count
    "Scripts .py" = $pyFiles.Count
    "Scripts .md" = (Get-ChildItem -Recurse -Filter "*.md" -File | Where-Object { $_.DirectoryName -notmatch "_archive" }).Count
}

$targetStats = @{
    "Total archivos" = 100
    "Documentos .docx" = 20  # Solo versiones finales
    "Scripts .py" = 30      # Solo esenciales
    "Scripts .md" = 15      # Solo documentación
}

Write-Host "   ACTUAL:" -ForegroundColor Gray
foreach ($stat in $currentStats.GetEnumerator()) {
    Write-Host "   - $($stat.Key): $($stat.Value)"
}

Write-Host "`n   OBJETIVO:" -ForegroundColor Gray
foreach ($stat in $targetStats.GetEnumerator()) {
    Write-Host "   - $($stat.Key): $($stat.Value)"
}

Write-Host "`n   REDUCCIÓN NECESARIA:" -ForegroundColor Red
foreach ($key in $currentStats.Keys) {
    $reduction = $currentStats[$key] - $targetStats[$key]
    $percent = ($reduction / $currentStats[$key] * 100)
    Write-Host "   - $($key): $reduction archivos ($($percent.ToString('0.0'))%)"
}

Write-Host "`n=== FIN DEL ANÁLISIS ===" -ForegroundColor Cyan
Write-Host "¿Ejecutar limpieza automática? (Sí/No)" -ForegroundColor White