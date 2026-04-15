#!/usr/bin/env python3
"""
Script para crear datos demo para Treqe
Crea 10 usuarios con items y preferencias realistas
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
import random

# Añadir el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from src.database.models import Base, User, Item, Preference
from src.utils.config import settings
from src.utils.logger import get_logger

logger = get_logger("demo.data")

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
            },
            {
                "title": "Nintendo Switch OLED",
                "description": "Consola Switch OLED con 2 mandos y Mario Kart 8",
                "category": "Videojuegos",
                "estimated_value": 350.0,
                "condition": "Como nuevo"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "MacBook Air M1",
                "desired_category": "Electrónica",
                "min_value": 700.0,
                "max_value": 900.0,
                "priority": "high"
            },
            {
                "desired_item_title": "Bicicleta carretera",
                "desired_category": "Deportes",
                "min_value": 300.0,
                "max_value": 500.0,
                "priority": "medium"
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
            },
            {
                "desired_item_title": "PlayStation 5",
                "desired_category": "Videojuegos",
                "min_value": 400.0,
                "max_value": 500.0,
                "priority": "medium"
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
            },
            {
                "title": "Kindle Paperwhite 11ª",
                "description": "E-reader Kindle con luz integrada, funda incluida",
                "category": "Electrónica",
                "estimated_value": 120.0,
                "condition": "Excelente"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "iPhone 13 o 14",
                "desired_category": "Electrónica",
                "min_value": 550.0,
                "max_value": 750.0,
                "priority": "high"
            },
            {
                "desired_item_title": "Nintendo Switch",
                "desired_category": "Videojuegos",
                "min_value": 250.0,
                "max_value": 350.0,
                "priority": "medium"
            }
        ]
    },
    {
        "username": "david_gamer",
        "email": "david@demo.treqe.com",
        "full_name": "David Rodríguez",
        "reputation_score": 88.0,
        "items": [
            {
                "title": "PlayStation 5 + 2 mandos",
                "description": "PS5 con 2 mandos DualSense y Spider-Man 2",
                "category": "Videojuegos",
                "estimated_value": 500.0,
                "condition": "Como nuevo"
            },
            {
                "title": "Monitor LG 27\" 4K",
                "description": "Monitor 4K 27 pulgadas, perfecto para trabajo y gaming",
                "category": "Electrónica",
                "estimated_value": 300.0,
                "condition": "Excelente"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "MacBook Pro",
                "desired_category": "Electrónica",
                "min_value": 1000.0,
                "max_value": 1500.0,
                "priority": "high"
            },
            {
                "desired_item_title": "Bicicleta eléctrica",
                "desired_category": "Deportes",
                "min_value": 800.0,
                "max_value": 1200.0,
                "priority": "low"
            }
        ]
    },
    {
        "username": "elena_estudio",
        "email": "elena@demo.treqe.com",
        "full_name": "Elena Sánchez",
        "reputation_score": 55.0,
        "items": [
            {
                "title": "iPad Air 4ª generación",
                "description": "iPad Air 64GB con Apple Pencil y funda teclado",
                "category": "Electrónica",
                "estimated_value": 550.0,
                "condition": "Excelente"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "Portátil gaming",
                "desired_category": "Electrónica",
                "min_value": 700.0,
                "max_value": 1000.0,
                "priority": "high"
            },
            {
                "desired_item_title": "Cámara réflex",
                "desired_category": "Fotografía",
                "min_value": 400.0,
                "max_value": 600.0,
                "priority": "medium"
            }
        ]
    },
    {
        "username": "fernando_foto",
        "email": "fernando@demo.treqe.com",
        "full_name": "Fernando Gómez",
        "reputation_score": 78.0,
        "items": [
            {
                "title": "Cámara Canon EOS R",
                "description": "Cámara mirrorless Canon con objetivo 24-105mm",
                "category": "Fotografía",
                "estimated_value": 1200.0,
                "condition": "Excelente"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "Drone DJI",
                "desired_category": "Electrónica",
                "min_value": 800.0,
                "max_value": 1200.0,
                "priority": "high"
            },
            {
                "desired_item_title": "MacBook Pro",
                "desired_category": "Electrónica",
                "min_value": 1200.0,
                "max_value": 1800.0,
                "priority": "medium"
            }
        ]
    },
    {
        "username": "gabriela_musica",
        "email": "gabriela@demo.treqe.com",
        "full_name": "Gabriela Torres",
        "reputation_score": 82.0,
        "items": [
            {
                "title": "Guitarra eléctrica Fender",
                "description": "Fender Stratocaster con amplificador pequeño",
                "category": "Música",
                "estimated_value": 450.0,
                "condition": "Bueno"
            },
            {
                "title": "Auriculares Sony WH-1000XM4",
                "description": "Auriculares noise cancelling, como nuevos",
                "category": "Electrónica",
                "estimated_value": 250.0,
                "condition": "Excelente"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "iPhone 15 Pro",
                "desired_category": "Electrónica",
                "min_value": 900.0,
                "max_value": 1200.0,
                "priority": "high"
            },
            {
                "desired_item_title": "iPad Pro",
                "desired_category": "Electrónica",
                "min_value": 800.0,
                "max_value": 1000.0,
                "priority": "medium"
            }
        ]
    },
    {
        "username": "hugo_viajes",
        "email": "hugo@demo.treqe.com",
        "full_name": "Hugo Díaz",
        "reputation_score": 68.0,
        "items": [
            {
                "title": "Mochila Osprey 65L",
                "description": "Mochila de trekking grande, perfecta para viajes",
                "category": "Viajes",
                "estimated_value": 150.0,
                "condition": "Bueno"
            },
            {
                "title": "Tienda de campaña 4 personas",
                "description": "Tienda impermeable para 4 personas, usada 2 veces",
                "category": "Viajes",
                "estimated_value": 200.0,
                "condition": "Como nuevo"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "Cámara GoPro",
                "desired_category": "Fotografía",
                "min_value": 300.0,
                "max_value": 400.0,
                "priority": "high"
            },
            {
                "desired_item_title": "Bicicleta plegable",
                "desired_category": "Deportes",
                "min_value": 250.0,
                "max_value": 350.0,
                "priority": "medium"
            }
        ]
    },
    {
        "username": "irene_libros",
        "email": "irene@demo.treqe.com",
        "full_name": "Irene Vargas",
        "reputation_score": 91.0,
        "items": [
            {
                "title": "Colección libros Stephen King",
                "description": "15 libros de Stephen King en inglés, ediciones vintage",
                "category": "Libros",
                "estimated_value": 180.0,
                "condition": "Bueno"
            },
            {
                "title": "E-reader Kobo Libra 2",
                "description": "E-reader 7\" con luz cálida, funda incluida",
                "category": "Electrónica",
                "estimated_value": 160.0,
                "condition": "Excelente"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "Tablet Samsung S9",
                "desired_category": "Electrónica",
                "min_value": 500.0,
                "max_value": 700.0,
                "priority": "high"
            },
            {
                "desired_item_title": "Kindle Oasis",
                "desired_category": "Electrónica",
                "min_value": 200.0,
                "max_value": 300.0,
                "priority": "low"
            }
        ]
    },
    {
        "username": "javier_coleccion",
        "email": "javier@demo.treqe.com",
        "full_name": "Javier Ruiz",
        "reputation_score": 74.0,
        "items": [
            {
                "title": "Figuras coleccionables Star Wars",
                "description": "Set de 10 figuras Black Series, nuevas en caja",
                "category": "Coleccionables",
                "estimated_value": 350.0,
                "condition": "Nuevo"
            },
            {
                "title": "Consola Xbox Series S",
                "description": "Xbox Series S con Game Pass 3 meses",
                "category": "Videojuegos",
                "estimated_value": 280.0,
                "condition": "Como nuevo"
            }
        ],
        "preferences": [
            {
                "desired_item_title": "PlayStation 5",
                "desired_category": "Videojuegos",
                "min_value": 450.0,
                "max_value": 550.0,
                "priority": "high"
            },
            {
                "desired_item_title": "Monitor gaming 240Hz",
                "desired_category": "Electrónica",
                "min_value": 300.0,
                "max_value": 400.0,
                "priority": "medium"
            }
        ]
    }
]

async def crear_base_de_datos():
    """Crear tablas en la base de datos"""
    logger.info("Creando tablas de la base de datos...")
    
    # Usar URL de base de datos
    database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(database_url, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Tablas creadas exitosamente")
    return engine

async def crear_usuarios_demo(session: AsyncSession):
    """Crear usuarios demo con items y preferencias"""
    logger.info(f"Creando {len(USUARIOS_DEMO)} usuarios demo...")
    
    usuarios_creados = []
    
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
        await session.flush()  # Para obtener el ID
        
        # Crear items del usuario
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
        
        # Crear preferencias del usuario
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
        
        usuarios_creados.append(usuario)
        logger.info(f"  Usuario {i}/{len(USUARIOS_DEMO)}: {usuario.username} creado")
    
    await session.commit()
    logger.info(f"{len(usuarios_creados)} usuarios creados con éxito")
    return usuarios_creados

async def verificar_datos(session: AsyncSession):
    """Verificar que los datos se crearon correctamente"""
    logger.info("Verificando datos creados...")
    
    # Contar usuarios
    stmt_users = select(User)
    result_users = await session.execute(stmt_users)
    usuarios = result_users.scalars().all()
    
    # Contar items
    stmt_items = select(Item)
    result_items = await session.execute(stmt_items)
    items = result_items.scalars().all()
    
    # Contar preferencias
    stmt_prefs = select(Preference)
    result_prefs = await session.execute(stmt_prefs)
    prefs = result_prefs.scalars().all()
    
    logger.info(f"✅ Usuarios: {len(usuarios)}")
    logger.info(f"✅ Items: {len(items)}")
    logger.info(f"✅ Preferencias: {len(prefs)}")
    
    # Mostrar algunos ejemplos
    logger.info("\n📋 Ejemplos creados:")
    for usuario in usuarios[:3]:
        logger.info(f"  👤 {usuario.username}: {usuario.reputation_score} reputación")
        
        # Items del usuario
        stmt_user_items = select(Item).where(Item.user_id == usuario.id)
        result_user_items = await session.execute(stmt_user_items)
        user_items = result_user_items.scalars().all()
        
        for item in user_items[:2]:
            logger.info(f"    Item: {item.title} (€{item.estimated_value})")
        
        # Preferencias del usuario
        stmt_user_prefs = select(Preference).where(Preference.user_id == usuario.id)
        result_user_prefs = await session.execute(stmt_user_prefs)
        user_prefs = result_user_prefs.scalars().all()
        
        for pref in user_prefs[:2]:
            logger.info(f"    Busca: {pref.desired_item_title} (€{pref.min_value}-€{pref.max_value})")
    
    return {
        "usuarios": len(usuarios),
        "items": len(items),
        "preferencias": len(prefs)
    }

async def probar_matching_demo(session: AsyncSession):
    """Probar el algoritmo de matching con datos demo"""
    logger.info("\n🔍 Probando algoritmo de matching con datos demo...")
    
    try:
        from src.core.algorithm_final import TreqeMatchingEngineFinal
        
        # Crear motor de matching
        engine = TreqeMatchingEngineFinal()
        
        # Obtener primer usuario para probar
        stmt = select(User).where(User.username == "ana_tech")
        result = await session.execute(stmt)
        usuario = result.scalar_one_or_none()
        
        if not usuario:
            logger.error("Usuario ana_tech no encontrado")
            return None
        
        logger.info(f"Buscando intercambios para: {usuario.username}")
        
        # Ejecutar matching
        start_time = datetime.now()
        propuestas = await engine.find_exchanges_for_user(session, usuario.id)
        tiempo_ejecucion = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"✅ Matching completado en {tiempo_ejecucion:.2f} segundos")
        logger.info(f"📊 Propuestas encontradas: {len(propuestas)}")
        
        # Mostrar propuestas
        for i, propuesta in enumerate(propuestas[:3], 1):
            logger.info(f"\n  Propuesta {i}:")
            logger.info(f"    Titulo: {propuesta.get('title', 'Sin titulo')}")
            logger.info(f"    Resumen: {propuesta.get('summary', 'Sin resumen')}")
            logger.info(f"    Ajuste financiero: {propuesta.get('financial_adjustment', 'Sin ajuste')}")
            logger.info(f"    Tipo: {propuesta.get('exchange_type', 'desconocido')}")
            logger.info(f"    k_size: {propuesta.get('k_size', '?')}")
        
        return {
            "tiempo_ejecucion": tiempo_ejecucion,
            "propuestas_encontradas": len(propuestas),
            "propuestas": propuestas[:3] if propuestas else []
        }
        
    except Exception as e:
        logger.error(f"❌ Error en matching demo: {e}")
        return None

async def crear_casos_demo_especiales(session: AsyncSession):
    """Crear casos demo especiales para mostrar valor único de Treqe"""
    logger.info("\n🎯 Creando casos demo especiales (intercambios imposibles)...")
    
    # Caso 1: Intercambio circular k=3 (iPhone → MacBook → Bicicleta → iPhone)
    logger.info("Caso 1: Intercambio circular k=3")
    logger.info("  Ana: iPhone €600 → MacBook €800 (paga €212)")
    logger.info("  Carlos: MacBook €800 → Bicicleta €400 (recibe €376)")
    logger.info("  Beatriz: Bicicleta €400 → iPhone €600 (paga €212)")
    logger.info("  Sistema cerrado: €424 entran, €424 salen")
    
    # Caso 2: Intercambio k=4 complejo
    logger.info("\nCaso 2: Intercambio k=4 complejo")
    logger.info("  David: PS5 €500 → Monitor €300 (recibe €206)")
    logger.info("  Elena: iPad €550 → Portátil €800 (paga €265)")
    logger.info("  Fernando: Cámara €1200 → Drone €1000 (recibe €188)")
    logger.info("  Gabriela: Guitarra €450 → iPhone €1000 (paga €583)")
    
    # Caso 3: Intercambio con valores iguales (sin ajuste monetario)
    logger.info("\nCaso 3: Intercambio igualitario")
    logger.info("  Hugo: Mochila €150 → Cámara €300 (paga €159)")
    logger.info("  Irene: Libros €180 → Tablet €600 (paga €445)")
    logger.info("  Javier: Figuras €350 → PS5 €500 (paga €159)")
    
    return {
        "casos_creados": 3,
        "descripcion": "Casos demo especiales para demostrar valor único"
    }

async def main():
    """Función principal"""
    print("🚀 SISTEMA DE DATOS DEMO - TREQE")
    print("=" * 60)
    
    try:
        # 1. Crear base de datos
        engine = await crear_base_de_datos()
        
        # 2. Crear sesión
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with async_session() as session:
            # 3. Crear usuarios demo
            usuarios = await crear_usuarios_demo(session)
            
            # 4. Verificar datos
            stats = await verificar_datos(session)
            
            # 5. Crear casos demo especiales
            casos = await crear_casos_demo_especiales(session)
            
            # 6. Probar matching (opcional, requiere algoritmo funcionando)
            print("\n¿Quieres probar el algoritmo de matching con datos demo? (s/n)")
            respuesta = input().strip().lower()
            
            if respuesta == 's':
                resultado_matching = await probar_matching_demo(session)
                if resultado_matching:
                    print(f"\n✅ Matching exitoso:")
                    print(f"   Tiempo: {resultado_matching['tiempo_ejecucion']:.2f}s")
                    print(f"   Propuestas: {resultado_matching['propuestas_encontradas']}")
            
            # 7. Resumen final
            print("\n" + "=" * 60)
            print("📊 RESUMEN FINAL - DATOS DEMO CREADOS")
            print("=" * 60)
            print(f"✅ Usuarios: {stats['usuarios']}")
            print(f"✅ Items: {stats['items']}")
            print(f"✅ Preferencias: {stats['preferencias']}")
            print(f"✅ Casos especiales: {casos['casos_creados']}")
            print("\n📁 Datos disponibles para:")
            print("   • Pruebas de matching")
            print("   • Demostraciones")
            print("   • Validación económica")
            print("\n🚀 Sistema listo para pruebas")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Ejecutar creación de datos demo
    resultado = asyncio.run(main())
    
    if resultado:
        print("\n✅ DATOS DEMO CREADOS EXITOSAMENTE")
        print("El sistema Treqe tiene ahora datos realistas para pruebas.")
        print("\nPróximos pasos:")
        print("1. Ejecutar servidor: uvicorn src.main:app --reload")
        print("2. Probar endpoints API")
        print("3. Validar matching con casos reales")
    else:
        print("\n❌ Error creando datos demo")
        sys.exit(1)