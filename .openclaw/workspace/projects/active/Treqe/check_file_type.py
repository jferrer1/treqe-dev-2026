#!/usr/bin/env python3
"""
Verificar si los archivos .shadownload son realmente archivos ZIP
"""

import os
import zipfile

def check_file_type():
    """Verificar tipo de archivo."""
    
    # Ruta al archivo de Illustrator
    illustrator_path = r"C:\Users\Shadow\Downloads\Adobe CC 2018 Collection For Windows (X64) October 2017 Setup + Crack\Adobe Illustrator CC 2018 v22.0.0.243 Setup + Crack.zip.shadownload"
    
    if not os.path.exists(illustrator_path):
        print(f"Error: El archivo no existe: {illustrator_path}")
        return False
    
    print(f"Verificando archivo: {illustrator_path}")
    file_size = os.path.getsize(illustrator_path)
    size_mb = file_size / (1024 * 1024)
    print(f"Tamaño: {size_mb:.1f} MB")
    
    # Intentar abrir como ZIP
    try:
        with zipfile.ZipFile(illustrator_path, 'r') as zip_ref:
            # Listar algunos archivos dentro
            file_list = zip_ref.namelist()
            print(f"\nEl archivo ES un ZIP válido!")
            print(f"Contiene {len(file_list)} archivos/directorios")
            
            # Mostrar primeros 10 archivos
            print("\nPrimeros 10 archivos/directorios:")
            for i, filename in enumerate(file_list[:10]):
                print(f"  {i+1}. {filename}")
            
            # Buscar archivos README o instrucciones
            readme_files = [f for f in file_list if 'readme' in f.lower() or 'instruc' in f.lower() or 'crack' in f.lower()]
            if readme_files:
                print("\nArchivos de instrucciones encontrados:")
                for readme in readme_files:
                    print(f"  - {readme}")
                    
                    # Intentar leer el contenido si es un archivo de texto
                    if readme.lower().endswith(('.txt', '.md', '.rtf', '.doc', '.docx', '.pdf')):
                        try:
                            # Para archivos de texto pequeños
                            if readme.lower().endswith(('.txt', '.md', '.rtf')):
                                with zip_ref.open(readme) as f:
                                    content = f.read(1000)  # Leer primeros 1000 bytes
                                    print(f"    Contenido (primeros 1000 bytes):")
                                    print(f"    {content.decode('utf-8', errors='ignore')[:200]}...")
                        except:
                            pass
            
            return True
            
    except zipfile.BadZipFile:
        print("\nEl archivo NO es un ZIP válido.")
        print("Puede estar corrupto o tener un formato diferente.")
        return False
    except Exception as e:
        print(f"\nError al verificar el archivo: {e}")
        return False

if __name__ == '__main__':
    print("=== VERIFICAR TIPO DE ARCHIVO ADOBE ===")
    check_file_type()