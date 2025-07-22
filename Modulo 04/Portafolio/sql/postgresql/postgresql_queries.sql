-- =========================================
-- CONSULTAS OPTIMIZADAS POSTGRESQL
-- E-commerce Analytics Queries
-- =========================================

-- =========================================
-- 1. CONSULTAS TRANSACCIONALES
-- =========================================

-- Obtener pedidos recientes de un usuario específico
SELECT 
    o.order_id,
    o.order_number,
    o.status,
    o.total_amount,
    o.created_at,
    COUNT(oi.order_item_id) as total_items
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.user_id = 1
    AND o.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY o.order_id, o.order_number, o.status, o.total_amount, o.created_at
ORDER BY o.created_at DESC;

-- Verificar disponibilidad de productos
SELECT 
    p.product_id,
    p.name,
    p.sku,
    i.quantity_available,
    CASE 
        WHEN i.quantity_available > 0 THEN 'Disponible'
        ELSE 'Agotado'
    END as stock_status
FROM products p
JOIN inventory i ON p.product_id = i.product_id
WHERE p.product_id IN (1, 2, 3, 4)
    AND p.is_active = TRUE;

-- Buscar productos por texto (usando índice GIN)
SELECT 
    p.product_id,
    p.name,
    p.description,
    p.price,
    c.name as category,
    ts_rank(to_tsvector('spanish', p.name || ' ' || COALESCE(p.description, '')), plainto_tsquery('spanish', 'smartphone')) as relevance
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE to_tsvector('spanish', p.name || ' ' || COALESCE(p.description, '')) @@ plainto_tsquery('spanish', 'smartphone')
    AND p.is_active = TRUE
ORDER BY relevance DESC, p.name;

-- =========================================
-- 2. CONSULTAS ANALÍTICAS
-- =========================================

-- Top 10 productos más vendidos (últimos 3 meses)
SELECT 
    p.name,
    p.sku,
    SUM(oi.quantity) as total_sold,
    SUM(oi.total_price) as total_revenue,
    AVG(oi.unit_price) as avg_price
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'delivered'
    AND o.created_at >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY p.product_id, p.name, p.sku
ORDER BY total_sold DESC
LIMIT 10;

-- Análisis de ventas mensuales
SELECT 
    DATE_TRUNC('month', o.created_at) as month,
    COUNT(DISTINCT o.order_id) as total_orders,
    COUNT(DISTINCT o.user_id) as unique_customers,
    SUM(o.total_amount) as total_revenue,
    AVG(o.total_amount) as avg_order_value
FROM orders o
WHERE o.status != 'cancelled'
    AND o.created_at >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', o.created_at)
ORDER BY month DESC;

-- Análisis de cohortes de clientes (retención mensual)
WITH first_orders AS (
    SELECT 
        user_id,
        DATE_TRUNC('month', MIN(created_at)) as first_order_month
    FROM orders 
    WHERE status != 'cancelled'
    GROUP BY user_id
),
monthly_orders AS (
    SELECT 
        o.user_id,
        fo.first_order_month,
        DATE_TRUNC('month', o.created_at) as order_month,
        EXTRACT(EPOCH FROM (DATE_TRUNC('month', o.created_at) - fo.first_order_month)) / (30.44 * 24 * 3600) as month_number
    FROM orders o
    JOIN first_orders fo ON o.user_id = fo.user_id
    WHERE o.status != 'cancelled'
)
SELECT 
    first_order_month,
    month_number::integer as months_after_first,
    COUNT(DISTINCT user_id) as customers
FROM monthly_orders
WHERE first_order_month >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY first_order_month, month_number::integer
ORDER BY first_order_month, months_after_first;

-- Productos con bajo stock
SELECT 
    p.name,
    p.sku,
    i.quantity_available,
    i.reorder_level,
    CASE 
        WHEN i.quantity_available = 0 THEN 'Sin Stock'
        WHEN i.quantity_available <= i.reorder_level THEN 'Stock Bajo'
        ELSE 'Stock Normal'
    END as stock_alert
