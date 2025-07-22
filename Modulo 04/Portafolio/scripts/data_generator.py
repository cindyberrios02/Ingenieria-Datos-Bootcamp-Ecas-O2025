#!/usr/bin/env python3
"""
=========================================
GENERADOR DE DATOS DE PRUEBA
E-commerce Database Sample Data Generator
=========================================
"""

import random
import json
import csv
from datetime import datetime, timedelta
from faker import Faker
import psycopg2
from pymongo import MongoClient
import os
import uuid

# Configuración
fake = Faker(['es_ES', 'en_US'])
random.seed(42)  # Para resultados reproducibles

# Configuración de base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ecommerce_db',
    'user': 'ecommerce_user',
    'password': 'secure_password_123'
}

MONGO_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'ecommerce_nosql'
}

class DataGenerator:
    def __init__(self):
        self.pg_conn = None
        self.mongo_client = None
        self.mongo_db = None
        self.categories = []
        self.products = []
        self.users = []
        
    def connect_postgresql(self):
        """Conectar a PostgreSQL"""
        try:
            self.pg_conn = psycopg2.connect(**DB_CONFIG)
            print("✅ Conectado a PostgreSQL")
        except Exception as e:
            print(f"❌ Error conectando a PostgreSQL: {e}")
            
    def connect_mongodb(self):
        """Conectar a MongoDB"""
        try:
            self.mongo_client = MongoClient(MONGO_CONFIG['host'], MONGO_CONFIG['port'])
            self.mongo_db = self.mongo_client[MONGO_CONFIG['database']]
            print("✅ Conectado a MongoDB")
        except Exception as e:
            print(f"❌ Error conectando a MongoDB: {e}")
    
    def generate_categories(self, num_categories=20):
        """Generar categorías de productos"""
        categories_data = [
            {'name': 'Electrónicos', 'description': 'Dispositivos electrónicos y gadgets'},
            {'name': 'Ropa y Accesorios', 'description': 'Prendas de vestir y accesorios de moda'},
            {'name': 'Hogar y Jardín', 'description': 'Artículos para el hogar, muebles y jardín'},
            {'name': 'Deportes y Fitness', 'description': 'Equipamiento deportivo y de fitness'},
            {'name': 'Libros y Medios', 'description': 'Libros, música, películas y videojuegos'},
            {'name': 'Salud y Belleza', 'description': 'Productos de cuidado personal y salud'},
            {'name': 'Juguetes y Juegos', 'description': 'Juguetes para niños y juegos de mesa'},
            {'name': 'Automóviles', 'description': 'Accesorios y repuestos para automóviles'},
            {'name': 'Mascotas', 'description': 'Productos para el cuidado de mascotas'},
            {'name': 'Oficina y Papelería', 'description': 'Suministros de oficina y papelería'}
        ]
        
        # Agregar subcategorías
        for i in range(num_categories - len(categories_data)):
            parent_category = random.choice(categories_data[:5])
            subcategory = {
                'name': f"{parent_category['name']} - {fake.word().title()}",
                'description': f"Subcategoría de {parent_category['name']}",
                'parent_category': parent_category['name']
            }
            categories_data.append(subcategory)
        
        return categories_data
    
    def generate_users(self, num_users=1000):
        """Generar usuarios"""
        users_data = []
        
        for _ in range(num_users):
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
            user = {
                'email': fake.unique.email(),
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'phone': fake.phone_number()[:20],
                'birth_date': birth_date,
                'gender': random.choice(['M', 'F', 'Other']),
                'created_at': fake.date_time_between(start_date='-2y', end_date='now'),
                'is_active': random.choice([True, True, True, False])  # 75% activos
            }
            users_data.append(user)
        
        return users_data
    
    def generate_products(self, categories, num_products=500):
        """Generar productos"""
        products_data = []
        product_names = [
            'Smartphone', 'Laptop', 'Tablet', 'Auriculares', 'Cámara',
            'Camiseta', 'Pantalón', 'Zapatos', 'Chaqueta', 'Vestido',
            'Silla', 'Mesa', 'Lámpara', 'Cojín', 'Espejo',
            'Pelota', 'Raqueta', 'Pesas', 'Bicicleta', 'Casco',
            'Libro', 'Revista', 'CD', 'DVD', 'Videojuego'
        ]
        
        for i in range(num_products):
            category = random.choice(categories)
            base_name = random.choice(product_names)
            
            # Precio basado en categoría
            if 'Electrónicos' in category['name']:
                price = round(random.uniform(50, 2000), 2)
            elif 'Ropa' in category['name']:
                price = round(random.uniform(10, 200), 2)
            elif 'Hogar' in category['name']:
                price = round(random.uniform(20, 500), 2)
            else:
                price = round(random.uniform(5, 300), 2)
            
            product = {
                'category_id': categories.index(category) + 1,
                'name': f"{base_name} {fake.color_name()} {fake.random_number(digits=3)}",
                'description': fake.text(max_nb_chars=200),
                'price': price,
                'cost': round(price * random.uniform(0.4, 0.7), 2),
                'sku': f"{base_name.upper()[:4]}-{fake.random_number(digits=6)}",
                'weight': round(random.uniform(0.1, 5.0), 3),
                'dimensions': {
                    'width': round(random.uniform(5, 50), 2),
                    'height': round(random.uniform(5, 50), 2),
                    'depth': round(random.uniform(1, 30), 2)
                },
                'is_active': random.choice([True, True, True, False]),
                'created_at': fake.date_time_between(start_date='-1y', end_date='now')
            }
            products_data.append(product)
        
        return products_data
    
    def generate_orders(self, users, products, num_orders=2000):
        """Generar pedidos"""
        orders_data = []
        order_items_data = []
        
        for i in range(num_orders):
            user = random.choice(users)
            order_date = fake.date_time_between(start_date='-6m', end_date='now')
            
            # Número de items en el pedido
            num_items = random.choices([1, 2, 3, 4, 5], weights=[30, 25, 20, 15, 10])[0]
            order_products = random.sample(products, num_items)
            
            subtotal = 0
            order_items = []
            
            for product in order_products:
                quantity = random.randint(1, 3)
                unit_price = product['price'] * random.uniform(0.9, 1.1)  # Variación de precio
                total_price = round(quantity * unit_price, 2)
                subtotal += total_price
                
                order_item = {
                    'order_id': i + 1,
                    'product_id': products.index(product) + 1,
                    'quantity': quantity,
                    'unit_price': round(unit_price, 2),
                    'total_price': total_price
                }
                order_items.append(order_item)
            
            tax_rate = 0.1  # 10% de impuestos
            tax_amount = round(subtotal * tax_rate, 2)
            shipping_cost = 0 if subtotal > 50 else 10  # Envío gratis por compras > $50
            discount_amount = round(subtotal * random.uniform(0, 0.1), 2) if random.random() < 0.2 else 0
            
            total_amount = subtotal + tax_amount + shipping_cost - discount_amount
            
            order = {
                'user_id': users.index(user) + 1,
                'order_number': f"ORD-{order_date.strftime('%Y%m%d')}-{str(i+1).zfill(6)}",
                'status': random.choices(
                    ['pending', 'processing', 'shipped', 'delivered', 'cancelled'],
                    weights=[5, 10, 15, 65, 5]
                )[0],
                'subtotal': round(subtotal, 2),
                'tax_amount': tax_amount,
                'shipping_cost': shipping_cost,
                'discount_amount': discount_amount,
                'total_amount': round(total_amount, 2),
                'payment_status': random.choices(
                    ['pending', 'paid', 'failed'],
                    weights=[5, 90, 5]
                )[0],
                'created_at': order_date
            }
            
            orders_data.append(order)
            order_items_data.extend(order_items)
        
        return orders_data, order_items_data
    
    def generate_mongodb_data(self, users, products):
        """Generar datos para MongoDB"""
        
        # Perfiles de usuario enriquecidos
        user_profiles = []
        for i, user in enumerate(users[:100]):  # Solo primeros 100 usuarios
            profile = {
                'user_id': i + 1,
                'email': user['email'],
                'personal_info': {
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'birth_date': user['birth_date'].isoformat() if user['birth_date'] else None,
                    'gender': user['gender'],
                    'phone': user['phone']
                },
                'preferences': {
                    'categories': random.sample([cat['name'] for cat in self.categories[:5]], k=random.randint(1, 3)),
                    'brands': [fake.company() for _ in range(random.randint(1, 4))],
                    'price_range': {
                        'min': random.randint(10, 50),
                        'max': random.randint(100, 1000)
                    },
                    'notifications': {
                        'email': random.choice([True, False]),
                        'sms': random.choice([True, False]),
                        'push': random.choice([True, False])
                    }
                },
                'address_history': [
                    {
                        'street': fake.street_address(),
                        'city': fake.city(),
                        'state': fake.state(),
                        'postal_code': fake.postcode(),
                        'country': fake.country(),
                        'type': random.choice(['home', 'work', 'other']),
                        'is_current': True,
                        'created_at': fake.date_time_between(start_date='-2y', end_date='now').isoformat()
                    }
                ],
                'social_profiles': {
                    'facebook': fake.url() if random.choice([True, False]) else None,
                    'twitter': f"@{fake.user_name()}" if random.choice([True, False]) else None,
                    'instagram': f"@{fake.user_name()}" if random.choice([True, False]) else None
                },
                'loyalty_program': {
                    'member_since': fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
                    'points': random.randint(0, 5000),
                    'tier': random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']),
                    'total_spent': round(random.uniform(100, 10000), 2)
                },
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            user_profiles.append(profile)
        
        # Catálogo de productos enriquecido
        products_catalog = []
        for i, product in enumerate(products[:50]):  # Solo primeros 50 productos
            catalog_item = {
                'product_id': i + 1,
                'sku': product['sku'],
                'name': product['name'],
                'description': product['description'],
                'category': self.categories[product['category_id'] - 1]['name'],
                'price': product['price'],
                'currency': 'USD',
                'brand': fake.company(),
                'tags': [fake.word() for _ in range(random.randint(3, 7))],
                'specifications': {
                    'color': fake.color_name(),
                    'material': random.choice(['Cotton', 'Polyester', 'Leather', 'Metal', 'Plastic', 'Wood']),
                    'size': random.choice(['XS', 'S', 'M', 'L', 'XL', 'XXL']) if 'Ropa' in self.categories[product['category_id'] - 1]['name'] else None,
                    'weight': f"{product['weight']} kg",
                    'dimensions': product['dimensions']
                },
                'images': [
                    f"https://example.com/images/{product['sku']}-1.jpg",
                    f"https://example.com/images/{product['sku']}-2.jpg",
                    f"https://example.com/images/{product['sku']}-3.jpg"
                ],
                'reviews_summary': {
                    'average_rating': round(random.uniform(3.0, 5.0), 1),
                    'total_reviews': random.randint(0, 500),
                    'rating_distribution': {
                        '5': random.randint(0, 200),
                        '4': random.randint(0, 150),
                        '3': random.randint(0, 100),
                        '2': random.randint(0, 50),
                        '1': random.randint(0, 25)
                    }
                },
                'seo': {
                    'meta_title': f"{product['name']} | TuTienda Online",
                    'meta_description': product['description'][:160],
                    'keywords': [fake.word() for _ in range(5)]
                },
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            products_catalog.append(catalog_item)
        
        # Sesiones de usuario
        user_sessions = []
        for _ in range(500):
            session_start = fake.date_time_between(start_date='-30d', end_date='now')
            session_duration = random.randint(30, 3600)  # 30 segundos a 1 hora
            
            session = {
                'session_id': str(uuid.uuid4()),
                'user_id': random.randint(1, min(100, len(users))),
                'session_start': session_start.isoformat(),
                'session_end': (session_start + timedelta(seconds=session_duration)).isoformat(),
                'pages_visited': [
                    {
                        'url': f"/product/{random.randint(1, 50)}",
                        'timestamp': fake.date_time_between(start_date=session_start, end_date=session_start + timedelta(seconds=session_duration)).isoformat(),
                        'time_spent': random.randint(10, 300)
                    }
                    for _ in range(random.randint(1, 10))
                ],
                'device_info': {
                    'user_agent': fake.user_agent(),
                    'device_type': random.choice(['desktop', 'mobile', 'tablet']),
                    'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
                    'os': random.choice(['Windows', 'macOS', 'iOS', 'Android', 'Linux'])
                },
                'location': {
                    'ip_address': fake.ipv4(),
                    'country': fake.country(),
                    'city': fake.city()
                },
                'created_at': datetime.utcnow().isoformat()
            }
            user_sessions.append(session)
        
        return user_profiles, products_catalog, user_sessions
    
    def insert_postgresql_data(self, categories, users, products, orders, order_items):
        """Insertar datos en PostgreSQL"""
        if not self.pg_conn:
            print("❌ No hay conexión a PostgreSQL")
            return
        
        cursor = self.pg_conn.cursor()
        
        try:
            # Insertar categorías
            print("📝 Insertando categorías en PostgreSQL...")
            for category in categories:
                cursor.execute("""
                    INSERT INTO categories (name, description) 
                    VALUES (%s, %s)
                """, (category['name'], category['description']))
            
            # Insertar usuarios
            print("👥 Insertando usuarios en PostgreSQL...")
            for user in users:
                cursor.execute("""
                    INSERT INTO users (email, first_name, last_name, phone, birth_date, gender, created_at, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    user['email'], user['first_name'], user['last_name'],
                    user['phone'], user['birth_date'], user['gender'],
                    user['created_at'], user['is_active']
                ))
            
            # Insertar productos
            print("📦 Insertando productos en PostgreSQL...")
            for product in products:
                cursor.execute("""
                    INSERT INTO products (category_id, name, description, price, cost, sku, weight, dimensions, is_active, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    product['category_id'], product['name'], product['description'],
                    product['price'], product['cost'], product['sku'],
                    product['weight'], json.dumps(product['dimensions'