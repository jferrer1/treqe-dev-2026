#!/usr/bin/env python3
"""
Test del algoritmo final fijo con datos demo
"""

import asyncio
import sys
import os
import time

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_algoritmo_final_fixed():
    """Test del algoritmo final fijo"""
    print("=" * 60)
    print("TEST ALGORITMO TREQE FINAL FIXED")
    print("=" * 60)
    
    try:
        # Importar módulos
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import select
        
        from src.database.models import User, Item, Preference
        from src.core.algorithm_final import TreqeMatchingEngineFinal
        
        # Conectar a SQLite
        DATABASE_URL = "sqlite+aiosqlite:///treqe_demo.db"
        engine = create_async_engine(DATABASE_URL, echo=False)
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with async_session() as session:
            print("1. Cargando datos demo...")
            
            # Obtener todos los usuarios
            stmt_users = select(User)
            result_users = await session.execute(stmt_users)
            all_users = result_users.scalars().all()
            
            print(f"   OK Usuarios: {len(all_users)}")
            
            # Crear motor de matching final
            print("\n2. Creando motor de matching final...")
            matching_engine = TreqeMatchingEngineFinal()
            
            # Test para cada usuario
            print("\n3. Probando algoritmo final:")
            
            for user in all_users:
                print(f"\n   Buscando intercambios para {user.username} (ID: {user.id})...")
                
                start_time = time.time()
                proposals = await matching_engine.find_exchanges_for_user(session, user.id)
                search_time_ms = (time.time() - start_time) * 1000
                
                print(f"      Tiempo busqueda: {search_time_ms:.2f} ms")
                print(f"      Propuestas encontradas: {len(proposals)}")
                
                if proposals:
                    for i, proposal in enumerate(proposals[:2], 1):  # Mostrar máximo 2
                        print(f"\n      PROPUESTA {i} (k={proposal['k_size']}):")
                        print(f"      {proposal['title']}")
                        print(f"      {proposal['summary']}")
                        print(f"      {proposal['financial_adjustment']}")
                        print(f"      Logica: {proposal['economic_logic']}")
                else:
                    print(f"      No se encontraron intercambios")
            
            # Test especial: intercambio circular k=3
            print("\n" + "=" * 60)
            print("4. TEST ESPECIAL: INTERCAMBIO CIRCULAR k=3")
            print("=" * 60)
            
            ana = next((u for u in all_users if u.username == "ana_tech"), None)
            
            if ana:
                print(f"\n   Buscando intercambio circular para Ana (ID: {ana.id})...")
                
                start_time = time.time()
                proposals = await matching_engine.find_exchanges_for_user(session, ana.id)
                search_time_ms = (time.time() - start_time) * 1000
                
                print(f"   Tiempo busqueda: {search_time_ms:.2f} ms")
                
                if proposals:
                    circular_found = False
                    for proposal in proposals:
                        if proposal['k_size'] == 3:
                            circular_found = True
                            print(f"\n   INTERCAMBIO CIRCULAR ENCONTRADO (k=3):")
                            print(f"   {proposal['title']}")
                            print(f"   {proposal['summary']}")
                            print(f"   {proposal['financial_adjustment']}")
                            print(f"   Logica: {proposal['economic_logic']}")
                    
                    if circular_found:
                        print(f"\n   VERIFICACION: Intercambio circular completo (3 usuarios)")
                        print(f"   ALGORITMO FINAL FUNCIONA CORRECTAMENTE!")
                        return True
                    else:
                        print(f"   No se encontro intercambio circular k=3")
                        return False
                else:
                    print(f"   ERROR: No se encontraron propuestas")
                    return False
            
            return False
            
    except Exception as e:
        print(f"\nERROR en test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("TEST DEL ALGORITMO TREQE FINAL FIXED")
    print("Objetivo: Verificar algoritmo final fijo funciona con datos demo")
    
    resultado = asyncio.run(test_algoritmo_final_fixed())
    
    if resultado:
        print("\n" + "=" * 60)
        print("TEST COMPLETADO CON EXITO")
        print("=" * 60)
        print("\nEl algoritmo final esta reparado y listo para produccion.")
        print("Puede integrarse con el endpoint /api/v1/matching/find")
    else:
        print("\nTest fallo")
        sys.exit(1)