FROM products p
JOIN inventory i ON p.product_id = i.product_id
WHERE p.is_active = TRUE
    AND i.quantity_available <= i.reorder_level
ORDER BY i.quantity_available ASC;

-- =========================================
-- 3. CONSULTAS CON VISTAS MATERIALIZADAS
-- =========================================

-- Consultar resumen de ventas por producto usando vista materializada
SELECT 
    product_name,
    sku,
    category_name,
    total_quantity_sold,
    total_revenue,
    ROUND(avg_unit_price::numeric, 2) as avg_unit_price,
    last_sale_date
FROM mv_product_sales_summary
WHERE total_quantity_sold > 0
ORDER BY total_revenue DESC
LIMIT 20;

-- Top clientes por valor gastado usando vista materializada
SELECT 
    full_name,
    email,
    total_orders,
    total_spent,
    ROUND(avg_order_value::numeric, 2) as avg_order_value,
    last_order_date
FROM mv_customer_summary
WHERE total_orders > 0
ORDER BY total_spent DESC
LIMIT 10;

-- =========================================
-- 4. CONSULTAS CON WINDOW FUNCTIONS
-- =========================================

-- Ranking de productos por ventas por categoría
SELECT 
    c.name as category,
    p.name as product,
    SUM(oi.quantity) as total_sold,
    RANK() OVER (PARTITION BY c.name ORDER BY SUM(oi.quantity) DESC) as rank_in_category
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'delivered'
    AND o.created_at >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY c.name, p.name
ORDER BY c.name, rank_in_category;

-- Crecimiento mensual de ventas con comparación al mes anterior
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', created_at) as month,
        SUM(total_amount) as revenue
    FROM orders
    WHERE status != 'cancelled'
    GROUP BY DATE_TRUNC('month', created_at)
)
SELECT 
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) as previous_month_revenue,
    ROUND(
        ((revenue - LAG(revenue) OVER (ORDER BY month)) / 
         LAG(revenue) OVER (ORDER BY month)) * 100, 2
    ) as growth_percentage
FROM monthly_sales
ORDER BY month DESC;

-- =========================================
-- 5. CONSULTAS COMPLEJAS CON JOINS
-- =========================================

-- Análisis completo de pedidos con detalles
SELECT 
    o.order_number,
    u.first_name || ' ' || u.last_name as customer_name,
    u.email,
    o.status,
    o.total_amount,
    o.created_at,
    COUNT(oi.order_item_id) as total_items,
    STRING_AGG(p.name, ', ') as products,
    a.city || ', ' || a.country as shipping_location
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN addresses a ON o.shipping_address_id = a.address_id
WHERE o.created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY 
    o.order_id, o.order_number, u.first_name, u.last_name, u.email,
    o.status, o.total_amount, o.created_at, a.city, a.country
ORDER BY o.created_at DESC;

-- Productos nunca vendidos
SELECT 
    p.product_id,
    p.name,
    p.sku,
    p.price,
    c.name as category,
    i.quantity_available
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN inventory i ON p.product_id = i.product_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL
    AND p.is_active = TRUE
ORDER BY p.created_at DESC;

-- =========================================
-- 6. MANTENIMIENTO Y OPTIMIZACIÓN
-- =========================================

-- Refrescar vistas materializadas
SELECT refresh_materialized_views();

-- Analizar estadísticas de tablas
ANALYZE users;
ANALYZE products;
ANALYZE orders;
ANALYZE order_items;

-- Verificar uso de índices
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM orders 
WHERE user_id = 1 
    AND created_at >= CURRENT_DATE - INTERVAL '30 days';

-- Estadísticas de tamaño de tablas
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
FROM pg_tables 
WHERE schemaname = 'transactional'
ORDER BY size_bytes DESC;