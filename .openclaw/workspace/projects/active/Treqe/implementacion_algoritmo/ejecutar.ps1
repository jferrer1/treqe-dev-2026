# Script PowerShell para ejecutar el algoritmo Treqe
Write-Host "🚀 ALGORITMO TREQE - EJECUCIÓN EN WINDOWS" -ForegroundColor Green
Write-Host "=========================================="
Write-Host ""

# Verificar si Python está instalado
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    $pythonPath = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $pythonPath) {
    Write-Host "❌ ERROR: Python no encontrado" -ForegroundColor Red
    Write-Host "Por favor, instala Python 3.8 o superior desde: https://www.python.org/downloads/"
    exit 1
}

Write-Host "✅ Python encontrado: $($pythonPath.Source)" -ForegroundColor Green

# Verificar si los archivos existen
$algorithmFile = "treqe_algorithm_v1.py"
if (-not (Test-Path $algorithmFile)) {
    Write-Host "❌ ERROR: Archivo $algorithmFile no encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Archivo del algoritmo encontrado: $algorithmFile" -ForegroundColor Green
Write-Host ""

# Mostrar opciones
Write-Host "OPCIONES DE EJECUCIÓN:" -ForegroundColor Cyan
Write-Host "1. Ejecutar algoritmo completo (100 usuarios, 5 minutos)"
Write-Host "2. Ejecutar prueba rápida (50 usuarios, 1 minuto)"
Write-Host "3. Ejecutar con parámetros personalizados"
Write-Host ""

$choice = Read-Host "Selecciona una opción (1-3)"

switch ($choice) {
    "1" {
        Write-Host "`n🎯 EJECUTANDO ALGORITMO COMPLETO..." -ForegroundColor Yellow
        Write-Host "Usuarios: 100, Timeout: 300s, k máximo: 8"
        Write-Host ""
        
        & python $algorithmFile
    }
    "2" {
        Write-Host "`n⚡ EJECUTANDO PRUEBA RÁPIDA..." -ForegroundColor Yellow
        
        # Crear script de prueba rápida
        $quickTest = @"
#!/usr/bin/env python3
from treqe_algorithm_v1 import TreqeAscendingAlgorithm

print("⚡ PRUEBA RÁPIDA TREQE")
print("Usuarios: 50, Timeout: 60s, k máximo: 6")
print()

algorithm = TreqeAscendingAlgorithm(time_budget_seconds=60, max_k=6)
result = algorithm.run_ascending_algorithm(n_users=50, verbose=True)

print()
print("📊 RESUMEN PRUEBA RÁPIDA:")
print(f"Cobertura: {result['coverage']:.1f}%")
print(f"Tiempo: {result['total_time']:.2f}s")
print(f"Densidad grafo: {result['graph_density']:.2f}%")

if result['coverage'] >= 60:
    print("✅ PRUEBA EXITOSA")
else:
    print("⚠️  PRUEBA MARGINAL - Considerar ajustes")
"@
        
        $quickTest | Out-File -FilePath "prueba_rapida.py" -Encoding UTF8
        & python "prueba_rapida.py"
        
        # Limpiar
        Remove-Item "prueba_rapida.py" -ErrorAction SilentlyContinue
    }
    "3" {
        Write-Host "`n🔧 PARÁMETROS PERSONALIZADOS:" -ForegroundColor Yellow
        
        $n_users = Read-Host "Número de usuarios (default: 100)"
        $timeout = Read-Host "Timeout en segundos (default: 300)"
        $max_k = Read-Host "k máximo (default: 8)"
        
        # Validar entradas
        if (-not $n_users) { $n_users = 100 }
        if (-not $timeout) { $timeout = 300 }
        if (-not $max_k) { $max_k = 8 }
        
        $n_users = [int]$n_users
        $timeout = [int]$timeout
        $max_k = [int]$max_k
        
        Write-Host "`n🎯 EJECUTANDO CON PARÁMETROS PERSONALIZADOS..." -ForegroundColor Yellow
        Write-Host "Usuarios: $n_users, Timeout: ${timeout}s, k máximo: $max_k"
        Write-Host ""
        
        # Crear script personalizado
        $customScript = @"
#!/usr/bin/env python3
from treqe_algorithm_v1 import TreqeAscendingAlgorithm

print("🔧 ALGORITMO TREQE - PARÁMETROS PERSONALIZADOS")
print(f"Usuarios: $n_users, Timeout: ${timeout}s, k máximo: $max_k")
print()

algorithm = TreqeAscendingAlgorithm(time_budget_seconds=$timeout, max_k=$max_k)
result = algorithm.run_ascending_algorithm(n_users=$n_users, verbose=True)

print()
print("📊 RESUMEN PERSONALIZADO:")
print(f"Cobertura: {result['coverage']:.1f}%")
print(f"Tiempo: {result['total_time']:.2f}s")
print(f"Densidad grafo: {result['graph_density']:.2f}%")
print(f"k máximo utilizado: {max(result['results_by_k'].keys()) if result['results_by_k'] else 0}")

# Recomendación
if result['coverage'] >= 70:
    print("✅ RECOMENDACIÓN: VIABLE para producción")
elif result['coverage'] >= 50:
    print("⚠️  RECOMENDACIÓN: MARGINAL, necesita optimización")
else:
    print("❌ RECOMENDACIÓN: NO VIABLE, revisar algoritmo")
"@
        
        $customScript | Out-File -FilePath "algoritmo_personalizado.py" -Encoding UTF8
        & python "algoritmo_personalizado.py"
        
        # Limpiar
        Remove-Item "algoritmo_personalizado.py" -ErrorAction SilentlyContinue
    }
    default {
        Write-Host "❌ Opción no válida. Ejecutando configuración por defecto..." -ForegroundColor Red
        & python $algorithmFile
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "✅ EJECUCIÓN COMPLETADA" -ForegroundColor Green
Write-Host "Los resultados están arriba ↑" -ForegroundColor Yellow
Write-Host ""

# Preguntar si guardar resultados
$saveResults = Read-Host "¿Guardar resultados en archivo? (s/n)"
if ($saveResults -eq "s" -or $saveResults -eq "S") {
    $timestamp = Get-Date -Format "yyyy-MM-dd_HHmm"
    $outputFile = "resultados_treqe_$timestamp.txt"
    
    # Capturar salida y guardar
    & python $algorithmFile 2>&1 | Out-File -FilePath $outputFile -Encoding UTF8
    
    Write-Host "✅ Resultados guardados en: $outputFile" -ForegroundColor Green
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")