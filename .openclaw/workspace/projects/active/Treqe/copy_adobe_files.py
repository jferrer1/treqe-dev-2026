#!/usr/bin/env python3
"""
Copiar archivos Adobe CC 2018 de .shadownload a .zip (copiar en lugar de renombrar)
"""

import os
import glob
import shutil

def copy_adobe_files():
    """Copiar archivos .shadownload a .zip."""
    
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
    
    # Crear una subcarpeta para los archivos .zip
    zip_folder = os.path.join(adobe_path, "zip_files")
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder)
        print(f"Creada carpeta para archivos .zip: {zip_folder}")
    
    # Copiar cada archivo con nueva extensión
    copied_count = 0
    for old_path in shadownload_files:
        # Crear nuevo nombre reemplazando .shadownload por .zip
        filename = os.path.basename(old_path)
        new_filename = filename.replace(".shadownload", ".zip")
        new_path = os.path.join(zip_folder, new_filename)
        
        # Verificar si ya existe un archivo .zip con ese nombre
        if os.path.exists(new_path):
            print(f"  Ya existe: {new_filename} - Saltando")
            continue
        
        try:
            # Copiar el archivo
            shutil.copy2(old_path, new_path)
            print(f"  Copiado: {filename} -> {new_filename}")
            copied_count += 1
            
            # Verificar tamaño
            file_size = os.path.getsize(new_path)
            size_mb = file_size / (1024 * 1024)
            print(f"    Tamaño: {size_mb:.1f} MB")
            
        except Exception as e:
            print(f"  Error copiando {filename}: {e}")
    
    print(f"\nTotal copiados: {copied_count} de {len(shadownload_files)} archivos")
    
    # Listar archivos copiados
    if copied_count > 0:
        print(f"\nArchivos copiados a: {zip_folder}")
        zip_files = glob.glob(os.path.join(zip_folder, "*.zip"))
        for zip_file in zip_files:
            file_size = os.path.getsize(zip_file)
            size_mb = file_size / (1024 * 1024)
            print(f"  {os.path.basename(zip_file)} ({size_mb:.1f} MB)")
    
    return True

if __name__ == '__main__':
    print("=== COPIAR ARCHIVOS ADOBE CC 2018 ===")
    print("Copiando archivos .shadownload a .zip...")
    success = copy_adobe_files()
    
    if success:
        print("\n¡Proceso completado!")
        print("\nLos archivos .zip están listos para extraer en la subcarpeta 'zip_files'.")
        print("Busca el archivo de Illustrator para instalarlo según las instrucciones del README.")
    else:
        print("\nProceso falló o no se encontraron archivos para copiar.")