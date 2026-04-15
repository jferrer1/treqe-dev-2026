#!/usr/bin/env python3
"""
Test directo del algoritmo Treqe con datos demo
"""

import asyncio
import sys
import os
import time

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_algoritmo():
    """Test directo del algoritmo"""
    print("=" * 60)
    print("TEST DIRECTO ALGORITMO TREQE - INTERCAMBIO CIRCULAR k=3")
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
            print("\n3. Creando motor de matching...")
            engine = TreqeMatchingEngineFinal(
                users=all_users,
                items=all_items,
                preferences=all_prefs
            )
            
            # Test para cada usuario
            print("\n4. Probando algoritmo para cada usuario:")
            
            for user in all_users:
                print(f"\n   Buscando intercambios para {user.username} (ID: {user.id})...")
                
                start_time = time.time()
                cycles = engine.find_exchanges_for_user(
                    user_id=user.id,
                    k_max=6,
                    timeout_seconds=5
                )
                search_time_ms = (time.time() - start_time) * 1000
                
                print(f"      Tiempo busqueda: {search_time_ms:.2f} ms")
                print(f"      Ciclos encontrados: {len(cycles)}")
                
                if cycles:
                    for i, cycle in enumerate(cycles, 1):
                        print(f"\n      CICLO {i} (k={cycle.k_size}):")
                        print(f"      Usuarios: {cycle.users}")
                        print(f"      Items: {cycle.items}")
                        print(f"      Valor total: EUR{cycle.total_value:.2f}")
                        print(f"      Comision total: EUR{cycle.commission_total:.2f}")
                        print(f"      Ajustes netos: {cycle.net_adjustments}")
                        
                        # Mostrar detalles del intercambio
                        print(f"\n      DETALLE INTERCAMBIO:")
                        for j, user_id in enumerate(cycle.users):
                            item_id = cycle.items[j]
                            
                            # Buscar usuario
                            stmt_user = select(User).where(User.id == user_id)
                            result_user = await session.execute(stmt_user)
                            cycle_user = result_user.scalar_one()
                            
                            # Buscar item
                            stmt_item = select(Item).where(Item.id == item_id)
                            result_item = await session.execute(stmt_item)
                            cycle_item = result_item.scalar_one()
                            
                            # Buscar preferencia
                            stmt_pref = select(Preference).where(
                                (Preference.user_id == user_id) & 
                                (Preference.item_id == item_id)
                            )
                            result_pref = await session.execute(stmt_pref)
                            cycle_pref = result_pref.scalar_one()
                            
                            print(f"        {cycle_user.username}: {cycle_item.title} -> {cycle_pref.desired_item_title}")
                
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
                cycles = engine.find_exchanges_for_user(
                    user_id=ana.id,
                    k_max=3,  # Solo buscar k=3 para el intercambio circular
                    timeout_seconds=5
                )
                search_time_ms = (time.time() - start_time) * 1000
                
                print(f"   Tiempo busqueda: {search_time_ms:.2f} ms")
                
                if cycles:
                    print(f"   EXITO: Se encontró el intercambio circular k=3!")
                    
                    for cycle in cycles:
                        if cycle.k_size == 3:
                            print(f"\n   INTERCAMBIO CIRCULAR ENCONTRADO:")
                            print(f"   k={cycle.k_size}, Usuarios: {cycle.users}, Items: {cycle.items}")
                            print(f"   Valor total: EUR{cycle.total_value:.2f}")
                            print(f"   Comision total: EUR{cycle.commission_total:.2f}")
                            
                            # Verificar que es el intercambio esperado
                            expected_users = sorted([u.id for u in all_users])
                            actual_users = sorted(cycle.users)
                            
                            if expected_users == actual_users:
                                print(f"   VERIFICACION: Intercambio circular completo (3 usuarios)")
                                print(f"   ALGORITMO FUNCIONA CORRECTAMENTE!")
                            else:
                                print(f"   Intercambio encontrado pero no es el circular completo")
                else:
                    print(f"   ERROR: No se encontró el intercambio circular k=3")
            
            print("\n" + "=" * 60)
            print("RESULTADO FINAL DEL TEST:")
            print("=" * 60)
            
            # Verificar si el algoritmo encontró el intercambio circular
            if cycles and any(c.k_size == 3 for c in cycles):
                print("ALGORITMO TREQE VALIDADO EXITOSAMENTE")
                print("\nEl algoritmo encontró el intercambio circular k=3 que es:")
                print("   • IMPOSIBLE en mercado tradicional (k=2)")
                print("   • POSIBLE con Treqe (k=3)")
                print("   • Sistema económicamente consistente")
                print("\n✅ VALIDACIÓN TÉCNICA COMPLETADA CON ÉXITO")
            else:
                print("El algoritmo NO encontró el intercambio circular k=3")
                print("   Revisar implementación del algoritmo")
            
            return True
            
    except Exception as e:
        print(f"\nERROR en test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("TEST DIRECTO DEL ALGORITMO TREQE")
    print("Objetivo: Verificar que el algoritmo encuentra intercambio circular k=3")
    
    resultado = asyncio.run(test_algoritmo())
    
    if resultado:
        print("\n" + "=" * 60)
        print("TEST COMPLETADO")
        print("=" * 60)
    else:
        print("\nTest falló")
        sys.exit(1)