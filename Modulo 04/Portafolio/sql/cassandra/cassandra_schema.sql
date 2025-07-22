-- =========================================
-- CASSANDRA SCHEMA Y QUERIES
-- E-commerce Events & Analytics
-- =========================================

-- Crear keyspace
CREATE KEYSPACE IF NOT EXISTS ecommerce_events 
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 3
};

USE ecommerce_events;

-- =========================================
-- 1. TABLA DE EVENTOS DE USUARIO
-- =========================================

-- Tabla principal para eventos de usuario (particionada por fecha)
CREATE TABLE IF NOT EXISTS user_events (
    event_date date,
    event_time timestamp,
    event_id uuid,
    user_id int,
    session_id text,
    event_type text,
    page_url text,
    referrer text,
    user_agent text,
    ip_address inet,
    device_type text,
    browser text,
    os text,
    country text,
    city text,
    event_data map<text, text>,
    PRIMARY KEY (event_date, event_time, event_id)
) WITH CLUSTERING ORDER BY (event_time DESC, event_id ASC)
AND comment = 'Eventos de usuario particionados por fecha'
AND gc_grace_seconds = 864000; -- 10 días

-- Tabla para consultas por usuario específico
CREATE TABLE IF NOT EXISTS user_events_by_user (
    user_id int,
    event_time timestamp,
    event_id uuid,
    event_date date,
    session_id text,
    event_type text,
    page_url text,
    event_data map<text, text>,
    PRIMARY KEY (user_id, event_time, event_id)
) WITH CLUSTERING ORDER BY (event_time DESC, event_id ASC)
AND comment = 'Eventos indexados por usuario';

-- Tabla para análisis por tipo de evento
CREATE TABLE IF NOT EXISTS events_by_type (
    event_type text,
    event_date date,
    event_time timestamp,
    event_id uuid,
    user_id int,
    session_id text,
    event_data map<text, text>,
    PRIMARY KEY (event_type, event_date, event_time, event_id)
) WITH CLUSTERING ORDER BY (event_date DESC, event_time DESC, event_id ASC)
AND comment = 'Eventos agrupados por tipo';

-- =========================================
-- 2. TABLA DE TRANSACCIONES HISTÓRICAS
-- =========================================

CREATE TABLE IF NOT EXISTS transaction_history (
    transaction_date date,
    transaction_time timestamp,
    transaction_id uuid,
    user_id int,
    order_id text,
    product_id text,
    product_sku text,
    product_name text,
    category text,
    brand text,
    quantity int,
    unit_price decimal,
    total_price decimal,
    currency text,
    discount_amount decimal,
    payment_method text,
    transaction_status text,
    warehouse_location text,
    PRIMARY KEY (transaction_date, transaction_time, transaction_id)
) WITH CLUSTERING ORDER BY (transaction_time DESC, transaction_id ASC)
AND comment = 'Historial completo de transacciones'
AND compaction = {'class': 'TimeWindowCompactionStrategy'};

-- Tabla para análisis por usuario
CREATE TABLE IF NOT EXISTS transaction_history_by_user (
    user_id int,
    transaction_time timestamp,
    transaction_id uuid,
    transaction_date date,
    order_id text,
    product_id text,
    product_sku text,
    quantity int,
    total_price decimal,
    currency text,
    transaction_status text,
    PRIMARY KEY (user_id, transaction_time, transaction_id)
) WITH CLUSTERING ORDER BY (transaction_time DESC, transaction_id ASC)
AND comment = 'Transacciones por usuario';

-- Tabla para análisis por producto
CREATE TABLE IF NOT EXISTS transaction_history_by_product (
    product_sku text,
    transaction_date date,
    transaction_time timestamp,
    transaction_id uuid,
    user_id int,
    order_id text,
    quantity int,
    unit_price decimal,
    total_price decimal,
    transaction_status text,
    PRIMARY KEY (product_sku, transaction_date, transaction_time, transaction_id)
) WITH CLUSTERING ORDER BY (transaction_date DESC, transaction_time DESC, transaction_id ASC)
AND comment = 'Transacciones por producto';

