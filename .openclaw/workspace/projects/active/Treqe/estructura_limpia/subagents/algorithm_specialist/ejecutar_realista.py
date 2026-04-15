#!/usr/bin/env python3
"""
Ejecutar análisis realista
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algoritmo_realista_5porciento import TreqeRealisticAlgorithm

print("ANALISIS REALISTA TREQE - DENSIDAD 5%")
print("="*70)

# Ejecutar con densidad REAL (5%)
algo = TreqeRealisticAlgorithm(n_users=100, density=0.05, avg_preferences=2, k_max=6)
result = algo.run_realistic_analysis()

if result:
    print("\n" + "="*70)
    print("RESUMEN EJECUTIVO:")
    print("="*70)
    
    print(f"\nCON DENSIDAD 5% (mercado actual):")
    print(f"  • Usuarios emparejados: {result['users_matched']}/{result['n_users']}")
    print(f"  • Cobertura: {result['coverage']*100:.1f}%")
    print(f"  • k optimo: {result['best_k']}")
    
    if result['best_k']:
        print(f"\nINTERPRETACION:")
        if result['best_k'] <= 3:
            print("  ❌ TREQE NO ES VIABLE")
            print("     k optimo <= 3 no justifica complejidad")
        elif result['best_k'] == 4:
            print("  ⚠️  TREQE MARGINALMENTE VIABLE")
            print("     k=4 mejora cobertura pero complejidad alta")
        elif result['best_k'] >= 5:
            print("  ✅ TREQE ES VIABLE")
            print(f"     k={result['best_k']} necesario para cobertura aceptable")
    
    # Mostrar distribución de ciclos
    print(f"\nDISTRIBUCION DE CICLOS ENCONTRADOS:")
    for k, count in result['cycles_by_k'].items():
        print(f"  k={k}: {count} ciclos")
    
    # Valor esperado vs realidad
    print(f"\nVALOR ESPERADO vs REALIDAD:")
    print(f"  • Mercado actual (k=2): <5% cobertura")
    print(f"  • Treqe (k optimo={result['best_k']}): {result['coverage']*100:.1f}% cobertura")
    
    if result['coverage'] > 0.05:
        improvement = result['coverage'] / 0.05
        print(f"  • MEJORA: {improvement:.1f}x más usuarios emparejados")
    else:
        print(f"  • MEJORA: Ninguna (Treqe no funciona)")