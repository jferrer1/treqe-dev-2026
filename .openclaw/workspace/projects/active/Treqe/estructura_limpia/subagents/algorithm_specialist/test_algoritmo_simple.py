#!/usr/bin/env python3
"""
Test simple del algoritmo Treqe optimizado
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algoritmo_treqe_optimizado_final import TreqeOptimizedAlgorithm

def main():
    print("TEST ALGORITMO TREQE OPTIMIZADO")
    print("="*70)
    
    # Ejecutar algoritmo con 100 usuarios
    algo = TreqeOptimizedAlgorithm(n_users=100, avg_preferences=3, k_max=4)
    result = algo.run_optimized_matching()
    
    print("\n" + "="*70)
    print("RESUMEN RAPIDO:")
    print("="*70)
    print(f"Usuarios: {result['n_users']}")
    print(f"Emparejados: {result['users_matched']} ({result['coverage']*100:.1f}%)")
    print(f"Valor total: EUR{result['total_value']:.0f}")
    print(f"Valor por usuario: EUR{result['value_per_user']:.0f}")
    print(f"Tiempo: {result['total_time']:.3f}s")
    print(f"k optimo: {result['best_k']}")
    
    # Mostrar algunos ciclos encontrados
    print("\nEJEMPLOS DE CICLOS ENCONTRADOS:")
    print("-"*40)
    selected = result['selected_cycles']
    for i, cycle_data in enumerate(selected[:3]):  # Mostrar primeros 3
        cycle = cycle_data['cycle']
        k = cycle_data['k']
        value = cycle_data['value']
        print(f"Ciclo {i+1} (k={k}, EUR{value:.0f}): {cycle}")
    
    print("\n" + "="*70)
    print("ESTADISTICAS POR k:")
    print("="*70)
    for k in range(2, 5):
        cycles_k = [c for c in selected if c['k'] == k]
        if cycles_k:
            total_value = sum(c['value'] for c in cycles_k)
            total_users = sum(len(c['cycle']) for c in cycles_k)
            print(f"k={k}: {len(cycles_k)} ciclos, {total_users} usuarios, EUR{total_value:.0f} valor")
    
    print("\n" + "="*70)
    print("VEREDICTO FINAL:")
    print("="*70)
    
    coverage = result['coverage']
    value_per_user = result['value_per_user']
    total_time = result['total_time']
    best_k = result['best_k']
    
    if coverage >= 0.5 and value_per_user >= 100 and total_time < 5:
        print("✅ ALGORITMO OPTIMIZADO - LISTO PARA PRODUCCION")
        print(f"   • Cobertura: {coverage*100:.1f}% (>=50%)")
        print(f"   • Valor/usuario: EUR{value_per_user:.0f} (>=100)")
        print(f"   • Tiempo: {total_time:.3f}s (<5s)")
        print(f"   • k optimo: {best_k}")
    else:
        print("⚠️  ALGORITMO NECESITA OPTIMIZACION")
        if coverage < 0.5:
            print(f"   • Cobertura baja: {coverage*100:.1f}%")
        if value_per_user < 100:
            print(f"   • Valor/usuario bajo: EUR{value_per_user:.0f}")
        if total_time >= 5:
            print(f"   • Tiempo alto: {total_time:.3f}s")
    
    print("\n" + "="*70)
    print("✅ TEST COMPLETADO")
    print("="*70)

if __name__ == "__main__":
    main()