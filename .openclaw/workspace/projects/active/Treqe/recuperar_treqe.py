import os
import shutil

backup_root = r'C:\Users\Shadow\Downloads\.openclaw\workspace'
current_root = r'C:\Users\Shadow\.openclaw\workspace'

backup_treqe = os.path.join(backup_root, 'projects', 'Treqe')
current_treqe = os.path.join(current_root, 'projects', 'Treqe')

print("=== RECUPERANDO PROYECTO TREQE ===")
print(f"Backup: {backup_treqe}")
print(f"Current: {current_treqe}")
print()

# Verificar que existe en backup
if not os.path.exists(backup_treqe):
    print("ERROR: Treqe no existe en backup")
    exit(1)

# Verificar estado actual
if os.path.exists(current_treqe):
    # Contar archivos actuales
    current_files = 0
    for root, dirs, files in os.walk(current_treqe):
        current_files += len(files)
    
    print(f"Treqe actual tiene: {current_files} archivos")
    
    if current_files > 0:
        print("ADVERTENCIA: Treqe actual no esta vacio")
        respuesta = input("¿Sobrescribir? (si/no): ")
        if respuesta.lower() != 'si':
            print("Cancelado")
            exit(0)
    
    # Eliminar current
    try:
        shutil.rmtree(current_treqe)
        print("Carpeta Treqe actual eliminada")
    except Exception as e:
        print(f"Error eliminando: {e}")
        exit(1)

# Contar archivos en backup
backup_files = 0
backup_dirs = 0
for root, dirs, files in os.walk(backup_treqe):
    backup_files += len(files)
    backup_dirs += len(dirs)

print(f"Treqe en backup tiene: {backup_files} archivos, {backup_dirs} carpetas")

# Copiar
print("\nCopiando Treqe desde backup...")
try:
    shutil.copytree(backup_treqe, current_treqe)
    print("OK: Treqe copiado exitosamente")
except Exception as e:
    print(f"ERROR copiando: {e}")
    exit(1)

# Verificar
print("\n=== VERIFICACION ===")
if os.path.exists(current_treqe):
    # Contar archivos copiados
    copied_files = 0
    copied_dirs = 0
    for root, dirs, files in os.walk(current_treqe):
        copied_files += len(files)
        copied_dirs += len(dirs)
    
    print(f"Treqe recuperado: {copied_files} archivos, {copied_dirs} carpetas")
    
    if copied_files == backup_files:
        print("OK: Todos los archivos recuperados")
    else:
        print(f"ADVERTENCIA: Diferencia en archivos (backup: {backup_files}, current: {copied_files})")
    
    # Verificar archivos importantes
    important_files = [
        "README.md",
        "implementacion_algoritmo",
        "analisis_mercado",
        "plan_negocio"
    ]
    
    print("\nArchivos importantes:")
    for file in important_files:
        path = os.path.join(current_treqe, file)
        if os.path.exists(path):
            if os.path.isdir(path):
                items = len(os.listdir(path))
                print(f"  OK: {file}/ ({items} items)")
            else:
                size = os.path.getsize(path)
                print(f"  OK: {file} ({size} bytes)")
        else:
            print(f"  FALTANTE: {file}")
else:
    print("ERROR: Treqe no se copio correctamente")