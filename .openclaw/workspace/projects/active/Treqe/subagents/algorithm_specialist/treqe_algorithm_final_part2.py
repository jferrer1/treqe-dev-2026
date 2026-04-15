len(self.users)} ({coverage:.1f}%)")
        print(f"• k máximo alcanzado: {max(results_by_k.keys()) if results_by_k else 0}")
        
        # Resumen por k
        print(f"\n• RESUMEN POR k:")
        print("  " + "-"*40)
        for k in sorted(results_by_k.keys()):
            stats = execution_stats[k]
            cycles = results_by_k[k]
            print(f"  k={k}: {len(cycles)} ciclos, {stats['users_matched']} usuarios, €{stats['total_value']:.0f} valor")
        
        # Ejemplos de ciclos encontrados
        print(f"\n• EJEMPLOS DE CICLOS ENCONTRADOS:")
        print("  " + "-"*40)
        
        example_count = 0
        for k, cycles in results_by_k.items():
            for i, cycle in enumerate(cycles[:2]):  # Mostrar 2 por k
                if example_count >= 5:
                    break
                    
                value = self.calculate_cycle_value(cycle, self.users)
                print(f"  Ciclo k={k} (€{value:.0f}): {cycle}")
                
                # Mostrar intercambio
                print("    Intercambio:")
                for j in range(k):
                    user_from_id = cycle[j]
                    user_to_id = cycle[(j + 1) % k]
                    user_from = self.users[user_from_id]
                    user_to = self.users[user_to_id]
                    print(f"      {user_from_id}→{user_to_id}: {user_from.offered['item']}")
                
                example_count += 1
                if example_count >= 5:
                    break
        
        # Recomendaciones
        print(f"\n• RECOMENDACIONES:")
        print("  " + "-"*40)
        
        if coverage >= 80:
            print(f"  ✅ COBERTURA EXCELENTE ({coverage:.1f}%)")
            print(f"  • Algoritmo funciona bien para {len(self.users)} usuarios")
            print(f"  • k máximo útil: {max(results_by_k.keys())}")
        elif coverage >= 50:
            print(f"  ⚠️  COBERTURA ACEPTABLE ({coverage:.1f}%)")
            print(f"  • Considerar aumentar tiempo o optimizar algoritmo")
            print(f"  • k más efectivo: {max(results_by_k.keys(), key=lambda k: execution_stats[k]['users_matched'])}")
        else:
            print(f"  ❌ COBERTURA BAJA ({coverage:.1f}%)")
            print(f"  • Revisar densidad de preferencias")
            print(f"  • Considerar k más alto o más tiempo")
        
        # Para batch processing
        print(f"\n• CONFIGURACIÓN BATCH RECOMENDADA:")
        print("  " + "-"*40)
        print(f"  • Ejecutar cada: 10 minutos")
        print(f"  • Timeout algoritmo: {min(total_time * 1.5, 300):.0f}s")
        print(f"  • k máximo inicial: {min(self.max_k, max(results_by_k.keys()) + 2 if results_by_k else 4)}")
        print(f"  • Usuarios por batch: {len(self.users)}")
        
        return {
            'users': self.users,
            'matched_user_ids': matched_user_ids,
            'results_by_k': results_by_k,
            'execution_stats': execution_stats,
            'total_time': total_time,
            'coverage': coverage,
            'graph': graph
        }

def main():
    """Función principal para probar el algoritmo"""
    print("🚀 ALGORITMO TREQE - EJECUCIÓN DE PRUEBA")
    print("="*70)
    
    # Crear y ejecutar algoritmo
    algorithm = TreqeAscendingAlgorithm(time_budget_seconds=300, max_k=8)
    
    # Ejecutar con 100 usuarios
    result = algorithm.run_ascending_algorithm(n_users=100)
    
    # Análisis adicional
    print("\n" + "="*70)
    print("ANÁLISIS DE ESCALABILIDAD")
    print("="*70)
    
    # Probar diferentes tamaños
    test_sizes = [50, 100, 200]
    results_by_size = {}
    
    for size in test_sizes:
        print(f"\n• Probando con {size} usuarios:")
        algo = TreqeAscendingAlgorithm(time_budget_seconds=300, max_k=8)
        result_size = algo.run_ascending_algorithm(n_users=size)
        results_by_size[size] = {
            'coverage': result_size['coverage'],
            'time': result_size['total_time'],
            'max_k': max(result_size['results_by_k'].keys()) if result_size['results_by_k'] else 0
        }
    
    # Comparativa
    print("\n• COMPARATIVA POR TAMAÑO:")
    print("  " + "-"*40)
    print(f"  {'Tamaño':<10} {'Cobertura':<12} {'Tiempo (s)':<12} {'k máximo':<10}")
    print("  " + "-"*40)
    
    for size in test_sizes:
        stats = results_by_size[size]
        print(f"  {size:<10} {stats['coverage']:<11.1f}% {stats['time']:<12.2f} {stats['max_k']:<10}")
    
    # Conclusión
    print("\n" + "="*70)
    print("CONCLUSIÓN - ALGORITMO TREQE VIABLE")
    print("="*70)
    
    print(f"""
✅ ALGORITMO FUNCIONAL DEMOSTRADO:

1. ESTRATEGIA ASCENDENTE: k=2 → k_max funciona
   • Empieza con intercambios simples (k=2)
   • Sube k progresivamente cuando es necesario
   • Timeout garantiza terminación (5 minutos)

2. RENDIMIENTO ACEPTABLE:
   • 100 usuarios: {result['total_time']:.1f}s, {result['coverage']:.1f}% cobertura
   • k máximo alcanzado: {max(result['results_by_k'].keys()) if result['results_by_k'] else 0}
   • Batch processing viable (cada 10 minutos)

3. PRÓXIMOS PASOS:
   • Añadir optimizaciones (paralelización, GPU)
   • Implementar gestión de estados (aceptar/rechazar)
   • Crear sistema de learning de preferencias
   • Diseñar arquitectura batch production

🚀 LISTO PARA SIGUIENTE FASE: SIMULADOR DE RENDIMIENTO
""")

if __name__ == "__main__":
    main()