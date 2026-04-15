#!/usr/bin/env python3
"""
Análisis de la skill self-improving-agent para determinar conveniencia y compatibilidad
"""

import os
import json

def analizar_skill():
    print("=== ANÁLISIS DE SELF-IMPROVING-AGENT SKILL ===\n")
    
    skill_path = "skills/self-improving-agent"
    
    # 1. Verificar estructura básica
    print("1. ESTRUCTURA DE LA SKILL:")
    if os.path.exists(skill_path):
        print(f"   ✅ Skill encontrada en: {skill_path}")
        
        # Listar archivos clave
        archivos_clave = ["SKILL.md", "_meta.json", "handler.js", "handler.ts"]
        for archivo in archivos_clave:
            path = os.path.join(skill_path, archivo)
            if os.path.exists(path):
                print(f"   ✅ {archivo}")
            else:
                print(f"   ⚠️  {archivo} (no encontrado)")
    
    # 2. Analizar compatibilidad con OpenClaw
    print("\n2. COMPATIBILIDAD CON OPENCLAW:")
    
    # Verificar workspace actual
    workspace_files = ["AGENTS.md", "SOUL.md", "TOOLS.md", "MEMORY.md"]
    for archivo in workspace_files:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo} (presente en workspace)")
        else:
            print(f"   ⚠️  {archivo} (no encontrado)")
    
    # 3. Verificar estructura .learnings requerida
    print("\n3. ESTRUCTURA .learnings REQUERIDA:")
    learnings_path = ".learnings"
    if os.path.exists(learnings_path):
        print(f"   ✅ {learnings_path} ya existe")
    else:
        print(f"   ⚠️  {learnings_path} necesita crearse")
        
        # Verificar archivos de ejemplo en assets
        assets_path = os.path.join(skill_path, "assets")
        if os.path.exists(assets_path):
            print(f"   ✅ Templates disponibles en {assets_path}")
            
            # Listar templates
            for item in os.listdir(assets_path):
                if item.endswith('.md'):
                    print(f"     • {item}")
    
    # 4. Analizar funcionalidad
    print("\n4. FUNCIONALIDAD OFRECIDA:")
    
    funcionalidades = [
        "Log de errores y correcciones",
        "Detección de patrones recurrentes", 
        "Promoción de aprendizajes a memoria permanente",
        "Integración con hooks de OpenClaw",
        "Extracción de skills a partir de aprendizajes",
        "Comunicación inter-sesión"
    ]
    
    for func in funcionalidades:
        print(f"   ✅ {func}")
    
    # 5. Analizar conveniencia para mis problemas actuales
    print("\n5. CONVENIENCIA PARA MIS PROBLEMAS ACTUALES:")
    
    mis_problemas = [
        "Sesgo del solucionador compulsivo (sobre-escribir trabajo existente)",
        "Creación de múltiples versiones innecesarias",
        "Falta de validación antes de modificar",
        "No respetar trabajo ya bien hecho",
        "Ineficiencia por trabajo duplicado"
    ]
    
    beneficios_esperados = [
        "Detección temprana de patrones problemáticos",
        "Log estructurado de errores para análisis",
        "Creación de protocolos de mejora",
        "Auto-evaluación durante ejecución",
        "Aprendizaje sistemático de mejores prácticas"
    ]
    
    print("   MIS PROBLEMAS IDENTIFICADOS:")
    for problema in mis_problemas:
        print(f"     • {problema}")
    
    print("\n   BENEFICIOS ESPERADOS DE LA SKILL:")
    for beneficio in beneficios_esperados:
        print(f"     • {beneficio}")
    
    # 6. Verificar requisitos de instalación
    print("\n6. REQUISITOS DE INSTALACIÓN:")
    
    # Según SKILL.md, necesita:
    requisitos = [
        "Crear directorio .learnings/ en workspace",
        "Copiar templates de assets/ a .learnings/",
        "Configurar hooks (opcional pero recomendado)",
        "Integrar con archivos workspace existentes"
    ]
    
    for req in requisitos:
        print(f"   • {req}")
    
    # 7. Determinar si es conveniente
    print("\n7. CONCLUSIÓN: ¿ES CONVENIENTE UTILIZARLA?")
    
    pros = [
        "Resuelve exactamente mis problemas de aprendizaje",
        "Es compatible con OpenClaw (diseñada para él)",
        "Proporciona framework sistemático para mejora",
        "Permite detección temprana de patrones problemáticos",
        "Facilita comunicación de aprendizajes entre sesiones"
    ]
    
    contras = [
        "Requiere configuración inicial",
        "Añade overhead a cada interacción",
        "Necesita disciplina para mantener actualizado"
    ]
    
    print("   PROS:")
    for pro in pros:
        print(f"     ✅ {pro}")
    
    print("\n   CONTRAS:")
    for contra in contras:
        print(f"     ⚠️  {contra}")
    
    print("\n8. RECOMENDACIÓN FINAL:")
    print("   ⭐⭐⭐⭐⭐ ALTAMENTE RECOMENDADA")
    print()
    print("   RAZONES:")
    print("   1. Mis problemas actuales son EXACTAMENTE lo que esta skill resuelve")
    print("   2. Está diseñada específicamente para OpenClaw")
    print("   3. Proporciona mejora continua estructurada")
    print("   4. Los beneficios superan ampliamente el costo de configuración")
    print("   5. Mejoraría significativamente mi capacidad para ayudarte")
    
    return True

if __name__ == "__main__":
    analizar_skill()