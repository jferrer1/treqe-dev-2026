#!/usr/bin/env python3
"""
Verificar la firma del archivo (magic bytes)
"""

import os

def check_file_signature():
    """Verificar los primeros bytes del archivo."""
    
    # Ruta al archivo de Illustrator
    illustrator_path = r"C:\Users\Shadow\Downloads\Adobe CC 2018 Collection For Windows (X64) October 2017 Setup + Crack\Adobe Illustrator CC 2018 v22.0.0.243 Setup + Crack.zip.shadownload"
    
    if not os.path.exists(illustrator_path):
        print(f"Error: El archivo no existe: {illustrator_path}")
        return False
    
    print(f"Verificando firma del archivo: {illustrator_path}")
    
    try:
        # Leer primeros 8 bytes
        with open(illustrator_path, 'rb') as f:
            magic_bytes = f.read(8)
        
        print(f"Primeros 8 bytes (hex): {magic_bytes.hex()}")
        print(f"Primeros 8 bytes (ASCII): {magic_bytes}")
        
        # Comparar con firmas conocidas
        signatures = {
            '504b0304': 'ZIP file (PK..)',
            '52494646': 'RIFF (AVI, WAV)',
            '25504446': 'PDF file (%PDF)',
            '377abcaf': '7z archive',
            '1f8b0800': 'GZIP file',
            '4d5a9000': 'Windows executable (MZ)',
            '7f454c46': 'ELF executable',
            '000001ba': 'MPEG file',
            '000001b3': 'MPEG file',
            '424d': 'BMP image (BM)',
            'ffd8ff': 'JPEG image',
            '89504e47': 'PNG image',
            '47494638': 'GIF image',
            '494433': 'MP3 file (ID3)',
            '524d4634': 'RealMedia file (RMF)',
            '2e7261fd': 'RealAudio file',
            '3026b275': 'Windows Media (ASF)',
            '4f676753': 'Ogg Vorbis',
            '1a45dfa3': 'Matroska (MKV, WEBM)',
            '00000018': 'MP4/QuickTime',
            '0000001c': 'MP4/QuickTime',
            '00000020': 'MP4/QuickTime',
            '1a45dfa3': 'Matroska/WebM',
        }
        
        hex_sig = magic_bytes.hex()
        found = False
        
        for sig, desc in signatures.items():
            if hex_sig.startswith(sig):
                print(f"\nFirma identificada: {desc}")
                print(f"Coincide con: {sig}")
                found = True
                break
        
        if not found:
            print(f"\nFirma no reconocida.")
            print("Posibles causas:")
            print("1. Archivo corrupto")
            print("2. Formato no estándar")
            print("3. Archivo cifrado/empaquetado")
            print("4. Archivo parcialmente descargado (.shadownload sugiere esto)")
        
        # También verificar si el archivo termina correctamente
        file_size = os.path.getsize(illustrator_path)
        print(f"\nTamaño total del archivo: {file_size:,} bytes ({file_size/(1024*1024):.1f} MB)")
        
        # Leer últimos 8 bytes
        with open(illustrator_path, 'rb') as f:
            f.seek(-8, 2)  # Ir a 8 bytes antes del final
            last_bytes = f.read(8)
        
        print(f"Últimos 8 bytes (hex): {last_bytes.hex()}")
        
        return True
        
    except Exception as e:
        print(f"Error al verificar el archivo: {e}")
        return False

if __name__ == '__main__':
    print("=== VERIFICAR FIRMA DE ARCHIVO ===")
    check_file_signature()