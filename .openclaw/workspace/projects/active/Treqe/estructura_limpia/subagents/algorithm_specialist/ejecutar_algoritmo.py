#!/usr/bin/env python3
"""
Ejecutar algoritmo Treqe final
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from algoritmo_treqe_final_sin_emojis import TreqeFinalAlgorithm, main
    print("Importacion exitosa. Ejecutando algoritmo...")
    main()
except Exception as e:
    print(f"Error: {e}")
    print("\nEjecutando directamente...")
    
    # Ejecutar directamente
    algorithm = TreqeFinalAlgorithm(n_users=100, avg_preferences=3, k_max=4)
    result = algorithm.run_final_matching()
    
    print("\nRESULTADOS CLAVE:")
    print(f"- Usuarios: {result['n_users']}")
    print(f"- Emparejados: {result['users_matched']} ({result['coverage']*100:.1f}%)")
    print(f"- Valor total: EUR{result['total_value']:.0f}")
    print(f"- Valor por usuario: EUR{result['value_per_user']:.0f}")
    print(f"- Tiempo: {result['total_time']:.3f}s")
    print(f"- k optimo: {result['best_k']}")