-- =========================================
-- 3. TABLA DE MÉTRICAS AGREGADAS
-- =========================================

CREATE TABLE IF NOT EXISTS daily_metrics (
    metric_date date,
    metric_type text,
    dimension text,
    dimension_value text,
    metric_value counter,
    PRIMARY KEY (metric_date, metric_type, dimension, dimension_value)
) WITH comment = 'Métricas diarias agregadas';

CREATE TABLE IF NOT EXISTS hourly_metrics (
    metric_date date,
    metric_hour int,
    metric_type text,
    dimension text,
    dimension_value text,
    metric_value counter,
    PRIMARY KEY (metric_date, metric_hour, metric_type, dimension, dimension_value)
) WITH comment = 'Métricas por hora';

-- =========================================
-- 4. TABLA DE SESIONES DE USUARIO
-- =========================================

CREATE TABLE IF NOT EXISTS user_sessions (
    session_date date,
    session_start_time timestamp,
    session_id text,
    user_id int,
    session_end_time timestamp,
    duration_seconds int,
    page_views int,
    events_count int,
    device_type text,
    browser text,
    os text,
    country text,
    city text,
    entry_page text,
    exit_page text,
    conversion boolean,
    revenue decimal,
    PRIMARY KEY (session_date, session_start_time, session_id)
) WITH CLUSTERING ORDER BY (session_start_time DESC, session_id ASC)
AND comment = 'Sesiones de usuario por fecha';

-- =========================================
-- 5. INSERCIÓN DE DATOS DE EJEMPLO
-- =========================================

-- Insertar eventos de usuario
INSERT INTO user_events (event_date, event_time, event_id, user_id, session_id, event_type, page_url, referrer, user_agent, ip_address, device_type, browser, os, country, city, event_data)
VALUES (
    '2024-07-21',
    '2024-07-21 14:30:00',
    uuid(),
    1001,
    'sess_20240721_1001',
    'page_view',
    '/products/smartphone-xyz',
    '/search?q=smartphone',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '192.168.1.100',
    'desktop',
    'Chrome',
    'Windows',
    'USA',
    'Springfield',
    {
        'product_id': 'PHONE-XYZ-001',
        'category': 'Electronics',
        'time_on_page': '120'
    }
);

INSERT INTO user_events (event_date, event_time, event_id, user_id, session_id, event_type, page_url, referrer, user_agent, ip_address, device_type, browser, os, country, city, event_data)
VALUES (
    '2024-07-21',
    '2024-07-21 14:32:00',
    uuid(),
    1001,
    'sess_20240721_1001',
    'add_to_cart',
    '/products/smartphone-xyz',
    '/products/smartphone-xyz',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '192.168.1.100',
    'desktop',
    'Chrome',
    'Windows',
    'USA',
    'Springfield',
    {
        'product_id': 'PHONE-XYZ-001',
        'quantity': '1',
        'price': '599.99'
    }
);

-- Insertar en tabla por usuario
INSERT INTO user_events_by_user (user_id, event_time, event_id, event_date, session_id, event_type, page_url, event_data)
VALUES (
    1001,
    '2024-07-21 14:30:00',
    uuid(),
    '2024-07-21',
    'sess_20240721_1001',
    'page_view',
    '/products/smartphone-xyz',
    {
        'product_id': 'PHONE-XYZ-001',
        'time_on_page': '120'
    }
);

-- Insertar en tabla por tipo de evento
INSERT INTO events_by_type (event_type, event_date, event_time, event_id, user_id, session_id, event_data)
VALUES (
    'add_to_cart',
    '2024-07-21',
    '2024-07-21 14:32:00',
    uuid(),
    1001,
    'sess_20240721_1001',
    {
        'product_id': 'PHONE-XYZ-001',
        'quantity': '1',
        'price': '599.99'
    }
);

