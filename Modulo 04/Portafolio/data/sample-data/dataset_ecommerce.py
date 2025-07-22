#!/usr/bin/env python3
"""
Dataset Generator for E-commerce Database Project
Generates realistic sample data for testing our polyglot architecture

Features:
- 50,000 customers with realistic profiles
- 10,000 products across 25 categories
- 200,000 orders with multiple items
- 1M+ events and user interactions
- 500,000 reviews and ratings
"""

import pandas as pd
import numpy as np
import json
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
import os
from typing import Dict, List, Any

# Initialize Faker for realistic data
fake = Faker(['en_US', 'es_ES'])
Faker.seed(42)
np.random.seed(42)
random.seed(42)

class EcommerceDataGenerator:
    """Generate realistic e-commerce data for multiple database types"""
    
    def __init__(self):
        self.fake = fake
        self.customers = []
        self.products = []
        self.orders = []
        self.order_items = []
        self.reviews = []
        self.events = []
        self.categories = self._generate_categories()
        
    def _generate_categories(self) -> List[Dict]:
        """Generate product categories"""
        categories = [
            {'id': 1, 'name': 'Electronics', 'parent_id': None},
            {'id': 2, 'name': 'Clothing', 'parent_id': None},
            {'id': 3, 'name': 'Books', 'parent_id': None},
            {'id': 4, 'name': 'Home & Garden', 'parent_id': None},
            {'id': 5, 'name': 'Sports & Outdoors', 'parent_id': None},
            {'id': 6, 'name': 'Beauty & Personal Care', 'parent_id': None},
            {'id': 7, 'name': 'Toys & Games', 'parent_id': None},
            {'id': 8, 'name': 'Automotive', 'parent_id': None},
            {'id': 9, 'name': 'Food & Beverages', 'parent_id': None},
            {'id': 10, 'name': 'Health & Wellness', 'parent_id': None},
            
            # Subcategories
            {'id': 11, 'name': 'Smartphones', 'parent_id': 1},
            {'id': 12, 'name': 'Laptops', 'parent_id': 1},
            {'id': 13, 'name': 'Headphones', 'parent_id': 1},
            {'id': 14, 'name': 'Cameras', 'parent_id': 1},
            {'id': 15, 'name': 'Men\'s Clothing', 'parent_id': 2},
            {'id': 16, 'name': 'Women\'s Clothing', 'parent_id': 2},
            {'id': 17, 'name': 'Shoes', 'parent_id': 2},
            {'id': 18, 'name': 'Fiction', 'parent_id': 3},
            {'id': 19, 'name': 'Non-Fiction', 'parent_id': 3},
            {'id': 20, 'name': 'Textbooks', 'parent_id': 3},
            {'id': 21, 'name': 'Furniture', 'parent_id': 4},
            {'id': 22, 'name': 'Kitchen & Dining', 'parent_id': 4},
            {'id': 23, 'name': 'Garden Tools', 'parent_id': 4},
            {'id': 24, 'name': 'Exercise Equipment', 'parent_id': 5},
            {'id': 25, 'name': 'Outdoor Gear', 'parent_id': 5},
        ]
        return categories
    
    def generate_customers(self, num_customers: int = 50000) -> pd.DataFrame:
        """Generate customer data for MySQL"""
        print(f"Generating {num_customers} customers...")
        
        customer_segments = ['Bronze', 'Silver', 'Gold', 'Platinum']
        countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Spain', 'Italy', 'Australia']
        
        for i in range(num_customers):
            if i % 10000 == 0:
                print(f"  Generated {i} customers...")
                
            registration_date = self.fake.date_between(start_date='-3y', end_date='today')
            
            customer = {
                'customer_id': i + 1,
                'email': self.fake.unique.email(),
                'password_hash': self.fake.sha256(),
                'first_name': self.fake.first_name(),
                'last_name': self.fake.last_name(),
                'phone': self.fake.phone_number(),
                'date_of_birth': self.fake.date_of_birth(minimum_age=18, maximum_age=80),
                'gender': random.choice(['M', 'F', 'O']),
                'country': random.choice(countries),
                'city': self.fake.city(),
                'postal_code': self.fake.postcode(),
                'address_line1': self.fake.street_address(),
                'address_line2': self.fake.secondary_address() if random.random() < 0.3 else None,
                'customer_segment': random.choice(customer_segments),
                'lifetime_value': round(random.uniform(50, 5000), 2),
                'total_orders': random.randint(0, 50),
                'registration_date': registration_date,
                'last_login': self.fake.date_between(start_date=registration_date, end_date='today'),
                'is_active': random.choice([True, False], weights=[0.85, 0.15]),
                'created_at': registration_date,
                'updated_at': self.fake.date_between(start_date=registration_date, end_date='today')
            }
            self.customers.append(customer)
        
        print(f"✅ Generated {len(self.customers)} customers")
        return pd.DataFrame(self.customers)
    
    def generate_products(self, num_products: int = 10000) -> pd.DataFrame:
        """Generate product data for MySQL and MongoDB"""
        print(f"Generating {num_products} products...")
        
        brands = ['Apple', 'Samsung', 'Nike', 'Adidas', 'Amazon', 'Sony', 'LG', 'Dell', 
                 'HP', 'Canon', 'Nikon', 'Zara', 'H&M', 'Levi\'s', 'Gucci', 'Prada']
        
        product_names = {
            11: ['iPhone 15', 'Galaxy S24', 'Pixel 8', 'OnePlus 12'],
            12: ['MacBook Pro', 'ThinkPad X1', 'XPS 13', 'Surface Laptop'],
            13: ['AirPods Pro', 'Sony WH-1000XM4', 'Bose QuietComfort'],
            14: ['Canon EOS R5', 'Nikon D850', 'Sony A7R IV'],
            15: ['Men\'s Jeans', 'Dress Shirt', 'Casual T-Shirt'],
            16: ['Women\'s Dress', 'Blouse', 'Leggings'],
            17: ['Running Shoes', 'Boots', 'Sneakers'],
            18: ['Fiction Novel', 'Mystery Book', 'Romance Novel'],
            19: ['Biography', 'Self-Help', 'History Book'],
            20: ['Math Textbook', 'Science Textbook', 'Literature']
        }
        
        for i in range(num_products):
            if i % 2000 == 0:
                print(f"  Generated {i} products...")
                
            category = random.choice([c for c in self.categories if c['parent_id'] is not None])
            category_id = category['id']
            
            base_names = product_names.get(category_id, ['Generic Product'])
            base_name = random.choice(base_names)
            
            product = {
                'product_id': i + 1,
                'sku': f"{category['name'][:3].upper()}-{i+1:06d}",
                'name': f"{random.choice(brands)} {base_name}",
                'description': self.fake.text(max_nb_chars=500),
                'category_id': category_id,
                'category_name': category['name'],
                'brand': random.choice(brands),
                'price': round(random.uniform(10, 2000), 2),
                'cost': round(random.uniform(5, 1000), 2),
                'weight': round(random.uniform(0.1, 50), 2),
                'dimensions': f"{random.randint(1,50)}x{random.randint(1,50)}x{random.randint(1,50)}",
                'color': random.choice(['Black', 'White', 'Silver', 'Blue', 'Red', 'Green']),
                'size': random.choice(['XS', 'S', 'M', 'L', 'XL', 'XXL', None]),
                'stock_quantity': random.randint(0, 1000),
                'reorder_level': random.randint(10, 100),
                'supplier_id': random.randint(1, 100),
                'rating_average': round(random.uniform(1, 5), 2),
                'rating_count': random.randint(0, 1000),
                'is_active': random.choice([True, False], weights=[0.9, 0.1]),
                'is_featured': random.choice([True, False], weights=[0.1, 0.9]),
                'created_at': self.fake.date_between(start_date='-2y', end_date='today'),
                'updated_at': self.fake.date_between(start_date='-1y', end_date='today')
            }
            self.products.append(product)
        
        print(f"✅ Generated {len(self.products)} products")
        return pd.DataFrame(self.products)
    
    def generate_orders(self, num_orders: int = 200000) -> tuple:
        """Generate order data for MySQL"""
        print(f"Generating {num_orders} orders...")
        
        order_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        payment_methods = ['credit_card', 'debit_card', 'paypal', 'apple_pay', 'google_pay']
        
        for i in range(num_orders):
            if i % 20000 == 0:
                print(f"  Generated {i} orders...")
                
            customer = random.choice(self.customers)
            order_date = self.fake.date_between(start_date='-2y', end_date='today')
            
            # Generate order items
            num_items = random.randint(1, 5)
            order_total = 0
            current_order_items = []
            
            for item_num in range(num_items):
                product = random.choice(self.products)
                quantity = random.randint(1, 3)
                unit_price = product['price']
                item_total = unit_price * quantity
                order_total += item_total
                
                order_item = {
                    'order_item_id': len(self.order_items) + item_num + 1,
                    'order_id': i + 1,
                    'product_id': product['product_id'],
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_price': item_total,
                    'created_at': order_date
                }
                current_order_items.append(order_item)
            
            # Add shipping and tax
            shipping_cost = round(random.uniform(0, 25), 2)
            tax_amount = round(order_total * 0.08, 2)  # 8% tax
            final_total = order_total + shipping_cost + tax_amount
            
            order = {
                'order_id': i + 1,
                'customer_id': customer['customer_id'],
                'order_date': order_date,
                'order_status': random.choice(order_statuses),
                'payment_method': random.choice(payment_methods),
                'payment_status': random.choice(['pending', 'completed', 'failed']),
                'subtotal': round(order_total, 2),
                'shipping_cost': shipping_cost,
                'tax_amount': tax_amount,
                'total_amount': round(final_total, 2),
                'shipping_address': f"{customer['address_line1']}, {customer['city']}, {customer['country']}",
                'billing_address': f"{customer['address_line1']}, {customer['city']}, {customer['country']}",
                'created_at': order_date,
                'updated_at': self.fake.date_between(start_date=order_date, end_date='today')
            }
            
            self.orders.append(order)
            self.order_items.extend(current_order_items)
        
        print(f"✅ Generated {len(self.orders)} orders with {len(self.order_items)} items")
        return pd.DataFrame(self.orders), pd.DataFrame(self.order_items)
    
    def generate_reviews(self, num_reviews: int = 500000) -> pd.DataFrame:
        """Generate review data for MongoDB"""
        print(f"Generating {num_reviews} reviews...")
        
        review_titles = [
            "Great product!", "Excellent quality", "Highly recommended", 
            "Perfect for my needs", "Amazing value", "Love it!", 
            "Not what I expected", "Could be better", "Disappointed",
            "Fantastic!", "Best purchase ever", "Good quality"
        ]
        
        for i in range(num_reviews):
            if i % 50000 == 0:
                print(f"  Generated {i} reviews...")
                
            customer = random.choice(self.customers)
            product = random.choice(self.products)
            rating = random.randint(1, 5)
            
            # Generate more positive reviews for higher ratings
            if rating >= 4:
                title = random.choice(review_titles[:6])
                helpful_votes = random.randint(0, 100)
            else:
                title = random.choice(review_titles[6:])
                helpful_votes = random.randint(0, 20)
            
            review = {
                'review_id': i + 1,
                'product_id': product['product_id'],
                'customer_id': customer['customer_id'],
                'rating': rating,
                'title': title,
                'content': self.fake.text(max_nb_chars=1000),
                'helpful_votes': helpful_votes,
                'total_votes': helpful_votes + random.randint(0, 50),
                'is_verified_purchase': random.choice([True, False], weights=[0.7, 0.3]),
                'created_at': self.fake.date_between(start_date='-2y', end_date='today'),
                'updated_at': self.fake.date_between(start_date='-1y', end_date='today')
            }
            self.reviews.append(review)
        
        print(f"✅ Generated {len(self.reviews)} reviews")
        return pd.DataFrame(self.reviews)
    
    def generate_events(self, num_events: int = 1000000) -> pd.DataFrame:
        """Generate event data for Cassandra"""
        print(f"Generating {num_events} events...")
        
        event_types = [
            'page_view', 'product_view', 'add_to_cart', 'remove_from_cart',
            'search', 'checkout_start', 'checkout_complete', 'login',
            'logout', 'register', 'add_to_wishlist', 'share_product',
            'review_submit', 'filter_products', 'sort_products'
        ]
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0'
        ]
        
        for i in range(num_events):
            if i % 100000 == 0:
                print(f"  Generated {i} events...")
                
            customer = random.choice(self.customers)
            event_type = random.choice(event_types)
            
            # Generate realistic event data based on type
            event_data = {'event_type': event_type}
            
            if event_type in ['product_view', 'add_to_cart', 'remove_from_cart']:
                event_data['product_id'] = random.choice(self.products)['product_id']
            elif event_type == 'search':
                event_data['search_query'] = self.fake.word()
                event_data['results_count'] = random.randint(0, 500)
            elif event_type == 'checkout_complete':
                event_data['order_id'] = random.choice(self.orders)['order_id']
                event_data['amount'] = round(random.uniform(10, 500), 2)
            
            event = {
                'event_id': str(uuid.uuid4()),
                'user_id': customer['customer_id'],
                'session_id': str(uuid.uuid4()),
                'event_type': event_type,
                'event_data': json.dumps(event_data),
                'timestamp': self.fake.date_time_between(start_date='-1y', end_date='now'),
                'ip_address': self.fake.ipv4(),
                'user_agent': random.choice(user_agents),
                'page_url': f"https://ecommerce.com/{self.fake.uri_path()}",
                'referrer': f"https://{self.fake.domain_name()}" if random.random() < 0.3 else None,
                'device_type': random.choice(['desktop', 'mobile', 'tablet']),
                'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
                'os': random.choice(['Windows', 'macOS', 'iOS', 'Android', 'Linux'])
            }
            self.events.append(event)
        
        print(f"✅ Generated {len(self.events)} events")
        return pd.DataFrame(self.events)
    
    def generate_mongodb_products(self) -> List[Dict]:
        """Generate MongoDB-specific product documents"""
        print("Generating MongoDB product documents...")
        
        mongo_products = []
        
        for product in self.products:
            # Get related reviews for this product
            product_reviews = [r for r in self.reviews if r['product_id'] == product['product_id']]
            
            # Get category hierarchy
            category = next(c for c in self.categories if c['id'] == product['category_id'])
            parent_category = None
            if category['parent_id']:
                parent_category = next(c for c in self.categories if c['id'] == category['parent_id'])
            
            # Generate specifications based on category
            specifications = self._generate_product_specifications(product['category_id'])
            
            mongo_product = {
                '_id': product['product_id'],
                'sku': product['sku'],
                'name': product['name'],
                'description': product['description'],
                'category': {
                    'id': category['id'],
                    'name': category['name'],
                    'parent_id': category['parent_id'],
                    'parent_name': parent_category['name'] if parent_category else None,
                    'path': f"{parent_category['name']}/{category['name']}" if parent_category else category['name']
                },
                'brand': product['brand'],
                'pricing': {
                    'base_price': product['price'],
                    'cost': product['cost'],
                    'discount_percentage': random.uniform(0, 30) if random.random() < 0.3 else 0,
                    'currency': 'USD'
                },
                'specifications': specifications,
                'inventory': {
                    'stock_quantity': product['stock_quantity'],
                    'reorder_level': product['reorder_level'],
                    'supplier_id': product['supplier_id'],
                    'warehouse_location': random.choice(['NYC', 'LAX', 'CHI', 'ATL'])
                },
                'media': {
                    'images': [
                        f"https://cdn.ecommerce.com/products/{product['sku']}/image1.jpg",
                        f"https://cdn.ecommerce.com/products/{product['sku']}/image2.jpg"
                    ],
                    'videos': [
                        f"https://cdn.ecommerce.com/products/{product['sku']}/demo.mp4"
                    ] if random.random() < 0.2 else []
                },
                'seo': {
                    'meta_title': f"{product['name']} - Best Price Online",
                    'meta_description': product['description'][:150],
                    'keywords': [product['brand'].lower(), category['name'].lower(), 'buy online']
                },
                'ratings': {
                    'average': product['rating_average'],
                    'count': product['rating_count'],
                    'distribution': {
                        '5': random.randint(0, 100),
                        '4': random.randint(0, 50),
                        '3': random.randint(0, 30),
                        '2': random.randint(0, 20),
                        '1': random.randint(0, 10)
                    }
                },
                'reviews': [
                    {
                        'review_id': r['review_id'],
                        'customer_id': r['customer_id'],
                        'rating': r['rating'],
                        'title': r['title'],
                        'content': r['content'],
                        'helpful_votes': r['helpful_votes'],
                        'created_at': r['created_at'].isoformat() if hasattr(r['created_at'], 'isoformat') else str(r['created_at'])
                    } for r in product_reviews[:5]  # Include top 5 reviews
                ],
                'tags': self._generate_product_tags(product, category),
                'related_products': random.sample([p['product_id'] for p in self.products], min(5, len(self.products))),
                'status': 'active' if product['is_active'] else 'inactive',
                'featured': product['is_featured'],
                'created_at': product['created_at'].isoformat() if hasattr(product['created_at'], 'isoformat') else str(product['created_at']),
                'updated_at': product['updated_at'].isoformat() if hasattr(product['updated_at'], 'isoformat') else str(product['updated_at'])
            }
            
            mongo_products.append(mongo_product)
        
        print(f"✅ Generated {len(mongo_products)} MongoDB product documents")
        return mongo_products
    
    def _generate_product_specifications(self, category_id: int) -> Dict:
        """Generate category-specific product specifications"""
        specs = {}
        
        if category_id == 11:  # Smartphones
            specs = {
                'display': {
                    'size': f"{random.uniform(5.0, 7.0):.1f} inches",
                    'resolution': random.choice(['1080x2340', '1170x2532', '1440x3200']),
                    'technology': random.choice(['OLED', 'Super AMOLED', 'IPS LCD'])
                },
                'processor': {
                    'brand': random.choice(['Apple', 'Qualcomm', 'Samsung', 'MediaTek']),
                    'model': f"A{random.randint(14, 18)} Bionic" if random.random() < 0.3 else f"Snapdragon {random.randint(800, 900)}",
                    'cores': random.choice([6, 8, 10])
                },
                'memory': {
                    'ram': random.choice(['4GB', '6GB', '8GB', '12GB', '16GB']),
                    'storage': random.choice(['64GB', '128GB', '256GB', '512GB', '1TB'])
                },
                'camera': {
                    'main': f"{random.randint(12, 108)}MP",
                    'ultra_wide': f"{random.randint(8, 16)}MP",
                    'telephoto': f"{random.randint(8, 12)}MP" if random.random() < 0.7 else None
                },
                'battery': f"{random.randint(3000, 5000)}mAh",
                'connectivity': ['5G', 'WiFi 6', 'Bluetooth 5.0', 'NFC']
            }
        elif category_id == 12:  # Laptops
            specs = {
                'display': {
                    'size': f"{random.uniform(13.0, 17.0):.1f} inches",
                    'resolution': random.choice(['1920x1080', '2560x1440', '3840x2160']),
                    'panel_type': random.choice(['IPS', 'OLED', 'TN'])
                },
                'processor': {
                    'brand': random.choice(['Intel', 'AMD', 'Apple']),
                    'model': random.choice(['Core i5', 'Core i7', 'Ryzen 5', 'Ryzen 7', 'M1', 'M2']),
                    'generation': random.randint(10, 13)
                },
                'memory': {
                    'ram': random.choice(['8GB', '16GB', '32GB', '64GB']),
                    'storage': random.choice(['256GB SSD', '512GB SSD', '1TB SSD', '2TB SSD'])
                },
                'graphics': random.choice(['Integrated', 'NVIDIA RTX 3060', 'NVIDIA RTX 4070', 'AMD Radeon']),
                'weight': f"{random.uniform(1.0, 3.0):.1f} kg",
                'battery_life': f"{random.randint(6, 15)} hours"
            }
        elif category_id in [15, 16]:  # Clothing
            specs = {
                'material': random.choice(['Cotton', '100% Cotton', 'Polyester', 'Cotton Blend', 'Wool', 'Silk']),
                'fit': random.choice(['Slim', 'Regular', 'Loose', 'Tight']),
                'care_instructions': 'Machine wash cold, tumble dry low',
                'origin': random.choice(['Made in USA', 'Made in China', 'Made in Vietnam', 'Made in India']),
                'size_guide': 'US sizing'
            }
        
        return specs
    
    def _generate_product_tags(self, product: Dict, category: Dict) -> List[str]:
        """Generate search and filter tags for products"""
        tags = [
            product['brand'].lower(),
            category['name'].lower(),
            product['color'].lower() if product['color'] else None,
            product['size'].lower() if product['size'] else None,
            'featured' if product['is_featured'] else None,
            'sale' if random.random() < 0.2 else None,
            'bestseller' if product['rating_average'] > 4.0 else None,
            'new' if random.random() < 0.1 else None
        ]
        
        # Remove None values
        tags = [tag for tag in tags if tag is not None]
        
        return tags
    
    def generate_dynamodb_sessions(self, num_sessions: int = 100000) -> List[Dict]:
        """Generate DynamoDB session data"""
        print(f"Generating {num_sessions} user sessions...")
        
        sessions = []
        
        for i in range(num_sessions):
            if i % 10000 == 0:
                print(f"  Generated {i} sessions...")
                
            customer = random.choice(self.customers)
            session_start = self.fake.date_time_between(start_date='-30d', end_date='now')
            session_duration = random.randint(60, 7200)  # 1 minute to 2 hours
            
            session = {
                'user_id': str(customer['customer_id']),
                'session_id': str(uuid.uuid4()),
                'session_start': int(session_start.timestamp()),
                'session_end': int(session_start.timestamp()) + session_duration,
                'device_info': {
                    'device_type': random.choice(['desktop', 'mobile', 'tablet']),
                    'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
                    'os': random.choice(['Windows', 'macOS', 'iOS', 'Android']),
                    'screen_resolution': random.choice(['1920x1080', '1366x768', '375x667', '414x896'])
                },
                'location': {
                    'country': customer['country'],
                    'city': customer['city'],
                    'ip_address': self.fake.ipv4()
                },
                'pages_visited': random.randint(1, 20),
                'actions_taken': random.randint(0, 10),
                'cart_value': round(random.uniform(0, 500), 2) if random.random() < 0.3 else 0,
                'referrer': random.choice([
                    'google.com', 'facebook.com', 'direct', 'email', 'twitter.com'
                ]),
                'ttl': int((session_start + timedelta(days=30)).timestamp())  # 30 days TTL
            }
            
            sessions.append(session)
        
        print(f"✅ Generated {len(sessions)} sessions")
        return sessions
    
    def save_data_to_files(self, output_dir: str = 'data'):
        """Save all generated data to files"""
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/sample-data", exist_ok=True)
        os.makedirs(f"{output_dir}/processed", exist_ok=True)
        
        print(f"Saving data to {output_dir}...")
        
        # Save CSV files for relational databases
        if self.customers:
            pd.DataFrame(self.customers).to_csv(f"{output_dir}/sample-data/customers.csv", index=False)
            
        if self.products:
            pd.DataFrame(self.products).to_csv(f"{output_dir}/sample-data/products.csv", index=False)
            
        if self.orders:
            pd.DataFrame(self.orders).to_csv(f"{output_dir}/sample-data/orders.csv", index=False)
            
        if self.order_items:
            pd.DataFrame(self.order_items).to_csv(f"{output_dir}/sample-data/order_items.csv", index=False)
            
        if self.reviews:
            pd.DataFrame(self.reviews).to_csv(f"{output_dir}/sample-data/reviews.csv", index=False)
            
        if self.events:
            pd.DataFrame(self.events).to_csv(f"{output_dir}/sample-data/events.csv", index=False)
        
        # Save categories
        pd.DataFrame(self.categories).to_csv(f"{output_dir}/sample-data/categories.csv", index=False)
        
        # Save JSON files for NoSQL databases
        mongo_products = self.generate_mongodb_products()
        with open(f"{output_dir}/sample-data/products_mongodb.json", 'w') as f:
            json.dump(mongo_products, f, indent=2, default=str)
        
        # Save DynamoDB session data
        sessions = self.generate_dynamodb_sessions()
        with open(f"{output_dir}/sample-data/sessions_dynamodb.json", 'w') as f:
            json.dump(sessions, f, indent=2, default=str)
        
        print("✅ All data saved successfully!")
        
        # Print summary
        print("\n" + "="*50)
        print("DATA GENERATION SUMMARY")
        print("="*50)
        print(f"Customers: {len(self.customers):,}")
        print(f"Products: {len(self.products):,}")
        print(f"Orders: {len(self.orders):,}")
        print(f"Order Items: {len(self.order_items):,}")
        print(f"Reviews: {len(self.reviews):,}")
        print(f"Events: {len(self.events):,}")
        print(f"Categories: {len(self.categories):,}")
        print(f"MongoDB Products: {len(mongo_products):,}")
        print(f"DynamoDB Sessions: {len(sessions):,}")
        print("="*50)

def main():
    """Main function to generate all e-commerce data"""
    generator = EcommerceDataGenerator()
    
    # Generate all data
    generator.generate_customers(50000)
    generator.generate_products(10000)
    generator.generate_orders(200000)
    generator.generate_reviews(500000)
    generator.generate_events(1000000)
    
    # Save to files
    generator.save_data_to_files()
    
    print("\n🎉 E-commerce dataset generation completed!")
    print("Ready to use with the polyglot database architecture!")

if __name__ == "__main__":
    main()