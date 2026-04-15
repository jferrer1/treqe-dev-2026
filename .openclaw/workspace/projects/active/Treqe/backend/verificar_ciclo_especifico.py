#!/usr/bin/env python3
"""
Verificación específica del ciclo Ana → Carlos → Beatriz → Ana
"""

import asyncio
import sys
import os

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def verificar_ciclo():
    """Verificar ciclo específico"""
    print("=" * 60)
    print("VERIFICACION CICLO ESPECIFICO")
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
            
            # Obtener usuario Ana
            stmt_ana = select(User).where(User.username == "ana_tech")
            result_ana = await session.execute(stmt_ana)
            ana = result_ana.scalar_one()
            
            # Obtener usuario Carlos
            stmt_carlos = select(User).where(User.username == "carlos_deportes")
            result_carlos = await session.execute(stmt_carlos)
            carlos = result_carlos.scalar_one()
            
            # Obtener usuario Beatriz
            stmt_beatriz = select(User).where(User.username == "beatriz_eco")
            result_beatriz = await session.execute(stmt_beatriz)
            beatriz = result_beatriz.scalar_one()
            
            print(f"   OK Ana: {ana.username} (ID: {ana.id})")
            print(f"   OK Carlos: {carlos.username} (ID: {carlos.id})")
            print(f"   OK Beatriz: {beatriz.username} (ID: {beatriz.id})")
            
            # Obtener items de cada usuario
            stmt_item_ana = select(Item).where(Item.user_id == ana.id)
            result_item_ana = await session.execute(stmt_item_ana)
            item_ana = result_item_ana.scalar_one()
            
            stmt_item_carlos = select(Item).where(Item.user_id == carlos.id)
            result_item_carlos = await session.execute(stmt_item_carlos)
            item_carlos = result_item_carlos.scalar_one()
            
            stmt_item_beatriz = select(Item).where(Item.user_id == beatriz.id)
            result_item_beatriz = await session.execute(stmt_item_beatriz)
            item_beatriz = result_item_beatriz.scalar_one()
            
            print(f"\n2. Items de cada usuario:")
            print(f"   Ana TIENE: {item_ana.title} (EUR{item_ana.estimated_value})")
            print(f"   Carlos TIENE: {item_carlos.title} (EUR{item_carlos.estimated_value})")
            print(f"   Beatriz TIENE: {item_beatriz.title} (EUR{item_beatriz.estimated_value})")
            
            # Obtener preferencias de cada usuario
            stmt_pref_ana = select(Preference).where(Preference.user_id == ana.id)
            result_pref_ana = await session.execute(stmt_pref_ana)
            pref_ana = result_pref_ana.scalar_one()
            
            stmt_pref_carlos = select(Preference).where(Preference.user_id == carlos.id)
            result_pref_carlos = await session.execute(stmt_pref_carlos)
            pref_carlos = result_pref_carlos.scalar_one()
            
            stmt_pref_beatriz = select(Preference).where(Preference.user_id == beatriz.id)
            result_pref_beatriz = await session.execute(stmt_pref_beatriz)
            pref_beatriz = result_pref_beatriz.scalar_one()
            
            print(f"\n3. Preferencias de cada usuario:")
            print(f"   Ana QUIERE: {pref_ana.desired_item_title} (EUR{pref_ana.min_value}-EUR{pref_ana.max_value})")
            print(f"   Carlos QUIERE: {pref_carlos.desired_item_title} (EUR{pref_carlos.min_value}-EUR{pref_carlos.max_value})")
            print(f"   Beatriz QUIERE: {pref_beatriz.desired_item_title} (EUR{pref_beatriz.min_value}-EUR{pref_beatriz.max_value})")
            
            print(f"\n4. Verificando compatibilidades...")
            
            # 1. ¿Ana quiere lo que tiene Carlos?
            ana_quiere_carlos = pref_ana.desired_item_title.lower() in item_carlos.title.lower()
            print(f"   ¿Ana quiere lo que tiene Carlos? {ana_quiere_carlos}")
            print(f"      Ana quiere: '{pref_ana.desired_item_title.lower()}'")
            print(f"      Carlos tiene: '{item_carlos.title.lower()}'")
            print(f"      Contiene?: {pref_ana.desired_item_title.lower() in item_carlos.title.lower()}")
            
            # 2. ¿Carlos quiere lo que tiene Beatriz?
            carlos_quiere_beatriz = pref_carlos.desired_item_title.lower() in item_beatriz.title.lower()
            print(f"   ¿Carlos quiere lo que tiene Beatriz? {carlos_quiere_beatriz}")
            print(f"      Carlos quiere: '{pref_carlos.desired_item_title.lower()}'")
            print(f"      Beatriz tiene: '{item_beatriz.title.lower()}'")
            print(f"      Contiene?: {pref_carlos.desired_item_title.lower() in item_beatriz.title.lower()}")
            
            # 3. ¿Beatriz quiere lo que tiene Ana?
            beatriz_quiere_ana = pref_beatriz.desired_item_title.lower() in item_ana.title.lower()
            print(f"   ¿Beatriz quiere lo que tiene Ana? {beatriz_quiere_ana}")
            print(f"      Beatriz quiere: '{pref_beatriz.desired_item_title.lower()}'")
            print(f"      Ana tiene: '{item_ana.title.lower()}'")
            print(f"      Contiene?: {pref_beatriz.desired_item_title.lower() in item_ana.title.lower()}")
            
            # Verificar rangos de valor
            print(f"\n5. Verificando rangos de valor...")
            
            # ¿El valor del item de Carlos está en el rango que acepta Ana?
            valor_en_rango_ana = pref_ana.min_value <= item_carlos.estimated_value <= pref_ana.max_value
            print(f"   ¿Valor de MacBook (EUR{item_carlos.estimated_value}) está en rango de Ana (EUR{pref_ana.min_value}-EUR{pref_ana.max_value})? {valor_en_rango_ana}")
            
            # ¿El valor del item de Beatriz está en el rango que acepta Carlos?
            valor_en_rango_carlos = pref_carlos.min_value <= item_beatriz.estimated_value <= pref_carlos.max_value
            print(f"   ¿Valor de Bicicleta (EUR{item_beatriz.estimated_value}) está en rango de Carlos (EUR{pref_carlos.min_value}-EUR{pref_carlos.max_value})? {valor_en_rango_carlos}")
            
            # ¿El valor del item de Ana está en el rango que acepta Beatriz?
            valor_en_rango_beatriz = pref_beatriz.min_value <= item_ana.estimated_value <= pref_beatriz.max_value
            print(f"   ¿Valor de iPhone (EUR{item_ana.estimated_value}) está en rango de Beatriz (EUR{pref_beatriz.min_value}-EUR{pref_beatriz.max_value})? {valor_en_rango_beatriz}")
            
            # Resultado final
            ciclo_posible = (
                ana_quiere_carlos and 
                carlos_quiere_beatriz and 
                beatriz_quiere_ana and
                valor_en_rango_ana and
                valor_en_rango_carlos and
                valor_en_rango_beatriz
            )
            
            if ciclo_posible:
                print("\n" + "=" * 60)
                print("INTERCAMBIO CIRCULAR k=3 POSIBLE")
                print("=" * 60)
                
                print(f"\nCICLO COMPLETO:")
                print(f"   Ana: {item_ana.title} -> {pref_ana.desired_item_title}")
                print(f"   Carlos: {item_carlos.title} -> {pref_carlos.desired_item_title}")
                print(f"   Beatriz: {item_beatriz.title} -> {pref_beatriz.desired_item_title}")
                
                print(f"\nVALORES:")
                print(f"   iPhone: EUR{item_ana.estimated_value}")
                print(f"   MacBook: EUR{item_carlos.estimated_value}")
                print(f"   Bicicleta: EUR{item_beatriz.estimated_value}")
                
                print(f"\nRANGOS ACEPTADOS:")
                print(f"   Ana acepta: EUR{pref_ana.min_value}-EUR{pref_ana.max_value}")
                print(f"   Carlos acepta: EUR{pref_carlos.min_value}-EUR{pref_carlos.max_value}")
                print(f"   Beatriz acepta: EUR{pref_beatriz.min_value}-EUR{pref_beatriz.max_value}")
                
                print(f"\nEste intercambio es IMPOSIBLE en mercado tradicional (k=2)")
                print(f"pero POSIBLE con Treqe (k=3).")
                
                return True
            else:
                print("\n" + "=" * 60)
                print("INTERCAMBIO CIRCULAR NO POSIBLE")
                print("=" * 60)
                
                problemas = []
                if not ana_quiere_carlos:
                    problemas.append("Ana no quiere lo que tiene Carlos")
                if not carlos_quiere_beatriz:
                    problemas.append("Carlos no quiere lo que tiene Beatriz")
                if not beatriz_quiere_ana:
                    problemas.append("Beatriz no quiere lo que tiene Ana")
                if not valor_en_rango_ana:
                    problemas.append(f"Valor MacBook (EUR{item_carlos.estimated_value}) fuera de rango de Ana (EUR{pref_ana.min_value}-EUR{pref_ana.max_value})")
                if not valor_en_rango_carlos:
                    problemas.append(f"Valor Bicicleta (EUR{item_beatriz.estimated_value}) fuera de rango de Carlos (EUR{pref_carlos.min_value}-EUR{pref_carlos.max_value})")
                if not valor_en_rango_beatriz:
                    problemas.append(f"Valor iPhone (EUR{item_ana.estimated_value}) fuera de rango de Beatriz (EUR{pref_beatriz.min_value}-EUR{pref_beatriz.max_value})")
                
                print("\nProblemas detectados:")
                for problema in problemas:
                    print(f"   • {problema}")
                
                return False
            
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("VERIFICACION CICLO ESPECIFICO")
    print("Objetivo: Confirmar ciclo Ana -> Carlos -> Beatriz -> Ana")
    
    resultado = asyncio.run(verificar_ciclo())
    
    if resultado:
        print("\n" + "=" * 60)
        print("VALIDACION EXITOSA")
        print("=" * 60)
        print("\nLos datos demo permiten intercambio circular k=3.")
        print("El algoritmo Treqe puede encontrar este intercambio.")
        print("\nValidacion tecnica completada con exito.")
    else:
        print("\n" + "=" * 60)
        print("VALIDACION FALLIDA")
        print("=" * 60)
        print("\nLos datos demo no permiten intercambio circular.")
        print("Revisar la configuracion de datos demo.")
        sys.exit(1)