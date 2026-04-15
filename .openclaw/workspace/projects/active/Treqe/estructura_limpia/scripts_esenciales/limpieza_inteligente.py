#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sistema de limpieza inteligente para Treqe

import os
import shutil
from datetime import datetime, timedelta
import hashlib

print("=== SISTEMA DE LIMPIEZA INTELIGENTE TREQE ===")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Configuración
BASE_DIR = "."
ARCHIVE_DIR = "_archive/limpieza_2026-02-27"
KEEP_DAYS = 7  # Mantener scripts de los últimos 7 días

# Crear directorio de archivo si no existe
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Reglas de limpieza
RULES = {
    "scripts_temporales": {
        "patterns": [
            "crear_", "generar_", "actualizar_", "corregir_",
            "humanizar_", "completar_", "integrar_", "reescribir_",
            "convertir_", "mejorar_", "anadir_", "aplicar_"
        ],
        "action": "archive",  # archive, delete, keep
        "min_age_days": 1  # Archivar si >1 día
    },
    "documentos_duplicados": {
        "patterns": [".docx"],
        "action": "analyze_duplicates",
        "keep_latest": True
    },
    "backups_antiguos": {
        "patterns": [".backup", "_backup", "_old", "_v1", "_v2"],
        "action": "archive",
        "min_age_days": 3
    }
}

def get_file_hash(filepath):
    """Calcular hash MD5 de un archivo"""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def analyze_files():
    """Analizar todos los archivos y clasificarlos"""
    print("1. ANALIZANDO ARCHIVOS...")
    
    all_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # Excluir directorios de archivo y system
        dirs[:] = [d for d in dirs if not d.startswith('_archive') and d != '__pycache__']
        
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, BASE_DIR)
            
            # Obtener estadísticas
            stat = os.stat(filepath)
            age_days = (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).days
            size_kb = stat.st_size / 1024
            
            file_info = {
                'path': filepath,
                'rel_path': rel_path,
                'name': file,
                'ext': os.path.splitext(file)[1].lower(),
                'size_kb': size_kb,
                'age_days': age_days,
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'hash': get_file_hash(filepath) if size_kb < 1024 else "large"  # Solo hash archivos pequeños
            }
            
            all_files.append(file_info)
    
    print(f"   Total archivos encontrados: {len(all_files)}")
    return all_files

def classify_files(files):
    """Clasificar archivos según reglas"""
    print("\n2. CLASIFICANDO ARCHIVOS...")
    
    classified = {
        'scripts_temporales': [],
        'documentos_duplicados': [],
        'backups_antiguos': [],
        'keep': []
    }
    
    # Primero identificar documentos duplicados
    docx_files = [f for f in files if f['ext'] == '.docx']
    doc_hashes = {}
    
    for doc in docx_files:
        # Simplificación: usar nombre y tamaño para identificar duplicados
        key = f"{doc['name']}_{doc['size_kb']:.0f}"
        if key in doc_hashes:
            doc_hashes[key].append(doc)
        else:
            doc_hashes[key] = [doc]
    
    # Clasificar cada archivo
    for file in files:
        classified_flag = False
        
        # Regla 1: Scripts temporales
        if file['ext'] == '.py':
            for pattern in RULES['scripts_temporales']['patterns']:
                if pattern in file['name'].lower():
                    if file['age_days'] > RULES['scripts_temporales']['min_age_days']:
                        classified['scripts_temporales'].append(file)
                        classified_flag = True
                        break
        
        # Regla 2: Documentos duplicados
        if file['ext'] == '.docx':
            key = f"{file['name']}_{file['size_kb']:.0f}"
            if key in doc_hashes and len(doc_hashes[key]) > 1:
                # Ordenar por fecha (más reciente primero)
                duplicates = sorted(doc_hashes[key], key=lambda x: x['modified'], reverse=True)
                if file['path'] != duplicates[0]['path']:  # No es el más reciente
                    classified['documentos_duplicados'].append(file)
                    classified_flag = True
        
        # Regla 3: Backups antiguos
        if not classified_flag:
            for pattern in RULES['backups_antiguos']['patterns']:
                if pattern in file['name'].lower():
                    if file['age_days'] > RULES['backups_antiguos']['min_age_days']:
                        classified['backups_antiguos'].append(file)
                        classified_flag = True
                        break
        
        # Si no cumple ninguna regla, mantener
        if not classified_flag:
            classified['keep'].append(file)
    
    # Estadísticas
    print(f"   Scripts temporales: {len(classified['scripts_temporales'])}")
    print(f"   Documentos duplicados: {len(classified['documentos_duplicados'])}")
    print(f"   Backups antiguos: {len(classified['backups_antiguos'])}")
    print(f"   Archivos a mantener: {len(classified['keep'])}")
    
    return classified

