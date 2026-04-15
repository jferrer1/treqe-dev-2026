acion:
        print(f"  • {item:15} ({k:4}): {timeline:20} - {notas}")
    
    print("\n📈 MÉTRICAS DE DECISIÓN:")
    
    metricas = [
        ("Tasa matching", ">40% usuarios emparejados", "k=3 óptimo, k=4 aceptable"),
        ("Tiempo ejecución", "<5s para 1000 usuarios", "k≤4 viable, k≥5 problemático"),
        ("Satisfacción", ">70% usuarios satisfechos", "k=3 ideal, k=4 bueno, k≥5 baja"),
        ("Valor intercambiado", "Maximizar EUR/usuario", "k=3-4 mejor balance"),
        ("Riesgo operacional", "Minimizar fallos envío", "k≤4 manejable, k≥5 alto"),
    ]
    
    for metrica, objetivo, implicacion in metricas:
        print(f"  • {metrica:20}: {objetivo:30} → {implicacion}")
    
    print("\n🔧 CONFIGURACIÓN RECOMENDADA PARA MVP:")
    
    config_mvp = {
        "max_rueda_size": 3,
        "algoritmo": "enhanced_matching (circular k=3)",
        "complejidad": "O(n³) - manejable para <1000 usuarios",
        "tiempo_max": "1s para 100 usuarios, 10s para 1000 usuarios",
        "cobertura": "100% búsqueda exhaustiva para k=2-3",
        "fallback": "Si no hay ruedas k=3, buscar k=2",
        "limites": "No buscar k=4+ en MVP (complejidad explosiva)",
    }
    
    for clave, valor in config_mvp.items():
        print(f"  {clave:20}: {valor}")
    
    print("\n🚀 ESTRATEGIA DE ESCALABILIDAD:")
    
    estrategia = [
        ("Corto plazo (0-6m)", "k=2-3 exacto", "100% calidad, escala media"),
        ("Medio plazo (6-18m)", "k=4 heurístico", "80-90% calidad, buena escala"),
        ("Largo plazo (18-36m)", "k=5-6 aproximado", "60-80% calidad, alta escala"),
        ("Muy largo plazo (36m+)", "k=2-8 híbrido", "Calidad variable, escala masiva"),
    ]
    
    print("  Plazo | Enfoque | Calidad | Escalabilidad")
    print("  " + "-"*60)
    for plazo, enfoque, calidad, escala in estrategia:
        print(f"  {plazo:18} | {enfoque:12} | {calidad:8} | {escala}")
    
    print("\n⚠️ ADVERTENCIAS CRÍTICAS:")
    
    advertencias = [
        "NO intentar k≥5 en MVP → complejidad explosiva",
        "k=4 requiere heurísticas → pérdida de optimalidad",
        "Cada +1 en k multiplica complejidad por n",
        "Ruedas grandes = mayor riesgo logístico",
        "Usuarios normales no entienden ruedas >4 personas",
    ]
    
    for i, adv in enumerate(advertencias, 1):
        print(f"  {i}. {adv}")
    
    print("\n✅ CONCLUSIÓN FINAL:")
    print("  Para MVP: k=3 máximo (óptimo balance valor/complejidad)")
    print("  Para crecimiento: k=4 con heurísticas")
    print("  Para escala: k=5-6 con aproximaciones/ML")
    print("  Nunca: k≥7 (impráctico computacional y operacionalmente)")
    
    print("\n" + "="*80)
    print("ANÁLISIS COMPLETADO - RESUMEN EJECUTIVO")
    print("="*80)
    
    # Guardar análisis en archivo
    analisis_completo = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "resumen": {
            "max_recomendado_mvp": 3,
            "max_recomendado_crecimiento": 4,
            "max_recomendado_escala": 6,
            "max_impráctico": 7,
            "complejidad_base": "O(n³) para k=3",
            "viabilidad_tecnica": "k≤4 viable, k≥5 requiere aproximaciones"
        },
        "analisis_detallado": {
            "computacional": "Crecimiento factorial con k",
            "operacional": "Logística más compleja con k grande",
            "usuario": "Experiencia empeora con k>4",
            "valor": "Rendimientos decrecientes después de k=4"
        },
        "recomendaciones": {
            "mvp": "k=2-3 exacto, no buscar k≥4",
            "crecimiento": "k=4 con heurísticas greedy",
            "escala": "k=5-6 con ML y aproximaciones",
            "arquitectura": "Sistema híbrido adaptable"
        }
    }
    
    with open("rueda_escalabilidad_analisis.json", "w") as f:
        json.dump(analisis_completo, f, indent=2)
    
    print(f"\nAnálisis detallado guardado en: rueda_escalabilidad_analisis.json")

# ========== EJECUCIÓN PRINCIPAL ==========

def main():
    """Función principal de ejecución"""
    print("\nANÁLISIS DE ESCALABILIDAD DE RUEDAS DE INTERCAMBIO")
    print("Respuesta a: ¿Cuán grande se puede hacer la rueda?")
    print(f"Inicio: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    try:
        # Ejecutar todos los análisis
        analizar_complejidad_computacional()
        analizar_viabilidad_practica()
        analizar_impacto_en_valor()
        analizar_escalabilidad_algoritmo()
        proponer_arquitectura_escalable()
        simular_rendimiento_real()
        generar_recomendaciones_finales()
        
        print(f"\nAnálisis completado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Mostrar respuesta directa a la pregunta
        print("\n" + "="*80)
        print("RESPUESTA DIRECTA A LA PREGUNTA:")
        print("="*80)
        
        print("\n❓ ¿Cuán grande se puede hacer la rueda de intercambio?")
        print("\n📊 RESPUESTA POR FASE:")
        
        respuestas = [
            ("MVP (0-6 meses)", "MÁXIMO 3 usuarios", "Óptimo balance valor/complejidad"),
            ("Crecimiento (6-18 meses)", "MÁXIMO 4 usuarios", "Con heurísticas optimizadas"),
            ("Escala (18-36 meses)", "MÁXIMO 5-6 usuarios", "Con ML y aproximaciones"),
            ("Límite absoluto", "MÁXIMO 6-7 usuarios", "Impráctico más allá"),
        ]
        
        for fase, maximo, explicacion in respuestas:
            print(f"  • {fase:20}: {maximo:15} → {explicacion}")
        
        print("\n🎯 RECOMENDACIÓN INMEDIATA PARA TREQE:")
        print("  Comenzar con ruedas de 2-3 usuarios en MVP")
        print("  No intentar ruedas de 4+ hasta fase de crecimiento")
        print("  Nunca planear ruedas de 7+ usuarios (impráctico)")
        
        print("\n🔧 RAZONES TÉCNICAS:")
        razones = [
            "1. Complejidad computacional factorial (NP-Completo)",
            "2. Logística exponencialmente más compleja",
            "3. Riesgo operacional multiplicado",
            "4. Experiencia usuario deteriorada",
            "5. Rendimientos decrecientes de valor",
        ]
        
        for razon in razones:
            print(f"  {razon}")
        
        return True
        
    except Exception as e:
        print(f"\nERROR en análisis: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)