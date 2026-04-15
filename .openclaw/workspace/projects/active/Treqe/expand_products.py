import json
import random
from copy import deepcopy

# Cargar el demo_data.json actual
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'demo_data.json')
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extraer categorías, subcategorías, usuarios
categories = data['categories']
users = data['users']
existing_products = data['products']

# Mapear categorías por slug para fácil acceso
category_by_slug = {cat['slug']: cat for cat in categories}

# Listas de ayuda
cities = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Málaga", "Zaragoza", "Murcia", "Alicante", "Palma de Mallorca", "Las Palmas", "Granada", "Vigo", "Gijón", "Santander", "Logroño", "Pamplona", "Santiago de Compostela", "Toledo", "Córdoba"]
conditions = ["new", "like-new", "used", "refurbished"]

# Títulos de producto por categoría
product_titles = {
    "motor": ["Coche eléctrico", "Moto deportiva", "Furgoneta de trabajo", "Coche familiar", "Coche deportivo", "Coche clásico", "Ciclocomotor", "Quad", "Patinete eléctrico", "Caravana"],
    "moda-accesorios": ["Abrigo de invierno", "Vestido de fiesta", "Bolso de diseñador", "Zapatos de cuero", "Gafas de sol premium", "Reloj inteligente", "Collar de plata", "Chaqueta vaquera", "Falda midi", "Cinturón de piel"],
    "tecnologia": ["Portátil gaming", "Tablet Android", "Smartphone flagship", "Smart TV 4K", "Auriculares inalámbricos", "Altavoz inteligente", "Monitor gaming", "Teclado mecánico", "Ratón gaming", "Impresora 3D"],
    "hogar-jardin": ["Sofá modular", "Mesa de centro", "Lámpara de diseño", "Cafetera espresso", "Robot aspirador", "Cortacésped robot", "Hamaca de jardín", "Barbacoa de gas", "Set de herramientas", "Macetero inteligente"],
    "deporte-ocio": ["Bicicleta de montaña", "Cinta de correr", "Set de golf", "Tabla de surf", "Raqueta de tenis", "Pesas rusas", "Colchoneta yoga", "Mochila senderismo", "Canoa inflable", "Dron deportivo"],
    "bebes-ninos": ["Cuna convertible", "Carrito de bebé", "Silla de paseo", "Juego de bloques", "Puzzle educativo", "Triciclo", "Casa de juegos", "Mesa de actividades", "Ropa recién nacido", "Set de baño"],
    "inmobiliaria": ["Apartamento estudio", "Casa adosada", "Local comercial", "Trastero 5m²", "Garaje privado", "Oficina coworking", "Terreno urbano", "Finca rústica", "Chalet independiente", "Ático con vistas"],
    "servicios": ["Clases de idiomas", "Servicio de limpieza", "Diseño web", "Asesoría fiscal", "Catering eventos", "Traducción técnica", "Cuidado de mayores", "Transporte de mudanzas", "Marketing digital", "Coaching personal"],
    "cultura-entretenimiento": ["Guitarra acústica", "Violín profesional", "Colección de cómics", "Piano digital", "Kit de pintura", "Libros de arte", "Consola retro", "Vinilos raros", "Cámara de vídeo", "Easel profesional"],
    "industria-profesional": ["Máquina de soldar", "Generador eléctrico", "Andamio profesional", "Compresor de aire", "Taladro de columna", "Sierra circular", "Carretilla elevadora", "Equipo de protección", "Software CAD", "Licencia profesional"]
}

# Descripciones genéricas
descriptions = [
    "En perfecto estado, con todos los accesorios originales.",
    "Poco uso, prácticamente como nuevo. Mantenimiento al día.",
    "Producto de alta gama, ideal para profesionales.",
    "Excelente relación calidad-precio. Oportunidad única.",
    "Vendido por cambio de necesidades. Funciona perfectamente.",
    "Con factura de compra y garantía restante.",
    "Bien cuidado, siempre almacenado en lugar seguro.",
    "Listo para usar. Incluye manuales y accesorios.",
    "Producto exclusivo, difícil de encontrar en el mercado.",
    "Perfecto para principiantes o aficionados avanzados."
]

# Generar 80 productos nuevos
new_products = []
start_id = len(existing_products) + 1

for i in range(start_id, start_id + 80):
    # Seleccionar categoría aleatoria
    category = random.choice(categories)
    category_slug = category['slug']
    subcategory = random.choice(category['subcategories'])
    
    # Seleccionar usuario aleatorio
    user = random.choice(users)
    
    # Generar título basado en categoría
    if category_slug in product_titles:
        base_title = random.choice(product_titles[category_slug])
    else:
        base_title = f"Producto {category['name']}"
    
    # Añadir detalles al título
    detail = random.choice(["2024", "Premium", "Profesional", "De lujo", "Económico", "Compacto", "Portátil", "Inteligente", "Sostenible", "Certificado"])
    title = f"{base_title} {detail}"
    
    # Generar valor según categoría
    if category_slug == "motor":
        value = random.randint(5000, 50000)
    elif category_slug == "inmobiliaria":
        value = random.randint(10000, 300000)
    elif category_slug == "moda-accesorios":
        value = random.randint(50, 2000)
    elif category_slug == "tecnologia":
        value = random.randint(200, 3000)
    else:
        value = random.randint(100, 5000)
    
    # Redondear a múltiplos de 10 o 100
    if value >= 1000:
        value = round(value / 100) * 100
    else:
        value = round(value / 10) * 10
    
    # Crear producto
    product = {
        "id": i,
        "title": title,
        "category": category_slug,
        "subcategory": subcategory,
        "value": value,
        "city": random.choice(cities),
        "userId": user['id'],
        "description": random.choice(descriptions),
        "condition": random.choice(conditions),
        "wantedCategory": random.choice([c['slug'] for c in categories if c['slug'] != category_slug]),
        "wantedSubcategory": random.choice([sc for sc in category_by_slug[category_slug]['subcategories'] if sc != subcategory]),
        "wantedValueRange": [max(1, int(value * 0.7)), int(value * 1.3)]
    }
    
    new_products.append(product)

# Añadir nuevos productos a la lista existente
data['products'].extend(new_products)

# Actualizar estadísticas (aumentar usuarios totales, intercambios, etc.)
data['stats']['totalUsers'] = 3850  # Aumentado
data['stats']['totalExchanges'] = 842  # Aumentado
data['stats']['valueCreated'] = 2258000  # Aumentado

# Guardar como nuevo archivo
output_file = os.path.join(current_dir, 'demo_data_expanded.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Generados {len(new_products)} productos nuevos.")
print(f"Total productos: {len(data['products'])}")
print(f"Guardado en: {output_file}")