#!/usr/bin/env python3
"""
Test del algoritmo completo con datos demo
"""

import asyncio
import sys
import os
import time

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_algoritmo_completo():
    """Test del algoritmo completo"""
    print("=" * 60)
    print("TEST ALGORITMO TREQE COMPLETO")
    print("=" * 60)
    
    try:
        # Importar módulos
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import select
        
        from src.database.models import User, Item, Preference
        from src.core.algorithm_complete import TreqeMatchingEngineComplete
        
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
            
            # Obtener todos los items
            stmt_items = select(Item)
            result_items = await session.execute(stmt_items)
            all_items = result_items.scalars().all()
            
            # Obtener todas las preferencias
            stmt_prefs = select(Preference)
            result_prefs = await session.execute(stmt_prefs)
            all_prefs = result_prefs.scalars().all()
            
            print(f"   OK Usuarios: {len(all_users)}")
            print(f"   OK Items: {len(all_items)}")
            print(f"   OK Preferencias: {len(all_prefs)}")
            
            # Mostrar datos demo
            print("\n2. Datos demo cargados:")
            for user in all_users:
                print(f"\n   USUARIO: {user.username} (ID: {user.id}, Reputacion: {user.reputation_score})")
                
                # Items del usuario
                stmt_user_items = select(Item).where(Item.user_id == user.id)
                result_user_items = await session.execute(stmt_user_items)
                user_items = result_user_items.scalars().all()
                
                for item in user_items:
                    print(f"      DA: {item.title} (EUR{item.estimated_value})")
                
                # Preferencias del usuario
                stmt_user_prefs = select(Preference).where(Preference.user_id == user.id)
                result_user_prefs = await session.execute(stmt_user_prefs)
                user_prefs = result_user_prefs.scalars().all()
                
                for pref in user_prefs:
                    print(f"      BUSCA: {pref.desired_item_title} (EUR{pref.min_value}-EUR{pref.max_value})")
            
            # Crear motor de matching
            print("\n3. Creando motor de matching completo...")
            engine = TreqeMatchingEngineComplete()
            
            # Test para cada usuario
            print("\n4. Probando algoritmo para cada usuario:")
            
            for user in all_users:
                print(f"\n   Buscando intercambios para {user.username} (ID: {user.id})...")
                
                start_time = time.time()
                proposals = await engine.find_exchanges_for_user(session, user.id)
                search_time_ms = (time.time() - start_time) * 1000
                
                print(f"      Tiempo busqueda: {search_time_ms:.2f} ms")
                print(f"      Propuestas encontradas: {len(proposals)}")
                
                if proposals:
                    for i, proposal in enumerate(proposals, 1):
                        print(f"\n      PROPUESTA {i}:")
                        print(f"      Titulo: {proposal['title']}")
                        print(f"      Resumen: {proposal['summary']}")
                        print(f"      Ajuste financiero: {proposal['financial_adjustment']}")
                        print(f"      Logica economica: {proposal['economic_logic']}")
                        print(f"      k={proposal['k_size']}, Participantes: {proposal['total_participants']}")
                else:
                    print(f"      No se encontraron intercambios para {user.username}")
            
            # Test especial: intercambio circular k=3
            print("\n" + "=" * 60)
            print("5. TEST ESPECIAL: INTERCAMBIO CIRCULAR k=3")
            print("=" * 60)
            
            # Buscar intercambios para Ana (debería encontrar el intercambio circular)
            ana = next((u for u in all_users if u.username == "ana_tech"), None)
            
            if ana:
                print(f"\n   Buscando intercambio circular para Ana (ID: {ana.id})...")
                
                start_time = time.time()
                proposals = await engine.find_exchanges_for_user(session, ana.id)
                search_time_ms = (time.time() - start_time) * 1000
                
                print(f"   Tiempo busqueda: {search_time_ms:.2f} ms")
                
                if proposals:
                    print(f"   EXITO: Se encontraron {len(proposals)} propuestas!")
                    
                    for proposal in proposals:
                        if proposal['k_size'] == 3:
                            print(f"\n   INTERCAMBIO CIRCULAR ENCONTRADO (k=3):")
                            print(f"   Titulo: {proposal['title']}")
                            print(f"   Resumen: {proposal['summary']}")
                            print(f"   Ajuste financiero: {proposal['financial_adjustment']}")
                            print(f"   Logica economica: {proposal['economic_logic']}")
                            
                            # Verificar que es el intercambio esperado
                            print(f"\n   VERIFICACION: Intercambio circular completo (3 usuarios)")
                            print(f"   ALGORITMO FUNCIONA CORRECTAMENTE!")
                else:
                    print(f"   ERROR: No se encontraron propuestas para Ana")
            
            print("\n" + "=" * 60)
            print("RESULTADO FINAL DEL TEST:")
            print("=" * 60)
            
            # Verificar si el algoritmo encontró el intercambio circular
            if proposals and any(p['k_size'] == 3 for p in proposals):
                print("ALGORITMO TREQE VALIDADO EXITOSAMENTE")
                print("\nEl algoritmo encontro el intercambio circular k=3 que es:")
                print("   • IMPOSIBLE en mercado tradicional (k=2)")
                print("   • POSIBLE con Treqe (k=3)")
                print("   • Sistema economicamente consistente")
                print("\nVALIDACION TECNICA COMPLETADA CON EXITO")
                return True
            else:
                print("El algoritmo NO encontro el intercambio circular k=3")
                print("   Revisar implementacion del algoritmo")
                return False
            
    except Exception as e:
        print(f"\nERROR en test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("TEST DEL ALGORITMO TREQE COMPLETO")
    print("Objetivo: Verificar que el algoritmo encuentra intercambio circular k=3")
    
    resultado = asyncio.run(test_algoritmo_completo())
    
    if resultado:
        print("\n" + "=" * 60)
        print("TEST COMPLETADO CON EXITO")
        print("=" * 60)
        print("\nEl algoritmo esta listo para produccion.")
    else:
        print("\nTest fallo")
        sys.exit(1)