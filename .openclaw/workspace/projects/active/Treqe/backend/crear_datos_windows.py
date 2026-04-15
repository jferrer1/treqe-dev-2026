#!/usr/bin/env python3
"""
Script para crear datos demo para Treqe - VERSION WINDOWS SIN EMOJIS
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
import random

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Configuración simple
DATABASE_URL = "postgresql+asyncpg://treqe:treqepass@localhost:5432/treqe_db"

# Datos demo realistas
USUARIOS_DEMO = [
    {
        "username": "ana_tech",
        "email": "ana@demo.treqe.com",
        "full_name": "Ana García",
        "reputation_score": 85.0,
        "items": [
            {
                "title": "iPhone 13 128GB Negro",
                "description": "iPhone 13 en perfecto estado, con funda y cargador original",
                "category": "Electrónica",
                "estimated_value": 600.0,
                "condition": "Excelente"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "MacBook Air M1",
                "desired_category": "Electrónica",
                "min_value": 700.0,
                "max_value": 900.0,
                "priority": "high"
            }
        ]
    },
    {
        "username": "carlos_deportes",
        "email": "carlos@demo.treqe.com",
        "full_name": "Carlos Martínez",
        "reputation_score": 72.0,
        "items": [
            {
                "title": "MacBook Air M1 2020",
                "description": "MacBook Air M1 8GB/256GB, batería 95%, impecable",
                "category": "Electrónica",
                "estimated_value": 800.0,
                "condition": "Excelente"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "Bicicleta de montaña",
                "desired_category": "Deportes",
                "min_value": 350.0,
                "max_value": 600.0,
                "priority": "high"
            }
        ]
    },
    {
        "username": "beatriz_eco",
        "email": "beatriz@demo.treqe.com",
        "full_name": "Beatriz López",
        "reputation_score": 65.0,
        "items": [
            {
                "title": "Bicicleta Trek Marlin 5",
                "description": "Bicicleta de montaña Trek, tamaño M, usada pero en buen estado",
                "category": "Deportes",
                "estimated_value": 400.0,
                "condition": "Bueno"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "iPhone 13 o 14",
                "desired_category": "Electrónica",
                "min_value": 550.0,
                "max_value": 750.0,
                "priority": "high"
            }
        ]
    }
]

async def main():
    """Función principal"""
    print("SISTEMA DE DATOS DEMO - TREQE")
    print("=" * 60)
    
    try:
        # Importar módulos
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import select
        
        from src.database.models import Base, User, Item, Preference
        
        print("1. Conectando a base de datos...")
        engine = create_async_engine(DATABASE_URL, echo=False)
        
        print("2. Creando tablas...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
        print("3. Creando sesión...")
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with async_session() as session:
            print("4. Creando usuarios demo...")
            
            for i, usuario_data in enumerate(USUARIOS_DEMO, 1):
                # Crear usuario
                usuario = User(
                    username=usuario_data["username"],
                    email=usuario_data["email"],
                    full_name=usuario_data["full_name"],
                    reputation_score=usuario_data["reputation_score"],
                    is_active=True,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                
                session.add(usuario)
                await session.flush()
                
                # Crear items
                for item_data in usuario_data["items"]:
                    item = Item(
                        user_id=usuario.id,
                        title=item_data["title"],
                        description=item_data["description"],
                        category=item_data["category"],
                        estimated_value=item_data["estimated_value"],
                        condition=item_data["condition"],
                        status="available",
                        created_at=datetime.now() - timedelta(days=random.randint(1, 15))
                    )
                    session.add(item)
                
                # Crear preferencias
                for pref_data in usuario_data["preferences"]:
                    preference = Preference(
                        user_id=usuario.id,
                        desired_item_title=pref_data["desired_item_title"],
                        desired_category=pref_data["desired_category"],
                        min_value=pref_data["min_value"],
                        max_value=pref_data["max_value"],
                        priority=pref_data["priority"],
                        is_active=True,
                        created_at=datetime.now() - timedelta(days=random.randint(1, 7))
                    )
                    session.add(preference)
                
                print(f"   OK Usuario {i}: {usuario.username}")
            
            await session.commit()
            
            # Verificar datos
            print("\n5. Verificando datos creados...")
            
            stmt_users = select(User)
            result_users = await session.execute(stmt_users)
            usuarios = result_users.scalars().all()
            
            stmt_items = select(Item)
            result_items = await session.execute(stmt_items)
            items = result_items.scalars().all()
            
            stmt_prefs = select(Preference)
            result_prefs = await session.execute(stmt_prefs)
            prefs = result_prefs.scalars().all()
            
            print(f"   OK Usuarios: {len(usuarios)}")
            print(f"   OK Items: {len(items)}")
            print(f"   OK Preferencias: {len(prefs)}")
            
            # Mostrar resumen
            print("\n" + "=" * 60)
            print("RESUMEN - DATOS DEMO CREADOS")
            print("=" * 60)
            
            for usuario in usuarios:
                print(f"\nUSUARIO: {usuario.username} (Reputacion: {usuario.reputation_score})")
                
                # Items del usuario
                stmt_user_items = select(Item).where(Item.user_id == usuario.id)
                result_user_items = await session.execute(stmt_user_items)
                user_items = result_user_items.scalars().all()
                
                for item in user_items:
                    print(f"   DA: {item.title} (EUR{item.estimated_value})")
                
                # Preferencias del usuario
                stmt_user_prefs = select(Preference).where(Preference.user_id == usuario.id)
                result_user_prefs = await session.execute(stmt_user_prefs)
                user_prefs = result_user_prefs.scalars().all()
                
                for pref in user_prefs:
                    print(f"   BUSCA: {pref.desired_item_title} (EUR{pref.min_value}-EUR{pref.max_value})")
            
            # Caso demo especial
            print("\n" + "=" * 60)
            print("CASO DEMO ESPECIAL - INTERCAMBIO CIRCULAR k=3")
            print("=" * 60)
            print("Este intercambio es IMPOSIBLE en el mercado actual (k=2):")
            print()
            print("1. Ana: iPhone EUR600 -> MacBook EUR800")
            print("   * Paga EUR212 (EUR200 diferencia + EUR12 comision 6%)")
            print()
            print("2. Carlos: MacBook EUR800 -> Bicicleta EUR400")  
            print("   * Recibe EUR376 (EUR400 diferencia - EUR24 comision 6%)")
            print()
            print("3. Beatriz: Bicicleta EUR400 -> iPhone EUR600")
            print("   * Paga EUR212 (EUR200 diferencia + EUR12 comision 6%)")
            print()
            print("SISTEMA CERRADO:")
            print("   * Total pagos: EUR424 (Ana EUR212 + Beatriz EUR212)")
            print("   * Total recepciones: EUR424 (Carlos EUR376 + Treqe EUR48 comisiones)")
            print("   * Sistema economicamente consistente OK")
            
            print("\n" + "=" * 60)
            print("DATOS DEMO LISTOS PARA PRUEBAS")
            print("=" * 60)
            print("Proximos pasos:")
            print("1. Iniciar servidor: uvicorn src.main:app --reload")
            print("2. Probar endpoint: POST /api/v1/matching/find")
            print("3. Validar que encuentra el intercambio circular k=3")
            
            return True
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Ejecutar
    resultado = asyncio.run(main())
    
    if resultado:
        print("\nOK: Datos demo creados correctamente")
        print("\nEl sistema ahora tiene 3 usuarios con:")
        print("* iPhone EUR600 -> busca MacBook EUR800")
        print("* MacBook EUR800 -> busca Bicicleta EUR400")
        print("* Bicicleta EUR400 -> busca iPhone EUR600")
        print("\nIntercambio circular perfecto k=3 listo para probar!")
    else:
        print("\nERROR creando datos demo")
        sys.exit(1)