#!/usr/bin/env python3
"""
Test del método wants_item
"""

import asyncio
import sys
import os

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_wants_item():
    """Test del método wants_item"""
    print("=" * 60)
    print("TEST METODO WANTS_ITEM")
    print("=" * 60)
    
    try:
        # Importar módulos
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import select
        
        from src.database.models import User, Item, Preference
        from src.core.algorithm_final import TreqeUserFinal
        
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
            
            # Obtener item de Ana
            stmt_item_ana = select(Item).where(Item.user_id == ana.id)
            result_item_ana = await session.execute(stmt_item_ana)
            item_ana = result_item_ana.scalar_one()
            
            # Obtener preferencias de Ana
            stmt_prefs_ana = select(Preference).where(Preference.user_id == ana.id)
            result_prefs_ana = await session.execute(stmt_prefs_ana)
            prefs_ana = result_prefs_ana.scalars().all()
            
            # Crear TreqeUserFinal para Ana
            ana_user = TreqeUserFinal(ana, item_ana, prefs_ana)
            
            print(f"\n2. Ana:")
            print(f"   Tiene: {ana_user.item_title}")
            print(f"   Quiere: {ana_user.desired_titles}")
            print(f"   Rango valor: €{ana_user.min_value}-€{ana_user.max_value}")
            
            # Obtener usuario Carlos
            stmt_carlos = select(User).where(User.username == "carlos_deportes")
            result_carlos = await session.execute(stmt_carlos)
            carlos = result_carlos.scalar_one()
            
            # Obtener item de Carlos
            stmt_item_carlos = select(Item).where(Item.user_id == carlos.id)
            result_item_carlos = await session.execute(stmt_item_carlos)
            item_carlos = result_item_carlos.scalar_one()
            
            # Obtener preferencias de Carlos
            stmt_prefs_carlos = select(Preference).where(Preference.user_id == carlos.id)
            result_prefs_carlos = await session.execute(stmt_prefs_carlos)
            prefs_carlos = result_prefs_carlos.scalars().all()
            
            # Crear TreqeUserFinal para Carlos
            carlos_user = TreqeUserFinal(carlos, item_carlos, prefs_carlos)
            
            print(f"\n3. Carlos:")
            print(f"   Tiene: {carlos_user.item_title}")
            print(f"   Quiere: {carlos_user.desired_titles}")
            print(f"   Rango valor: €{carlos_user.min_value}-€{carlos_user.max_value}")
            
            # Test: ¿Ana quiere lo que tiene Carlos?
            print(f"\n4. Test: ¿Ana quiere lo que tiene Carlos?")
            print(f"   Ana quiere: {ana_user.desired_titles}")
            print(f"   Carlos tiene: {carlos_user.item_title}")
            
            resultado = ana_user.wants_item(carlos_user.item_title)
            print(f"   Resultado: {resultado}")
            
            # Test: ¿Carlos quiere lo que tiene Beatriz?
            print(f"\n5. Test: ¿Carlos quiere lo que tiene Beatriz?")
            
            # Obtener usuario Beatriz
            stmt_beatriz = select(User).where(User.username == "beatriz_eco")
            result_beatriz = await session.execute(stmt_beatriz)
            beatriz = result_beatriz.scalar_one()
            
            # Obtener item de Beatriz
            stmt_item_beatriz = select(Item).where(Item.user_id == beatriz.id)
            result_item_beatriz = await session.execute(stmt_item_beatriz)
            item_beatriz = result_item_beatriz.scalar_one()
            
            # Crear TreqeUserFinal para Beatriz
            beatriz_user = TreqeUserFinal(beatriz, item_beatriz, [])
            
            print(f"   Carlos quiere: {carlos_user.desired_titles}")
            print(f"   Beatriz tiene: {beatriz_user.item_title}")
            
            resultado = carlos_user.wants_item(beatriz_user.item_title)
            print(f"   Resultado: {resultado}")
            
            # Test: ¿Beatriz quiere lo que tiene Ana?
            print(f"\n6. Test: ¿Beatriz quiere lo que tiene Ana?")
            
            # Obtener preferencias de Beatriz
            stmt_prefs_beatriz = select(Preference).where(Preference.user_id == beatriz.id)
            result_prefs_beatriz = await session.execute(stmt_prefs_beatriz)
            prefs_beatriz = result_prefs_beatriz.scalars().all()
            
            beatriz_user = TreqeUserFinal(beatriz, item_beatriz, prefs_beatriz)
            
            print(f"   Beatriz quiere: {beatriz_user.desired_titles}")
            print(f"   Ana tiene: {ana_user.item_title}")
            
            resultado = beatriz_user.wants_item(ana_user.item_title)
            print(f"   Resultado: {resultado}")
            
            print(f"\n" + "=" * 60)
            print("RESULTADO:")
            print("=" * 60)
            
            # Verificar si todos los tests pasan
            test1 = ana_user.wants_item(carlos_user.item_title)
            test2 = carlos_user.wants_item(beatriz_user.item_title)
            test3 = beatriz_user.wants_item(ana_user.item_title)
            
            if test1 and test2 and test3:
                print("TODOS LOS TESTS PASAN")
                print("El metodo wants_item funciona correctamente")
                print("El intercambio circular k=3 es posible")
                return True
            else:
                print("ALGUN TEST FALLO")
                print(f"   Ana quiere MacBook? {test1}")
                print(f"   Carlos quiere Bicicleta? {test2}")
                print(f"   Beatriz quiere iPhone? {test3}")
                return False
            
    except Exception as e:
        print(f"\nERROR en test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("TEST DEL METODO WANTS_ITEM")
    print("Objetivo: Verificar que el método de compatibilidad funciona")
    
    resultado = asyncio.run(test_wants_item())
    
    if resultado:
        print("\n" + "=" * 60)
        print("TEST COMPLETADO CON EXITO")
        print("=" * 60)
    else:
        print("\nTest fallo")
        sys.exit(1)