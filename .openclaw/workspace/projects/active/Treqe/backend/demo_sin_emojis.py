#!/usr/bin/env python3
"""
Script FINAL sin emojis para crear datos demo funcionales
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

async def main():
    """Función principal"""
    print("=" * 60)
    print("SISTEMA DE DATOS DEMO - TREQE (INTERCAMBIO CIRCULAR k=3)")
    print("=" * 60)
    
    try:
        # Importar módulos
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import select, func
        
        from src.database.models import Base, User, Item, Preference
        
        print("1. Conectando a SQLite...")
        engine = create_async_engine(DATABASE_URL, echo=False)
        
        print("2. Creando tablas...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
        print("3. Creando sesion...")
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with async_session() as session:
            print("4. Creando usuarios demo...")
            
            # Datos demo - Intercambio circular perfecto
            usuarios_demo = [
                {
                    "username": "ana_tech",
                    "email": "ana@demo.treqe.com",
                    "password": "password123",
                    "full_name": "Ana Garcia",
                    "reputation_score": 85.0,
                    "items": [
                        {
                            "title": "iPhone 13 128GB Negro",
                            "description": "iPhone 13 en perfecto estado",
                            "category": "Electronica",
                            "estimated_value": 600.0,
                            "condition": "Excelente"
                        }
                    ],
                    "preferences": [
                        {
                            "desired_item_title": "MacBook Air M1",
                            "desired_category": "Electronica",
                            "min_value": 700.0,
                            "max_value": 900.0
                        }
                    ]
                },
                {
                    "username": "carlos_deportes",
                    "email": "carlos@demo.treqe.com",
                    "password": "password123",
                    "full_name": "Carlos Martinez",
                    "reputation_score": 72.0,
                    "items": [
                        {
                            "title": "MacBook Air M1 2020",
                            "description": "MacBook Air M1 8GB/256GB",
                            "category": "Electronica",
                            "estimated_value": 800.0,
                            "condition": "Excelente"
                        }
                    ],
                    "preferences": [
                        {
                            "desired_item_title": "Bicicleta de montana",
                            "desired_category": "Deportes",
                            "min_value": 350.0,
                            "max_value": 600.0
                        }
                    ]
                },
                {
                    "username": "beatriz_eco",
                    "email": "beatriz@demo.treqe.com",
                    "password": "password123",
                    "full_name": "Beatriz Lopez",
                    "reputation_score": 65.0,
                    "items": [
                        {
                            "title": "Bicicleta Trek Marlin 5",
                            "description": "Bicicleta de montana Trek",
                            "category": "Deportes",
                            "estimated_value": 400.0,
                            "condition": "Bueno"
                        }
                    ],
                    "preferences": [
                        {
                            "desired_item_title": "iPhone 13 o 14",
                            "desired_category": "Electronica",
                            "min_value": 550.0,
                            "max_value": 750.0
                        }
                    ]
                }
            ]
            
            for i, usuario_data in enumerate(usuarios_demo, 1):
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
                
                # Crear items del usuario
                items_creados = []
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
                    await session.flush()
                    items_creados.append(item)
                
                # Crear preferencias - cada preferencia asociada al PRIMER item
                for pref_data in usuario_data["preferences"]:
                    if items_creados:
                        item_asociado = items_creados[0]
                        preference = Preference(
                            user_id=usuario.id,
                            item_id=item_asociado.id,  # IMPORTANTE: Preference necesita item_id
                            desired_item_title=pref_data["desired_item_title"],
                            desired_category=pref_data["desired_category"],
                            min_value=pref_data["min_value"],
                            max_value=pref_data["max_value"],
                            priority=1,
                            is_active=True,
                            created_at=datetime.now() - timedelta(days=random.randint(1, 7))
                        )
                        session.add(preference)
                
                print(f"   OK Usuario {i}: {usuario.username}")
                print(f"      Item: {items_creados[0].title} (EUR{items_creados[0].estimated_value})")
                print(f"      Busca: {usuario_data['preferences'][0]['desired_item_title']}")
            
            await session.commit()
            
            # Verificar datos
            print("\n5. Verificando datos creados...")
            
            stmt_users = select(func.count(User.id))
            result_users = await session.execute(stmt_users)
            total_users = result_users.scalar()
            
            stmt_items = select(func.count(Item.id))
            result_items = await session.execute(stmt_items)
            total_items = result_items.scalar()
            
            stmt_prefs = select(func.count(Preference.id))
            result_prefs = await session.execute(stmt_prefs)
            total_prefs = result_prefs.scalar()
            
            print(f"   OK Usuarios: {total_users}")
            print(f"   OK Items: {total_items}")
            print(f"   OK Preferencias: {total_prefs}")
            
            # Mostrar intercambio circular
            print("\n" + "=" * 60)
            print("INTERCAMBIO CIRCULAR k=3 CONFIGURADO:")
            print("=" * 60)
            print("Este intercambio es IMPOSIBLE en mercado tradicional (k=2):")
            print()
            print("1. Ana: iPhone EUR600 -> MacBook EUR800")
            print("   * Paga EUR212 total")
            print("   * EUR200 diferencia + EUR12 comision (6%)")
            print()
            print("2. Carlos: MacBook EUR800 -> Bicicleta EUR400")
            print("   * Recibe EUR376 total")
            print("   * EUR400 diferencia - EUR24 comision (6%)")
            print()
            print("3. Beatriz: Bicicleta EUR400 -> iPhone EUR600")
            print("   * Paga EUR212 total")
            print("   * EUR200 diferencia + EUR12 comision (6%)")
            print()
            print("SISTEMA ECONOMICAMENTE CERRADO:")
            print("   * Total pagos: EUR424 (Ana EUR212 + Beatriz EUR212)")
            print("   * Total recepciones: EUR424 (Carlos EUR376 + Treqe EUR48)")
            print("   * Verificacion: EUR424 = EUR424 OK")
            
            # Instrucciones
            print("\n" + "=" * 60)
            print("INSTRUCCIONES PARA PROBAR:")
            print("=" * 60)
            
            print("\n1. Configurar sistema:")
            print("   Modificar config.py (linea DATABASE_URL):")
            print('   DATABASE_URL = "sqlite+aiosqlite:///treqe_demo.db"')
            
            print("\n2. Ejecutar servidor:")
            print("   uvicorn src.main:app --reload")
            
            print("\n3. Probar endpoints:")
            print("   POST /api/v1/auth/login")
            print('   Body: {"username": "ana_tech", "password": "password123"}')
            print("   POST /api/v1/matching/find")
            print('   Headers: {"Authorization": "Bearer <token>"}')
            
            print("\n4. Resultado esperado:")
            print("   * Algoritmo encuentra intercambio circular k=3")
            print("   * Tiempo <500ms")
            print("   * Propuesta con calculos economicos claros")
            
            # Crear archivo de instrucciones
            with open("instrucciones_demo.txt", "w") as f:
                f.write("=" * 60 + "\n")
                f.write("INSTRUCCIONES DEMO TREQE\n")
                f.write("=" * 60 + "\n\n")
                f.write("USUARIOS:\n")
                f.write("- ana_tech / password123\n")
                f.write("- carlos_deportes / password123\n")
                f.write("- beatriz_eco / password123\n\n")
                f.write("INTERCAMBIO CONFIGURADO (k=3):\n")
                f.write("1. Ana: iPhone 600 -> MacBook 800\n")
                f.write("2. Carlos: MacBook 800 -> Bicicleta 400\n")
                f.write("3. Beatriz: Bicicleta 400 -> iPhone 600\n\n")
                f.write("PARA PROBAR:\n")
                f.write("1. Cambiar DATABASE_URL en config.py a SQLite\n")
                f.write("2. uvicorn src.main:app --reload\n")
                f.write("3. Login y probar matching\n")
            
            print("\n" + "=" * 60)
            print("ARCHIVOS CREADOS:")
            print("=" * 60)
            print("1. treqe_demo.db - Base de datos SQLite")
            print("2. instrucciones_demo.txt - Instrucciones")
            
            return True
            
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("CREANDO DATOS DEMO PARA VALIDAR ALGORITMO TREQE")
    print("Objetivo: Demostrar intercambio circular k=3")
    
    resultado = asyncio.run(main())
    
    if resultado:
        print("\n" + "=" * 60)
        print("EXITO: DATOS DEMO CREADOS")
        print("=" * 60)
        print("\nEl algoritmo Treqe ahora tiene datos para validar.")
        print("Intercambio circular k=3 listo para probar.")
        print("\nSiguiente paso: Probar el algoritmo con estos datos.")
    else:
        print("\nERROR creando datos demo")
        sys.exit(1)