#!/usr/bin/env python3
"""
Script de ejecución simple para el algoritmo Treqe
"""

import sys
import os
import time

# Añadir directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from treqe_algorithm_v1 import TreqeAscendingAlgorithm, main
    
    print("✅ Algoritmo Treqe cargado correctamente")
    print()
    
    # Ejecutar función principal
    main()
    
except ImportError as e:
    print(f"❌ Error importando algoritmo: {e}")
    print("\nIntentando ejecutar directamente...")
    
    # Ejecutar el archivo directamente
    import subprocess
    
    try:
        result = subprocess.run(
            [sys.executable, "treqe_algorithm_v1.py"],
            capture_output=True,
            text=True,
            timeout=310  # 5 minutos + 10 segundos de margen
        )
        
        print(result.stdout)
        if result.stderr:
            print("ERRORES:", result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT: El algoritmo excedió el tiempo límite (5 minutos)")
    except Exception as e:
        print(f"❌ Error ejecutando algoritmo: {e}")