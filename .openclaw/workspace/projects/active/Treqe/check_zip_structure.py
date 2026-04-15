#!/usr/bin/env python3
"""
Verificar estructura de archivo ZIP
"""

import os
import struct

def check_zip_structure():
    """Verificar estructura del archivo ZIP."""
    
    # Ruta al archivo de Illustrator
    file_path = r"C:\Users\Shadow\Downloads\Adobe CC 2018 Collection For Windows (X64) October 2017 Setup + Crack\Adobe Illustrator CC 2018 v22.0.0.243 Setup + Crack.zip.shadownload"
    
    if not os.path.exists(file_path):
        print(f"Error: El archivo no existe: {file_path}")
        return False
    
    print(f"Analizando estructura ZIP: {file_path}")
    file_size = os.path.getsize(file_path)
    print(f"Tamaño total: {file_size:,} bytes ({file_size/(1024*1024):.1f} MB)")
    
    try:
        with open(file_path, 'rb') as f:
            # 1. Verificar firma ZIP al inicio
            f.seek(0)
            signature = f.read(4)
            if signature != b'PK\x03\x04':
                print(f"Firma ZIP no encontrada al inicio: {signature.hex()}")
                return False
            
            print(f"✓ Firma ZIP encontrada al inicio: {signature.hex()} (PK\\x03\\x04)")
            
            # 2. Buscar firma de directorio central al final (debería estar en los últimos 65536 bytes)
            f.seek(max(0, file_size - 65536))
            end_data = f.read(65536)
            
            # Buscar firma de directorio central (0x02014b50)
            central_dir_sig = b'PK\x01\x02'
            central_dir_pos = end_data.rfind(central_dir_sig)
            
            if central_dir_pos != -1:
                print(f"✓ Firma de directorio central encontrada cerca del final")
                actual_pos = max(0, file_size - 65536) + central_dir_pos
                print(f"  Posición: {actual_pos:,} (0x{actual_pos:08x})")
            else:
                print(f"✗ Firma de directorio central NO encontrada")
                print("  Esto sugiere que el archivo ZIP está incompleto o corrupto")
            
            # 3. Buscar firma de fin de directorio central (0x06054b50)
            end_central_dir_sig = b'PK\x05\x06'
            end_central_dir_pos = end_data.rfind(end_central_dir_sig)
            
            if end_central_dir_pos != -1:
                print(f"✓ Firma de fin de directorio central encontrada")
                actual_pos = max(0, file_size - 65536) + end_central_dir_pos
                print(f"  Posición: {actual_pos:,} (0x{actual_pos:08x})")
                
                # Leer el registro de fin de directorio central
                f.seek(actual_pos)
                end_record = f.read(22)  # Tamaño mínimo del registro
                
                if len(end_record) >= 22:
                    # Parsear el registro
                    # signature (4), disk_number (2), central_dir_disk (2), 
                    # disk_entries (2), total_entries (2), central_dir_size (4),
                    # central_dir_offset (4), comment_length (2)
                    values = struct.unpack('<4sHHHHIIH', end_record)
                    
                    print(f"\nInformación del registro de fin de directorio:")
                    print(f"  Número de disco: {values[1]}")
                    print(f"  Disco con directorio central: {values[2]}")
                    print(f"  Entradas en este disco: {values[3]}")
                    print(f"  Entradas totales: {values[4]}")
                    print(f"  Tamaño directorio central: {values[5]:,} bytes")
                    print(f"  Offset directorio central: {values[6]:,} (0x{values[6]:08x})")
                    print(f"  Longitud comentario: {values[7]} bytes")
                    
                    # Verificar que el offset del directorio central esté dentro del archivo
                    if values[6] < file_size:
                        print(f"✓ Offset del directorio central válido")
                    else:
                        print(f"✗ Offset del directorio central fuera del archivo")
                        
                else:
                    print(f"✗ Registro de fin de directorio incompleto")
                    
            else:
                print(f"✗ Firma de fin de directorio central NO encontrada")
                print("  Esto confirma que el archivo ZIP está incompleto")
                print("\nPosibles causas:")
                print("  1. Descarga incompleta (.shadownload sugiere esto)")
                print("  2. Archivo corrupto")
                print("  3. Formato no estándar")
            
            # 4. Verificar últimos bytes
            f.seek(-100, 2)  # Últimos 100 bytes
            last_100 = f.read(100)
            
            print(f"\nÚltimos 100 bytes del archivo:")
            hex_str = last_100.hex()
            for i in range(0, len(hex_str), 32):
                print(f"  {hex_str[i:i+32]}")
            
            # Contar ceros en los últimos 100 bytes
            zero_count = last_100.count(b'\x00')
            print(f"\nDe los últimos 100 bytes, {zero_count} son ceros ({(zero_count/100)*100:.1f}%)")
            
            if zero_count == 100:
                print("⚠️  TODOS los últimos 100 bytes son ceros - muy probablemente descarga incompleta")
            
        return True
        
    except Exception as e:
        print(f"Error al analizar el archivo: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=== ANÁLISIS DE ESTRUCTURA ZIP ===")
    check_zip_structure()