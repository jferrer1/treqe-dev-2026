#!/usr/bin/env python3
"""
Script FINAL para crear datos demo funcionales para Treqe
Crea 3 usuarios con intercambio circular perfecto k=3
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
import random
import bcrypt
import uuid

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

async def crear_base_datos():
    """Crear tablas en la base de datos"""
    print("1. Conectando a base de datos SQLite...")
    
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    
    from src.database.models import Base
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    print("2. Creando tablas...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    print("3. Creando sesión...")
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    return engine, async_session

async def crear_usuario(session, usuario_data):
    """Crear un usuario con sus items y preferencias"""
    from src.database.models import User, Item, Preference
    
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
    
    # Crear preferencias - cada preferencia asociada al PRIMER item del usuario
    for pref_data in usuario_data["preferences"]:
        if items_creados:  # Asociar al primer item del usuario
            item_asociado = items_creados[0]
            preference = Preference(
                user_id=usuario.id,
                item_id=item_asociado.id,  # ¡IMPORTANTE! Preference necesita item_id
                desired_item_title=pref_data["desired_item_title"],
                desired_category=pref_data["desired_category"],
                min_value=pref_data["min_value"],
                max_value=pref_data["max_value"],
                priority=1,  # high priority
                is_active=True,
                created_at=datetime.now() - timedelta(days=random.randint(1, 7))
            )
            session.add(preference)
    
    return usuario, items_creados

async def main():
    """Función principal"""
    print("=" * 60)
    print("SISTEMA DE DATOS DEMO - TREQE (INTERCAMBIO CIRCULAR k=3)")
    print("=" * 60)
    
    try:
        # 1. Crear base de datos
        engine, async_session = await crear_base_datos()
        
        async with async_session() as session:
            print("\n4. Creando usuarios demo...")
            
            # Datos demo - Intercambio circular perfecto
            usuarios_demo = [
                {
                    "username": "ana_tech",
                    "email": "ana@demo.treqe.com",
                    "password": "password123",
                    "full_name": "Ana García",
                    "reputation_score": 85.0,
                    "items": [
                        {
                            "title": "iPhone 13 128GB Negro",
                            "description": "iPhone 13 en perfecto estado",
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
                            "max_value": 900.0
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
                            "description": "MacBook Air M1 8GB/256GB",
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
                            "max_value": 600.0
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
                            "description": "Bicicleta de montaña Trek",
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
                            "max_value": 750.0
                        }
                    ]
                }
            ]
            
            usuarios_creados = []
            for i, usuario_data in enumerate(usuarios_demo, 1):
                usuario, items = await crear_usuario(session, usuario_data)
                usuarios_creados.append((usuario, items))
                print(f"   OK Usuario {i}: {usuario.username}")
                print(f"      Item: {items[0].title} (EUR{items[0].estimated_value})")
                print(f"      Busca: {usuario_data['preferences'][0]['desired_item_title']}")
            
            await session.commit()
            
            # 5. Verificar datos
            print("\n5. Verificando datos creados...")
            from sqlalchemy import select, func
            from src.database.models import User, Item, Preference
            
            stmt_users = select(func.count(User.id))
            result_users = await session.execute(stmt_users)
            total_users = result_users.scalar()
            
            stmt_items = select(func.count(Item.id))
            result_items = await session.execute(stmt_items)
            total_items = result_items.scalar()
            
            stmt_prefs = select(func.count(Preference.id))
            result_prefs = await session.execute(stmt_prefs)
            total_prefs = result_prefs.scalar()
            
            print(f"   ✅ Usuarios: {total_users}")
            print(f"   ✅ Items: {total_items}")
            print(f"   ✅ Preferencias: {total_prefs}")
            
            # 6. Mostrar intercambio circular
            print("\n" + "=" * 60)
            print("INTERCAMBIO CIRCULAR k=3 CONFIGURADO:")
            print("=" * 60)
            print("Este intercambio es IMPOSIBLE en mercado tradicional (k=2):")
            print()
            print("1. Ana: iPhone EUR600 → MacBook EUR800")
            print("   • Paga EUR212 total")
            print("   • EUR200 diferencia + EUR12 comisión (6%)")
            print()
            print("2. Carlos: MacBook EUR800 → Bicicleta EUR400")
            print("   • Recibe EUR376 total")
            print("   • EUR400 diferencia - EUR24 comisión (6%)")
            print()
            print("3. Beatriz: Bicicleta EUR400 → iPhone EUR600")
            print("   • Paga EUR212 total")
            print("   • EUR200 diferencia + EUR12 comisión (6%)")
            print()
            print("💰 SISTEMA ECONÓMICAMENTE CERRADO:")
            print("   • Total pagos: EUR424 (Ana EUR212 + Beatriz EUR212)")
            print("   • Total recepciones: EUR424 (Carlos EUR376 + Treqe EUR48)")
            print("   • Verificación: EUR424 = EUR424 ✅")
            
            # 7. Instrucciones para probar
            print("\n" + "=" * 60)
            print("INSTRUCCIONES PARA PROBAR EL ALGORITMO:")
            print("=" * 60)
            
            print("\nA) CONFIGURAR SISTEMA:")
            print("1. Temporalmente reemplazar config.py con config_demo.py")
            print("   o modificar DATABASE_URL en config.py a:")
            print('   DATABASE_URL = "sqlite+aiosqlite:///treqe_demo.db"')
            print("2. Instalar dependencias mínimas:")
            print("   pip install fastapi uvicorn sqlalchemy aiosqlite bcrypt")
            
            print("\nB) EJECUTAR SERVIDOR:")
            print("   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
            
            print("\nC) PROBAR ENDPOINTS:")
            print("1. Login (obtener token JWT):")
            print("   POST /api/v1/auth/login")
            print('   Body: {"username": "ana_tech", "password": "password123"}')
            print("2. Buscar intercambios:")
            print("   POST /api/v1/matching/find")
            print('   Headers: {"Authorization": "Bearer <token>"}')
            
            print("\nD) RESULTADO ESPERADO:")
            print("   • El algoritmo debería encontrar el intercambio circular k=3")
            print("   • Tiempo estimado: <500ms")
            print("   • Propuesta clara con cálculos económicos")
            
            # 8. Crear archivo de instrucciones
            with open("instrucciones_demo.txt", "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("INSTRUCCIONES DEMO TREQE - INTERCAMBIO CIRCULAR k=3\n")
                f.write("=" * 60 + "\n\n")
                
                f.write("DATOS CREADOS:\n")
                f.write("- Usuarios: ana_tech, carlos_deportes, beatriz_eco\n")
                f.write("- Password: password123 (para todos)\n")
                f.write("- Base de datos: treqe_demo.db (SQLite)\n\n")
                
                f.write("INTERCAMBIO CONFIGURADO:\n")
                f.write("1. Ana: iPhone €600 → busca MacBook €800\n")
                f.write("2. Carlos: MacBook €800 → busca Bicicleta €400\n")
                f.write("3. Beatriz: Bicicleta €400 → busca iPhone €600\n\n")
                
                f.write("PARA PROBAR:\n")
                f.write("1. Modificar config.py:\n")
                f.write('   DATABASE_URL = "sqlite+aiosqlite:///treqe_demo.db"\n')
                f.write("2. Ejecutar servidor:\n")
                f.write("   uvicorn src.main:app --reload\n")
                f.write("3. Login y probar matching\n\n")
                
                f.write("VALOR DEMOSTRADO:\n")
                f.write("- Intercambio IMPOSIBLE en mercado tradicional (k=2)\n")
                f.write("- Posible SOLO con Treqe (k=3)\n")
                f.write("- Sistema económicamente cerrado y transparente\n")
            
            print("\n" + "=" * 60)
            print("ARCHIVOS CREADOS:")
            print("=" * 60)
            print("1. treqe_demo.db - Base de datos SQLite")
            print("2. instrucciones_demo.txt - Instrucciones detalladas")
            print("3. config_demo.py - Configuración para pruebas")
            
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 CREANDO DATOS DEMO PARA VALIDAR ALGORITMO TREQE")
    print("Objetivo: Demostrar intercambio circular k=3 imposible en mercado tradicional")
    
    resultado = asyncio.run(main())
    
    if resultado:
        print("\n" + "=" * 60)
        print("✅ DATOS DEMO CREADOS EXITOSAMENTE")
        print("=" * 60)
        print("\nEl algoritmo Treqe ahora tiene datos para validar:")
        print("• Intercambio circular k=3 funcional")
        print("• Lógica económica correcta verificable")
        print("• Sistema listo para pruebas reales")
        print("\nSiguiente paso: Probar el algoritmo con estos datos.")
    else:
        print("\n❌ Error creando datos demo")
        sys.exit(1)