#!/usr/bin/env python3
"""
Script FINAL para crear datos demo - con password hash
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
import random
import bcrypt

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Usar SQLite para pruebas
DATABASE_URL = "sqlite+aiosqlite:///treqe_demo.db"

# Función para hash de password
def hash_password(password: str) -> str:
    """Hash de password usando bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Datos demo realistas con passwords
USUARIOS_DEMO = [
    {
        "username": "ana_tech",
        "email": "ana@demo.treqe.com",
        "password": "password123",  # En producción usar passwords seguras
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
        "password": "password123",
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
        "password": "password123",
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
    print("SISTEMA DE DATOS DEMO - TREQE (FINAL)")
    print("=" * 60)
    
    try:
        # Importar módulos
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import select
        
        from src.database.models import Base, User, Item, Preference
        
        print("1. Conectando a SQLite...")
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
                # Hash password
                password_hash = hash_password(usuario_data["password"])
                
                # Crear usuario
                usuario = User(
                    username=usuario_data["username"],
                    email=usuario_data["email"],
                    password_hash=password_hash,
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
            print("ARCHIVOS CREADOS:")
            print("=" * 60)
            print("1. treqe_demo.db - Base de datos SQLite con datos demo")
            print("2. Modelos: 3 usuarios, 3 items, 3 preferencias")
            print("3. Passwords: 'password123' para todos los usuarios demo")
            
            print("\n" + "=" * 60)
            print("PRUEBAS RECOMENDADAS:")
            print("=" * 60)
            print("1. Para usar estos datos, modificar config.py:")
            print("   DATABASE_URL = 'sqlite+aiosqlite:///treqe_demo.db'")
            print("2. Iniciar servidor: uvicorn src.main:app --reload")
            print("3. Login con:")
            print("   - Usuario: ana_tech / carlos_deportes / beatriz_eco")
            print("   - Password: password123")
            print("4. Probar endpoint: POST /api/v1/matching/find")
            
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
        print("\n" + "=" * 60)
        print("EXITO: Datos demo creados correctamente")
        print("=" * 60)
        print("\nRESUMEN DEL SISTEMA CREADO:")
        print("1. Base de datos: treqe_demo.db")
        print("2. 3 usuarios con passwords hasheados")
        print("3. Intercambio circular k=3 configurado:")
        print("   * Ana: iPhone -> busca MacBook")
        print("   * Carlos: MacBook -> busca Bicicleta")
        print("   * Beatriz: Bicicleta -> busca iPhone")
        print("\nPARA PROBAR EL ALGORITMO:")
        print("1. Instalar dependencias: pip install -r requirements.txt")
        print("2. Modificar config.py para usar SQLite")
        print("3. Ejecutar: uvicorn src.main:app --reload")
        print("4. Probar matching con datos demo")
    else:
        print("\nERROR creando datos demo")
        sys.exit(1)