-- Insertar transacciones históricas
INSERT INTO transaction_history (transaction_date, transaction_time, transaction_id, user_id, order_id, product_id, product_sku, product_name, category, brand, quantity, unit_price, total_price, currency, discount_amount, payment_method, transaction_status, warehouse_location)
VALUES (
    '2024-07-21',
    '2024-07-21 15:45:00',
    uuid(),
    1001,
    'ORD-20240721-000001',
    'PHONE-XYZ-001',
    'PHONE-XYZ-001',
    'Smartphone XYZ Pro',
    'Electronics',
    'TechBrand',
    1,
    599.99,
    599.99,
    'USD',
    0.00,
    'credit_card',
    'completed',
    'WH-001'
);

INSERT INTO transaction_history_by_user (user_id, transaction_time, transaction_id, transaction_date, order_id, product_id, product_sku, quantity, total_price, currency, transaction_status)
VALUES (
    1001,
    '2024-07-21 15:45:00',
    uuid(),
    '2024-07-21',
    'ORD-20240721-000001',
    'PHONE-XYZ-001',
    'PHONE-XYZ-001',
    1,
    599.99,
    'USD',
    'completed'
);

INSERT INTO transaction_history_by_product (product_sku, transaction_date, transaction_time, transaction_id, user_id, order_id, quantity, unit_price, total_price, transaction_status)
VALUES (
    'PHONE-XYZ-001',
    '2024-07-21',
    '2024-07-21 15:45:00',
    uuid(),
    1001,
    'ORD-20240721-000001',
    1,
    599.99,
    599.99,
    'completed'
);

-- Insertar métricas agregadas
UPDATE daily_metrics SET metric_value = metric_value + 1 
WHERE metric_date = '2024-07-21' 
  AND metric_type = 'page_views' 
  AND dimension = 'product' 
  AND dimension_value = 'PHONE-XYZ-001';

UPDATE daily_metrics SET metric_value = metric_value + 1 
WHERE metric_date = '2024-07-21' 
  AND metric_type = 'transactions' 
  AND dimension = 'category' 
  AND dimension_value = 'Electronics';

-- Insertar sesión de usuario
INSERT INTO user_sessions (session_date, session_start_time, session_id, user_id, session_end_time, duration_seconds, page_views, events_count, device_type, browser, os, country, city, entry_page, exit_page, conversion, revenue)
VALUES (
    '2024-07-21',
    '2024-07-21 14:30:00',
    'sess_20240721_1001',
    1001,
    '2024-07-21 15:50:00',
    4800,
    8,
    15,
    'desktop',
    'Chrome',
    'Windows',
    'USA',
    'Springfield',
    '/search?q=smartphone',
    '/checkout/success',
    true,
    599.99
);

-- =========================================
-- 6. CONSULTAS DE EJEMPLO
-- =========================================

-- Eventos de un día específico
SELECT event_time, user_id, event_type, page_url, event_data
FROM user_events
WHERE event_date = '2024-07-21'
LIMIT 100;

-- Eventos de un usuario específico (últimos 30 días)
SELECT event_time, event_type, page_url, event_data
FROM user_events_by_user
WHERE user_id = 1001
  AND event_time >= '2024-06-21 00:00:00'
LIMIT 50;

-- Eventos de tipo específico en un rango de fechas
SELECT event_date, event_time, user_id, event_data
FROM events_by_type
WHERE event_type = 'add_to_cart'
  AND event_date IN ('2024-07-20', '2024-07-21')
LIMIT 100;

-- Transacciones de un día específico
SELECT transaction_time, user_id, order_id, product_name, quantity, total_price
FROM transaction_history
WHERE transaction_date = '2024-07-21'
  AND transaction_status = 'complete