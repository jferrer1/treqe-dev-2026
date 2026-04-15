#!/usr/bin/env python3
"""
Ejecutar algoritmo Treqe de manera simple
"""

import sys
import os

# Añadir directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Intentar importar la clase directamente
try:
    # Primero necesitamos definir TreqeUser
    class TreqeUser:
        """Usuario de Treqe"""
        def __init__(self, user_id: int, offered_item: str, offered_value: float, 
                     wanted_items: list, wanted_values: list):
            self.id = user_id
            self.offered = {
                'item': offered_item,
                'value': offered_value,
                'owner': user_id
            }
            self.wanted = [
                {'item': item, 'value': value, 'owner': None}
                for item, value in zip(wanted_items, wanted_values)
            ]
            import random
            self.flexibility = random.uniform(0.3, 0.8)
            
        def __repr__(self):
            return f"User({self.id}, offers:{self.offered['item']}, wants:{len(self.wanted)} items)"
    
    # Ahora importar la clase principal
    from treqe_algorithm_final import TreqeAscendingAlgorithm
    
    print("✅ Algoritmo cargado correctamente")
    
    # Ejecutar algoritmo
    print("\n🚀 EJECUTANDO ALGORITMO ASCENDENTE K=2→K_MAX")
    print("="*70)
    
    algorithm = TreqeAscendingAlgorithm(time_budget_seconds=300, max_k=8)
    result = algorithm.run_ascending_algorithm(n_users=100)
    
    # Análisis de la estrategia
    print("\n" + "="*70)
    print("ANÁLISIS ESTRATEGIA ASCENDENTE:")
    print("="*70)
    
    total_users = 100
    matched_by_k = {}
    
    print("\nDISTRIBUCIÓN POR K:")
    print("-"*40)
    for k, cycles in result['results_by_k'].items():
        users_in_cycles = sum(len(cycle) for cycle in cycles)
        matched_by_k[k] = users_in_cycles
        print(f"k={k}: {len(cycles)} ciclos, {users_in_cycles} usuarios")
    
    total_matched = sum(matched_by_k.values())
    
    print(f"\nTOTAL EMPAREJADOS: {total_matched}/{total_users} ({result['coverage']:.1f}%)")
    print(f"TIEMPO TOTAL: {result['total_time']:.2f}s")
    print(f"K MÁXIMO ALCANZADO: {max(result['results_by_k'].keys()) if result['results_by_k'] else 0}")
    
    # Densidad del grafo
    total_possible_edges = total_users * (total_users - 1)
    actual_edges = sum(len(neighbors) for neighbors in result['graph'].values())
    density = actual_edges / total_possible_edges * 100
    
    print(f"\nDENSIDAD DEL MERCADO: {density:.2f}%")
    print(f"ARISTAS: {actual_edges}/{total_possible_edges}")
    
    # Mostrar eficiencia
    print("\nEFICIENCIA POR K:")
    print("-"*40)
    for k, stats in result['execution_stats'].items():
        if stats['cycles_selected'] > 0:
            avg_value = stats['total_value'] / stats['users_matched'] if stats['users_matched'] > 0 else 0
            print(f"k={k}: {stats['users_matched']} usuarios, €{stats['total_value']:.0f} valor, €{avg_value:.0f}/usuario")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    # Intentar ejecución alternativa
    print("\nIntentando ejecución alternativa...")
    try:
        # Ejecutar el script de ejecución
        import subprocess
        result = subprocess.run([sys.executable, "ejecutar_algoritmo_final.py"], 
                              capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print("Salida:", result.stdout)
    except Exception as e2:
        print(f"Error alternativo: {e2}")