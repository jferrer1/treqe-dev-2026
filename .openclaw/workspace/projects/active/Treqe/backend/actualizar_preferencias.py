#!/usr/bin/env python3
"""
Actualizar preferencias para que coincidan exactamente con los títulos
"""

import asyncio
import sys
import os

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def actualizar_preferencias():
    """Actualizar preferencias para intercambio circular perfecto"""
    print("=" * 60)
    print("ACTUALIZANDO PREFERENCIAS")
    print("=" * 60)
    
    try:
        # Importar módulos
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import select, update
        
        from src.database.models import User, Item, Preference
        
        # Conectar a SQLite
        DATABASE_URL = "sqlite+aiosqlite:///treqe_demo.db"
        engine = create_async_engine(DATABASE_URL, echo=False)
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with async_session() as session:
            print("1. Cargando datos...")
            
            # Obtener usuarios
            stmt_ana = select(User).where(User.username == "ana_tech")
            result_ana = await session.execute(stmt_ana)
            ana = result_ana.scalar_one()
            
            stmt_carlos = select(User).where(User.username == "carlos_deportes")
            result_carlos = await session.execute(stmt_carlos)
            carlos = result_carlos.scalar_one()
            
            stmt_beatriz = select(User).where(User.username == "beatriz_eco")
            result_beatriz = await session.execute(stmt_beatriz)
            beatriz = result_beatriz.scalar_one()
            
            # Obtener items
            stmt_item_carlos = select(Item).where(Item.user_id == carlos.id)
            result_item_carlos = await session.execute(stmt_item_carlos)
            item_carlos = result_item_carlos.scalar_one()
            
            stmt_item_beatriz = select(Item).where(Item.user_id == beatriz.id)
            result_item_beatriz = await session.execute(stmt_item_beatriz)
            item_beatriz = result_item_beatriz.scalar_one()
            
            stmt_item_ana = select(Item).where(Item.user_id == ana.id)
            result_item_ana = await session.execute(stmt_item_ana)
            item_ana = result_item_ana.scalar_one()
            
            print(f"   OK Ana: {ana.username}")
            print(f"   OK Carlos: {carlos.username}")
            print(f"   OK Beatriz: {beatriz.username}")
            
            print(f"\n2. Items actuales:")
            print(f"   Carlos tiene: {item_carlos.title}")
            print(f"   Beatriz tiene: {item_beatriz.title}")
            print(f"   Ana tiene: {item_ana.title}")
            
            # Obtener preferencias
            stmt_pref_ana = select(Preference).where(Preference.user_id == ana.id)
            result_pref_ana = await session.execute(stmt_pref_ana)
            pref_ana = result_pref_ana.scalar_one()
            
            stmt_pref_carlos = select(Preference).where(Preference.user_id == carlos.id)
            result_pref_carlos = await session.execute(stmt_pref_carlos)
            pref_carlos = result_pref_carlos.scalar_one()
            
            stmt_pref_beatriz = select(Preference).where(Preference.user_id == beatriz.id)
            result_pref_beatriz = await session.execute(stmt_pref_beatriz)
            pref_beatriz = result_pref_beatriz.scalar_one()
            
            print(f"\n3. Preferencias actuales:")
            print(f"   Ana quiere: {pref_ana.desired_item_title}")
            print(f"   Carlos quiere: {pref_carlos.desired_item_title}")
            print(f"   Beatriz quiere: {pref_beatriz.desired_item_title}")
            
            # Actualizar preferencias para que coincidan exactamente
            print(f"\n4. Actualizando preferencias...")
            
            # Ana quiere exactamente lo que tiene Carlos
            pref_ana.desired_item_title = item_carlos.title
            pref_ana.min_value = item_carlos.estimated_value - 50
            pref_ana.max_value = item_carlos.estimated_value + 50
            
            # Carlos quiere exactamente lo que tiene Beatriz
            pref_carlos.desired_item_title = item_beatriz.title
            pref_carlos.min_value = item_beatriz.estimated_value - 50
            pref_carlos.max_value = item_beatriz.estimated_value + 50
            
            # Beatriz quiere exactamente lo que tiene Ana
            pref_beatriz.desired_item_title = item_ana.title
            pref_beatriz.min_value = item_ana.estimated_value - 50
            pref_beatriz.max_value = item_ana.estimated_value + 50
            
            await session.commit()
            
            print(f"\n5. Preferencias actualizadas:")
            print(f"   Ana quiere: {pref_ana.desired_item_title} (EUR{pref_ana.min_value}-EUR{pref_ana.max_value})")
            print(f"   Carlos quiere: {pref_carlos.desired_item_title} (EUR{pref_carlos.min_value}-EUR{pref_carlos.max_value})")
            print(f"   Beatriz quiere: {pref_beatriz.desired_item_title} (EUR{pref_beatriz.min_value}-EUR{pref_beatriz.max_value})")
            
            print(f"\n" + "=" * 60)
            print("ACTUALIZACION COMPLETADA")
            print("=" * 60)
            print("\nAhora el intercambio circular k=3 es perfecto:")
            print(f"   Ana: {item_ana.title} -> {pref_ana.desired_item_title}")
            print(f"   Carlos: {item_carlos.title} -> {pref_carlos.desired_item_title}")
            print(f"   Beatriz: {item_beatriz.title} -> {pref_beatriz.desired_item_title}")
            
            return True
            
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("ACTUALIZACION DE PREFERENCIAS")
    print("Objetivo: Hacer que las preferencias coincidan exactamente")
    
    resultado = asyncio.run(actualizar_preferencias())
    
    if resultado:
        print("\n" + "=" * 60)
        print("EXITO")
        print("=" * 60)
        print("\nLas preferencias se han actualizado correctamente.")
        print("El intercambio circular k=3 ahora es perfectamente compatible.")
    else:
        print("\n" + "=" * 60)
        print("FALLO")
        print("=" * 60)
        print("\nNo se pudieron actualizar las preferencias.")
        sys.exit(1)