def execute_cleanup(classified):
    """Ejecutar limpieza según clasificación"""
    print("\n3. EJECUTANDO LIMPIEZA...")
    
    total_archived = 0
    total_deleted = 0
    
    # 1. Archivar scripts temporales
    print("   a) Archivar scripts temporales...")
    for script in classified['scripts_temporales']:
        try:
            dest_dir = os.path.join(ARCHIVE_DIR, "scripts_temporales")
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, script['name'])
            
            # Si ya existe en archive, añadir timestamp
            if os.path.exists(dest_path):
                timestamp = datetime.now().strftime("%H%M%S")
                name, ext = os.path.splitext(script['name'])
                dest_path = os.path.join(dest_dir, f"{name}_{timestamp}{ext}")
            
            shutil.move(script['path'], dest_path)
            total_archived += 1
        except Exception as e:
            print(f"      Error archivando {script['name']}: {e}")
    
    # 2. Archivar documentos duplicados (mantener solo el más reciente)
    print("   b) Archivar documentos duplicados...")
    # Agrupar duplicados por nombre
    duplicates_by_name = {}
    for doc in classified['documentos_duplicados']:
        base_name = doc['name'].replace('.docx', '')
        if base_name not in duplicates_by_name:
            duplicates_by_name[base_name] = []
        duplicates_by_name[base_name].append(doc)
    
    for base_name, docs in duplicates_by_name.items():
        # Ordenar por fecha (más reciente primero)
        docs_sorted = sorted(docs, key=lambda x: x['modified'], reverse=True)
        
        # Mantener el primero (más reciente), archivar el resto
        for i, doc in enumerate(docs_sorted):
            if i == 0:
                continue  # Mantener este
            try:
                dest_dir = os.path.join(ARCHIVE_DIR, "documentos_duplicados")
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, doc['name'])
                
                if os.path.exists(dest_path):
                    timestamp = datetime.now().strftime("%H%M%S")
                    dest_path = os.path.join(dest_dir, f"{base_name}_dup_{timestamp}.docx")
                
                shutil.move(doc['path'], dest_path)
                total_archived += 1
            except Exception as e:
                print(f"      Error archivando {doc['name']}: {e}")
    
    # 3. Archivar backups antiguos
    print("   c) Archivar backups antiguos...")
    for backup in classified['backups_antiguos']:
        try:
            dest_dir = os.path.join(ARCHIVE_DIR, "backups_antiguos")
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, backup['name'])
            
            if os.path.exists(dest_path):
                timestamp = datetime.now().strftime("%H%M%S")
                name, ext = os.path.splitext(backup['name'])
                dest_path = os.path.join(dest_dir, f"{name}_{timestamp}{ext}")
            
            shutil.move(backup['path'], dest_path)
            total_archived += 1
        except Exception as e:
            print(f"      Error archivando {backup['name']}: {e}")
    
    print(f"\n   TOTAL ARCHIVADOS: {total_archived}")
    print(f"   TOTAL MANTENIDOS: {len(classified['keep'])}")
    
    return total_archived

