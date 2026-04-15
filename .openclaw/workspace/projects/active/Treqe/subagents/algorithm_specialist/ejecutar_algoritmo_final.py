#!/usr/bin/env python3
"""
Ejecutar algoritmo Treqe final combinado
"""

import sys
import os

# Combinar los dos archivos
def combine_files():
    """Combinar treqe_algorithm_final.py y treqe_algorithm_final_part2.py"""
    with open('treqe_algorithm_final.py', 'r', encoding='utf-8') as f1:
        content1 = f1.read()
    
    with open('treqe_algorithm_final_part2.py', 'r', encoding='utf-8') as f2:
        content2 = f2.read()
    
    # Encontrar donde termina el primer archivo (antes del main)
    end_marker = "def main():"
    idx = content1.find(end_marker)
    
    if idx != -1:
        combined = content1[:idx] + content2
    else:
        combined = content1 + "\n" + content2
    
    # Guardar archivo combinado
    with open('treqe_algorithm_completo.py', 'w', encoding='utf-8') as f:
        f.write(combined)
    
    return 'treqe_algorithm_completo.py'

# Ejecutar directamente
print("EJECUTANDO ALGORITMO TREQE FINAL")
print("="*70)

# Importar directamente desde los archivos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Intentar importar la clase
    from treqe_algorithm_final import TreqeAscendingAlgorithm
    
    print("✅ Algoritmo cargado correctamente")
    print("Ejecutando con 100 usuarios, timeout 300s, k_max=8...")
    print("-"*70)
    
    # Crear y ejecutar algoritmo
    algorithm = TreqeAscendingAlgorithm(time_budget_seconds=300, max_k=8)
    result = algorithm.run_ascending_algorithm(n_users=100)
    
    print("\n" + "="*70)
    print("RESUMEN EJECUTIVO:")
    print("="*70)
    
    print(f"• Usuarios procesados: {len(result['users'])}")
    print(f"• Usuarios emparejados: {len(result['matched_user_ids'])} ({result['coverage']:.1f}%)")
    print(f"• Tiempo total: {result['total_time']:.2f}s")
    print(f"• k máximo utilizado: {max(result['results_by_k'].keys()) if result['results_by_k'] else 0}")
    
    # Mostrar distribución por k
    print(f"\n• DISTRIBUCIÓN POR k:")
    for k, stats in result['execution_stats'].items():
        print(f"  k={k}: {stats['cycles_selected']} ciclos, {stats['users_matched']} usuarios")
    
    # Verificar viabilidad
    print(f"\n• VIABILIDAD:")
    if result['coverage'] >= 70:
        print("  ✅ VIABLE - Cobertura >70% alcanzada")
    elif result['coverage'] >= 50:
        print("  ⚠️  MARGINAL - Cobertura 50-70%, necesita optimización")
    else:
        print("  ❌ NO VIABLE - Cobertura <50%, revisar algoritmo")
    
    print(f"\n• RECOMENDACIÓN BATCH:")
    print(f"  • Ejecutar cada: 10 minutos")
    print(f"  • Timeout: 300 segundos")
    print(f"  • k máximo inicial: 8")
    print(f"  • Esperar cobertura: {result['coverage']:.1f}%")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nIntentando ejecución alternativa...")
    
    # Ejecutar directamente el código
    import subprocess
    result = subprocess.run([sys.executable, "treqe_algorithm_final_part2.py"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)