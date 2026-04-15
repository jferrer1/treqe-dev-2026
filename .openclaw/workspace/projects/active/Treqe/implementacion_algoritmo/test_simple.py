#!/usr/bin/env python3
"""
Test simple del algoritmo Treqe
"""

import sys
import os

# Añadir directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from treqe_algorithm_v1 import TreqeAscendingAlgorithm
    
    print("="*60)
    print("🧪 TEST SIMPLE - ALGORITMO TREQE")
    print("="*60)
    
    # Configuración de prueba rápida
    n_users = 30
    timeout = 30  # 30 segundos
    max_k = 6
    
    print(f"\n⚙️  Configuración:")
    print(f"  • Usuarios: {n_users}")
    print(f"  • Timeout: {timeout}s")
    print(f"  • k máximo: {max_k}")
    
    # Crear algoritmo
    print("\n🔧 Creando algoritmo...")
    algorithm = TreqeAscendingAlgorithm(time_budget_seconds=timeout, max_k=max_k)
    
    # Ejecutar (sin verbose para test simple)
    print("🚀 Ejecutando algoritmo...")
    result = algorithm.run_ascending_algorithm(n_users=n_users, verbose=False)
    
    print("\n" + "="*60)
    print("📊 RESULTADOS DEL TEST:")
    print("="*60)
    
    print(f"\n📈 MÉTRICAS PRINCIPALES:")
    print(f"  • Cobertura: {result['coverage']:.1f}%")
    print(f"  • Tiempo total: {result['total_time']:.2f}s")
    print(f"  • Densidad del grafo: {result['graph_density']:.2f}%")
    print(f"  • Usuarios emparejados: {len(result['matched_user_ids'])}/{n_users}")
    
    print(f"\n🎯 DISTRIBUCIÓN POR k:")
    if result['execution_stats']:
        for k in sorted(result['execution_stats'].keys()):
            stats = result['execution_stats'][k]
            print(f"  • k={k}: {stats['cycles_selected']} ciclos, {stats['users_matched']} usuarios")
    else:
        print("  • No se encontraron ciclos")
    
    print(f"\n✅ VIABILIDAD:")
    if result['coverage'] >= 70:
        print("  ✅ EXCELENTE - Cobertura >70%")
    elif result['coverage'] >= 50:
        print("  ⚠️  ACEPTABLE - Cobertura 50-70%")
    elif result['coverage'] >= 30:
        print("  📉 MARGINAL - Cobertura 30-50%")
    else:
        print("  ❌ BAJA - Cobertura <30%")
    
    print(f"\n💡 RECOMENDACIONES:")
    if result['coverage'] < 50:
        print("  1. Aumentar k máximo (ej: 8-10)")
        print("  2. Aumentar timeout (ej: 60-120s)")
        print("  3. Revisar densidad de preferencias")
    else:
        print("  1. El algoritmo funciona correctamente")
        print("  2. Considerar escalar a más usuarios")
        print("  3. Implementar en producción")
    
    print("\n" + "="*60)
    print("🧪 TEST COMPLETADO EXITOSAMENTE")
    print("="*60)
    
except ImportError as e:
    print(f"❌ Error importando: {e}")
    print("\nAsegúrate de que:")
    print("1. El archivo 'treqe_algorithm_v1.py' existe")
    print("2. Estás en el directorio correcto")
    print("3. Tienes Python 3.8+ instalado")
    
except Exception as e:
    print(f"❌ Error durante la ejecución: {e}")
    import traceback
    traceback.print_exc()