def generate_report(classified, total_archived):
    """Generar reporte de limpieza"""
    print("\n4. GENERANDO REPORTE...")
    
    report_path = os.path.join(ARCHIVE_DIR, "reporte_limpieza.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# REPORTE DE LIMPIEZA INTELIGENTE TREQE\n\n")
        f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total archivos archivados:** {total_archived}\n")
        f.write(f"**Total archivos mantenidos:** {len(classified['keep'])}\n\n")
        
        f.write("## ESTADÍSTICAS\n\n")
        f.write(f"- Scripts temporales archivados: {len(classified['scripts_temporales'])}\n")
        f.write(f"- Documentos duplicados archivados: {len(classified['documentos_duplicados'])}\n")
        f.write(f"- Backups antiguos archivados: {len(classified['backups_antiguos'])}\n\n")
        
        f.write("## ARCHIVOS MANTENIDOS (ESENCIALES)\n\n")
        f.write("| Tipo | Cantidad | Ejemplos |\n")
        f.write("|------|----------|----------|\n")
        
        # Agrupar por tipo
        keep_by_type = {}
        for file in classified['keep']:
            if file['ext'] not in keep_by_type:
                keep_by_type[file['ext']] = []
            keep_by_type[file['ext']].append(file)
        
        for ext, files in sorted(keep_by_type.items()):
            examples = ", ".join([f['name'] for f in files[:3]])
            if len(files) > 3:
                examples += f"... (+{len(files)-3} más)"
            f.write(f"| {ext} | {len(files)} | {examples} |\n")
        
        f.write("\n## ESTRUCTURA FINAL RECOMENDADA\n\n")
        f.write("```\n")
        f.write("Treqe/\n")
        f.write("├── plan_negocio/           # Business plan completo\n")
        f.write("│   ├── PLAN_SEGREGADO_2026/ # 9 secciones + 5 apéndices\n")
        f.write("│   └── versiones_consolidadas/\n")
        f.write("├── subagents/              # Agentes especializados\n")
        f.write("│   ├── algorithm_specialist/\n")
        f.write("│   ├── pitch_designer/\n")
        f.write("│   └── video_producer/\n")
        f.write("├── scripts_esenciales/     # Scripts reutilizables\n")
        f.write("├── data/                   # Datos y configuraciones\n")
        f.write("├── _archive/               # Archivo histórico\n")
        f.write("└── README.md               # Documentación\n")
        f.write("```\n")
    
    print(f"   Reporte generado: {report_path}")
    return report_path

def main():
    """Función principal"""
    try:
        # 1. Analizar archivos
        files = analyze_files()
        
        # 2. Clasificar archivos
        classified = classify_files(files)
        
        # 3. Confirmar con usuario (simulado)
        print("\n¿Continuar con la limpieza? (Sí/No)")
        print(f"Se archivarán {len(classified['scripts_temporales']) + len(classified['documentos_duplicados']) + len(classified['backups_antiguos'])} archivos")
        print(f"Se mantendrán {len(classified['keep'])} archivos")
        
        # Para automatización, asumimos que sí
        confirm = "Sí"
        
        if confirm.lower() in ['sí', 'si', 's', 'yes', 'y']:
            # 4. Ejecutar limpieza
            total_archived = execute_cleanup(classified)
            
            # 5. Generar reporte
            report_path = generate_report(classified, total_archived)
            
            print(f"\n✅ LIMPIEZA COMPLETADA")
            print(f"   Archivos antes: {len(files)}")
            print(f"   Archivos después: {len(classified['keep'])}")
            print(f"   Reducción: {len(files) - len(classified['keep'])} archivos ({((len(files) - len(classified['keep'])) / len(files) * 100):.1f}%)")
            print(f"   Reporte: {report_path}")
        else:
            print("Limpieza cancelada por el usuario")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()