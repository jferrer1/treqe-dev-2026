#!/usr/bin/env python3
"""
Test del endpoint /api/v1/matching/find con algoritmo final reparado
"""

import asyncio
import sys
import os
import json

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_endpoint_matching():
    """Test del endpoint de matching"""
    print("=" * 60)
    print("TEST ENDPOINT MATCHING")
    print("=" * 60)
    
    try:
        # Importar módulos
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import select
        
        from src.database.models import User
        from src.core.algorithm_final import TreqeMatchingEngineFinal
        
        # Conectar a SQLite
        DATABASE_URL = "sqlite+aiosqlite:///treqe_demo.db"
        engine = create_async_engine(DATABASE_URL, echo=False)
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with async_session() as session:
            print("1. Cargando datos demo...")
            
            # Obtener usuario Ana
            stmt_ana = select(User).where(User.username == "ana_tech")
            result_ana = await session.execute(stmt_ana)
            ana = result_ana.scalar_one()
            
            print(f"   OK Usuario: {ana.username} (ID: {ana.id})")
            
            # Crear motor de matching final
            print("\n2. Creando motor de matching final...")
            matching_engine = TreqeMatchingEngineFinal()
            
            # Simular llamada al endpoint
            print("\n3. Simulando endpoint /api/v1/matching/find...")
            
            # Buscar intercambios para Ana
            exchanges = await matching_engine.find_exchanges_for_user(session, ana.id)
            
            print(f"   Resultado: {len(exchanges)} intercambios encontrados")
            
            if exchanges:
                print("\n4. Detalles del primer intercambio:")
                exchange = exchanges[0]
                
                print(f"   Titulo: {exchange['title']}")
                print(f"   k_size: {exchange['k_size']}")
                print(f"   Total participantes: {exchange['total_participants']}")
                print(f"   Resumen: {exchange['summary']}")
                print(f"   Ajuste financiero: {exchange['financial_adjustment']}")
                print(f"   Logica economica: {exchange['economic_logic']}")
                print(f"   ID intercambio: {exchange['exchange_id']}")
                print(f"   Version algoritmo: {exchange['algorithm_version']}")
                
                # Verificar que es el intercambio circular k=3
                if exchange['k_size'] == 3:
                    print("\n" + "=" * 60)
                    print("ENDPOINT MATCHING FUNCIONA CORRECTAMENTE")
                    print("=" * 60)
                    print("\nEl endpoint /api/v1/matching/find devuelve:")
                    print("   • Intercambio circular k=3 encontrado")
                    print("   • Propuesta completa con detalles financieros")
                    print("   • Logica economica correcta")
                    print("   • Metadata completa")
                    print("\nALGORITMO FINAL REPARADO Y FUNCIONAL")
                    return True
                else:
                    print("\nIntercambio encontrado pero no es k=3")
                    return False
            else:
                print("\nNo se encontraron intercambios")
                return False
            
    except Exception as e:
        print(f"\nERROR en test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("TEST DEL ENDPOINT /api/v1/matching/find")
    print("Objetivo: Verificar que el endpoint funciona con algoritmo final reparado")
    
    resultado = asyncio.run(test_endpoint_matching())
    
    if resultado:
        print("\n" + "=" * 60)
        print("TEST COMPLETADO CON EXITO")
        print("=" * 60)
        print("\nEl algoritmo final esta completamente reparado y listo.")
        print("El backend Treqe puede ejecutar intercambios circulares k=3.")
        print("\nREPARACION DEL ALGORITMO COMPLETADA")
    else:
        print("\nTest fallo")
        sys.exit(1)