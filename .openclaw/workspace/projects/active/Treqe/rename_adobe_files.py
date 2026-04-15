#!/usr/bin/env python3
"""
Renombrar archivos Adobe CC 2018 de .shadownload a .zip
"""

import os
import glob

def rename_adobe_files():
    """Renombrar archivos .shadownload a .zip."""
    
    # Ruta a la carpeta Adobe
    adobe_path = r"C:\Users\Shadow\Downloads\Adobe CC 2018 Collection For Windows (X64) October 2017 Setup + Crack"
    
    if not os.path.exists(adobe_path):
        print(f"Error: La carpeta no existe: {adobe_path}")
        return False
    
    print(f"Explorando carpeta: {adobe_path}")
    
    # Buscar archivos .shadownload
    shadownload_files = glob.glob(os.path.join(adobe_path, "*.shadownload"))
    
    if not shadownload_files:
        print("No se encontraron archivos .shadownload")
        return False
    
    print(f"Encontrados {len(shadownload_files)} archivos .shadownload")
    
    # Renombrar cada archivo
    renamed_count = 0
    for old_path in shadownload_files:
        # Crear nuevo nombre reemplazando .shadownload por .zip
        new_path = old_path.replace(".shadownload", ".zip")
        
        # Verificar si ya existe un archivo .zip con ese nombre
        if os.path.exists(new_path):
            print(f"  Ya existe: {os.path.basename(new_path)} - Saltando")
            continue
        
        try:
            os.rename(old_path, new_path)
            print(f"  Renombrado: {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
            renamed_count += 1
        except Exception as e:
            print(f"  Error renombrando {os.path.basename(old_path)}: {e}")
    
    print(f"\nTotal renombrados: {renamed_count} de {len(shadownload_files)} archivos")
    
    # Listar archivos después del renombrado
    print("\nArchivos en la carpeta después del renombrado:")
    zip_files = glob.glob(os.path.join(adobe_path, "*.zip"))
    for zip_file in zip_files:
        file_size = os.path.getsize(zip_file)
        size_mb = file_size / (1024 * 1024)
        print(f"  {os.path.basename(zip_file)} ({size_mb:.1f} MB)")
    
    return True

if __name__ == '__main__':
    print("=== RENOMBRAR ARCHIVOS ADOBE CC 2018 ===")
    print("Cambiando extensión .shadownload a .zip...")
    success = rename_adobe_files()
    
    if success:
        print("\n¡Proceso completado!")
        print("\nAhora puedes extraer los archivos .zip para acceder a los instaladores.")
        print("Busca el archivo de Illustrator para instalarlo según las instrucciones del README.")
    else:
        print("\nProceso falló o no se encontraron archivos para renombrar.")