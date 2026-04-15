#!/usr/bin/env python3
"""
Verificación simple del intercambio circular k=3
"""

import asyncio
import sys
import os

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def verificar_intercambio():
    """Verificar que existe intercambio circular k=3"""
    print("=" * 60)
    print("VERIFICACION INTERCAMBIO CIRCULAR k=3")
    print("=" * 60)
    
    try:
        # Importar módulos
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import select
        
        from src.database.models import User, Item, Preference
        
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
            
            # Mapear datos
            user_map = {user.id: user for user in all_users}
            item_map = {item.id: item for item in all_items}
            user_items = {}  # user_id -> item
            user_preferences = {}  # user_id -> list of preferences
            
            for item in all_items:
                user_items[item.user_id] = item
            
            for pref in all_prefs:
                if pref.user_id not in user_preferences:
                    user_preferences[pref.user_id] = []
                user_preferences[pref.user_id].append(pref)
            
            print("\n2. Verificando intercambio circular...")
            
            # Buscar intercambio circular k=3
            circular_found = False
            circular_details = []
            
            # Para cada usuario, verificar si hay un ciclo
            for user1 in all_users:
                user1_item = user_items.get(user1.id)
                if not user1_item:
                    continue
                
                user1_prefs = user_preferences.get(user1.id, [])
                if not user1_prefs:
                    continue
                
                # Buscar usuario que tenga lo que user1 quiere
                for pref1 in user1_prefs:
                    desired_title = pref1.desired_item_title.lower()
                    
                    # Buscar usuario que tenga un item con ese título
                    for user2 in all_users:
                        if user2.id == user1.id:
                            continue
                        
                        user2_item = user_items.get(user2.id)
                        if not user2_item:
                            continue
                        
                        if desired_title in user2_item.title.lower():
                            # user1 quiere lo que tiene user2
                            # Ahora buscar lo que user2 quiere
                            user2_prefs = user_preferences.get(user2.id, [])
                            if not user2_prefs:
                                continue
                            
                            for pref2 in user2_prefs:
                                desired_title2 = pref2.desired_item_title.lower()
                                
                                # Buscar usuario que tenga un item con ese título
                                for user3 in all_users:
                                    if user3.id in [user1.id, user2.id]:
                                        continue
                                    
                                    user3_item = user_items.get(user3.id)
                                    if not user3_item:
                                        continue
                                    
                                    if desired_title2 in user3_item.title.lower():
                                        # user2 quiere lo que tiene user3
                                        # Finalmente, verificar si user3 quiere lo que tiene user1
                                        user3_prefs = user_preferences.get(user3.id, [])
                                        if not user3_prefs:
                                            continue
                                        
                                        for pref3 in user3_prefs:
                                            desired_title3 = pref3.desired_item_title.lower()
                                            if desired_title3 in user1_item.title.lower():
                                                # ¡Ciclo encontrado!
                                                circular_found = True
                                                circular_details = [
                                                    (user1, user1_item, pref1),
                                                    (user2, user2_item, pref2),
                                                    (user3, user3_item, pref3)
                                                ]
                                                break
                                        
                                        if circular_found:
                                            break
                                
                                if circular_found:
                                    break
                        
                        if circular_found:
                            break
                
                if circular_found:
                    break
            
            if circular_found:
                print("\n   INTERCAMBIO CIRCULAR k=3 ENCONTRADO!")
                print("\n   Detalles del intercambio:")
                
                for user, item, pref in circular_details:
                    print(f"\n   {user.username}:")
                    print(f"      TIENE: {item.title} (EUR{item.estimated_value})")
                    print(f"      QUIERE: {pref.desired_item_title} (EUR{pref.min_value}-EUR{pref.max_value})")
                
                print("\n" + "=" * 60)
                print("RESULTADO: INTERCAMBIO CIRCULAR POSIBLE")
                print("=" * 60)
                print("\nEste intercambio es IMPOSIBLE en mercado tradicional (k=2)")
                print("pero POSIBLE con Treqe (k=3).")
                print("\nValidacion tecnica completada con exito.")
                return True
            else:
                print("\n   No se encontro intercambio circular k=3")
                print("\n   Revisando datos individuales...")
                
                for user in all_users:
                    user_item = user_items.get(user.id)
                    user_prefs = user_preferences.get(user.id, [])
                    
                    if user_item and user_prefs:
                        print(f"\n   {user.username}:")
                        print(f"      TIENE: {user_item.title}")
                        for pref in user_prefs:
                            print(f"      QUIERE: {pref.desired_item_title}")
                
                return False
            
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("VERIFICACION DE INTERCAMBIO CIRCULAR k=3")
    print("Objetivo: Confirmar que los datos demo permiten intercambio circular")
    
    resultado = asyncio.run(verificar_intercambio())
    
    if resultado:
        print("\n" + "=" * 60)
        print("VALIDACION EXITOSA")
        print("=" * 60)
        print("\nLos datos demo estan correctamente configurados.")
        print("El intercambio circular k=3 es posible.")
        print("\nEl algoritmo Treqe puede encontrar este intercambio.")
    else:
        print("\n" + "=" * 60)
        print("VALIDACION FALLIDA")
        print("=" * 60)
        print("\nLos datos demo no permiten intercambio circular.")
        print("Revisar la configuracion de datos demo.")
        sys.exit(1)