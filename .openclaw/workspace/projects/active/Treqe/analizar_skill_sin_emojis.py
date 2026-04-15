#!/usr/bin/env python3
"""
Analisis de self-improving-agent skill - version sin emojis
"""

import os
import json

def analizar_skill():
    print("=== ANALISIS DE SELF-IMPROVING-AGENT SKILL ===\n")
    
    skill_path = "skills/self-improving-agent"
    
    # 1. Verificar estructura basica
    print("1. ESTRUCTURA DE LA SKILL:")
    if os.path.exists(skill_path):
        print(f"   [OK] Skill encontrada en: {skill_path}")
        
        # Listar archivos clave
        archivos_clave = ["SKILL.md", "_meta.json", "handler.js", "handler.ts"]
        for archivo in archivos_clave:
            path = os.path.join(skill_path, archivo)
            if os.path.exists(path):
                print(f"   [OK] {archivo}")
            else:
                print(f"   [INFO] {archivo} (no encontrado)")
    
    # 2. Analizar compatibilidad con OpenClaw
    print("\n2. COMPATIBILIDAD CON OPENCLAW:")
    
    # Verificar workspace actual
    workspace_files = ["AGENTS.md", "SOUL.md", "TOOLS.md", "MEMORY.md"]
    for archivo in workspace_files:
        if os.path.exists(archivo):
            print(f"   [OK] {archivo} (presente en workspace)")
        else:
            print(f"   [INFO] {archivo} (no encontrado)")
    
    # 3. Verificar estructura .learnings requerida
    print("\n3. ESTRUCTURA .learnings REQUERIDA:")
    learnings_path = ".learnings"
    if os.path.exists(learnings_path):
        print(f"   [OK] {learnings_path} ya existe")
    else:
        print(f"   [INFO] {learnings_path} necesita crearse")
        
        # Verificar archivos de ejemplo en assets
        assets_path = os.path.join(skill_path, "assets")
        if os.path.exists(assets_path):
            print(f"   [OK] Templates disponibles en {assets_path}")
            
            # Listar templates
            for item in os.listdir(assets_path):
                if item.endswith('.md'):
                    print(f"     * {item}")
    
    # 4. Analizar funcionalidad
    print("\n4. FUNCIONALIDAD OFRECIDA:")
    
    funcionalidades = [
        "Log de errores y correcciones",
        "Deteccion de patrones recurrentes", 
        "Promocion de aprendizajes a memoria permanente",
        "Integracion con hooks de OpenClaw",
        "Extraccion de skills a partir de aprendizajes",
        "Comunicacion inter-sesion"
    ]
    
    for func in funcionalidades:
        print(f"   [OK] {func}")
    
    # 5. Analizar conveniencia para mis problemas actuales
    print("\n5. CONVENIENCIA PARA MIS PROBLEMAS ACTUALES:")
    
    mis_problemas = [
        "Sesgo del solucionador compulsivo (sobre-escribir trabajo existente)",
        "Creacion de multiples versiones innecesarias",
        "Falta de validacion antes de modificar",
        "No respetar trabajo ya bien hecho",
        "Ineficiencia por trabajo duplicado"
    ]
    
    beneficios_esperados = [
        "Deteccion temprana de patrones problematicos",
        "Log estructurado de errores para analisis",
        "Creacion de protocolos de mejora",
        "Auto-evaluacion durante ejecucion",
        "Aprendizaje sistematico de mejores practicas"
    ]
    
    print("   MIS PROBLEMAS IDENTIFICADOS:")
    for problema in mis_problemas:
        print(f"     * {problema}")
    
    print("\n   BENEFICIOS ESPERADOS DE LA SKILL:")
    for beneficio in beneficios_esperados:
        print(f"     * {beneficio}")
    
    # 6. Verificar requisitos de instalacion
    print("\n6. REQUISITOS DE INSTALACION:")
    
    # Segun SKILL.md, necesita:
    requisitos = [
        "Crear directorio .learnings/ en workspace",
        "Copiar templates de assets/ a .learnings/",
        "Configurar hooks (opcional pero recomendado)",
        "Integrar con archivos workspace existentes"
    ]
    
    for req in requisitos:
        print(f"   * {req}")
    
    # 7. Determinar si es conveniente
    print("\n7. CONCLUSION: ¿ES CONVENIENTE UTILIZARLA?")
    
    pros = [
        "Resuelve exactamente mis problemas de aprendizaje",
        "Es compatible con OpenClaw (disenada para el)",
        "Proporciona framework sistematico para mejora",
        "Permite deteccion temprana de patrones problematicos",
        "Facilita comunicacion de aprendizajes entre sesiones"
    ]
    
    contras = [
        "Requiere configuracion inicial",
        "Anade overhead a cada interaccion",
        "Necesita disciplina para mantener actualizado"
    ]
    
    print("   PROS:")
    for pro in pros:
        print(f"     [OK] {pro}")
    
    print("\n   CONTRAS:")
    for contra in contras:
        print(f"     [INFO] {contra}")
    
    print("\n8. RECOMENDACION FINAL:")
    print("   [RECOMENDADO] ALTAMENTE RECOMENDADA")
    print()
    print("   RAZONES:")
    print("   1. Mis problemas actuales son EXACTAMENTE lo que esta skill resuelve")
    print("   2. Esta disenada especificamente para OpenClaw")
    print("   3. Proporciona mejora continua estructurada")
    print("   4. Los beneficios superan ampliamente el costo de configuracion")
    print("   5. Mejoraria significativamente mi capacidad para ayudarte")
    
    return True

if __name__ == "__main__":
    analizar_skill()