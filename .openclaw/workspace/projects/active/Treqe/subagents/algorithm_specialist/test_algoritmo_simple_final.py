#!/usr/bin/env python3
"""
Test simple del algoritmo Treqe final (sin emojis)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from treqe_algorithm_final import TreqeAscendingAlgorithm
    
    print("ALGORITMO TREQE FINAL - TEST")
    print("="*70)
    
    # Configurar algoritmo
    algorithm = TreqeAscendingAlgorithm(time_budget_seconds=300, max_k=8)
    
    # Ejecutar con 100 usuarios
    print("Ejecutando con 100 usuarios...")
    result = algorithm.run_ascending_algorithm(n_users=100)
    
    # Mostrar resultados
    print("\nRESULTADOS:")
    print("-"*40)
    print(f"Usuarios totales: {len(result['users'])}")
    print(f"Usuarios emparejados: {len(result['matched_user_ids'])}")
    print(f"Cobertura: {result['coverage']:.1f}%")
    print(f"Tiempo total: {result['total_time']:.2f}s")
    
    if result['results_by_k']:
        max_k = max(result['results_by_k'].keys())
        print(f"k maximo utilizado: {max_k}")
    
    # Distribucion por k
    print("\nDISTRIBUCION POR k:")
    print("-"*40)
    for k in sorted(result['execution_stats'].keys()):
        stats = result['execution_stats'][k]
        if 'users_matched' in stats:
            print(f"k={k}: {stats['cycles_selected']} ciclos, {stats['users_matched']} usuarios")
        else:
            print(f"k={k}: {stats['cycles_selected']} ciclos, 0 usuarios")
    
    # Verificacion
    print("\nVERIFICACION:")
    print("-"*40)
    if result['coverage'] >= 70:
        print("OK - Cobertura >70% (viable)")
    elif result['coverage'] >= 50:
        print("ALERTA - Cobertura 50-70% (necesita optimizacion)")
    else:
        print("PROBLEMA - Cobertura <50% (no viable)")
    
    # Recomendaciones
    print("\nRECOMENDACIONES BATCH:")
    print("-"*40)
    print("• Ejecutar cada: 10 minutos")
    print("• Timeout algoritmo: 300 segundos")
    print("• k maximo inicial: 8")
    
    print("\n" + "="*70)
    print("TEST COMPLETADO")
    print("="*70)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()