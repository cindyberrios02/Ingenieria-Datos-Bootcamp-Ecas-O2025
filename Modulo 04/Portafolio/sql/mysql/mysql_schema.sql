-- ====================================================================
-- MySQL Schema for E-commerce Transactional Database (OLTP)
-- Optimized for high-concurrency transactions, ACID compliance
-- ====================================================================

-- Create database and user
CREATE DATABASE IF NOT EXISTS ecommerce_oltp;
CREATE USER IF NOT EXISTS 'ecommerce_user'@'%' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON ecommerce_oltp.* TO 'ecommerce_user'@'%';
FLUSH PRIVILEGES;

-- Use the database
USE ecommerce_oltp;

-- Set optimal settings for OLTP workload
SET GLOBAL innodb_buffer_pool_size = 2147483648;  -- 2GB
SET GLOBAL max_connections = 500;
SET GLOBAL innodb_flush_log_at_trx_commit = 1;    -- Full ACID compliance
SET GLOBAL query_cache_size = 268435456;          -- 256MB
SET GLOBAL innodb_log_file_size = 1073741824;     -- 1GB

-- ====================================================================
-- CORE BUSINESS TABLES
-- ====================================================================

-- Customers table
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    gender ENUM('M', 'F', 'O') DEFAULT 'O',
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    phone_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for performance
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Customer addresses
CREATE TABLE customer_addresses (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    address_type ENUM('billing', 'shipping', 'both') DEFAULT 'both',
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    company VARCHAR(200),
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state_province VARCHAR(100),
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL DEFAULT 'USA',
    phone VARCHAR(20),
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    INDEX idx_customer_id (customer_id),
    INDEX idx_address_type (address_type),
    INDEX idx_country (country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Categories table
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    parent_category_id INT,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    image_url VARCHAR(500),
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (parent_category_id) REFERENCES categories(category_id) ON DELETE SET NULL,
    INDEX idx_parent_category (parent_category_id),
    INDEX idx_slug (slug),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Products table
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    sku VARCHAR(100) NOT NULL UNIQUE,
    product_name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    short_description TEXT,
    long_description TEXT,
    category_id INT NOT NULL,
    brand VARCHAR(100),
    model VARCHAR(100),
    weight DECIMAL(8,2),
    dimensions VARCHAR(100),
    color VARCHAR(50),
    size VARCHAR(20),
    material VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    is_digital BOOLEAN DEFAULT FALSE,
    requires_shipping BOOLEAN DEFAULT TRUE,
    meta_title VARCHAR(255),
    meta_description TEXT,
    meta_keywords VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT,
    INDEX idx_sku (sku),
    INDEX idx_category (category_id),
    INDEX idx_brand (brand),
    INDEX idx_active (is_active),
    INDEX idx_featured (is_featured),
    INDEX idx_slug (slug),
    FULLTEXT idx_search (product_name, short_description, brand)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Product variants (for products with multiple options)
CREATE TABLE product_variants (
    variant_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    variant_sku VARCHAR(100) NOT NULL UNIQUE,
    variant_name VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    compare_price DECIMAL(10,2),
    cost_price DECIMAL(10,2),
    stock_quantity INT DEFAULT 0,
    low_stock_threshold INT DEFAULT 10,
    weight DECIMAL(8,2),
    barcode VARCHAR(100),
    image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_variant_sku (variant_sku),
    INDEX idx_price (price),
    INDEX idx_stock (stock_quantity),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Product attributes (for flexible product specifications)
CREATE TABLE product_attributes (
    attribute_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    attribute_name VARCHAR(100) NOT NULL,
    attribute_value TEXT NOT NULL,
    display_order INT DEFAULT 0,
    is_searchable BOOLEAN DEFAULT FALSE,
    is_comparable BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_attribute_name (attribute_name),
    INDEX idx_searchable (is_searchable)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inventory tracking
CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    variant_id INT,
    stock_quantity INT NOT NULL DEFAULT 0,
    reserved_quantity INT NOT NULL DEFAULT 0,
    available_quantity INT GENERATED ALWAYS AS (stock_quantity - reserved_quantity) VIRTUAL,
    low_stock_threshold INT DEFAULT 10,
    supplier_id INT,
    warehouse_location VARCHAR(100),
    last_stock_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_variant_id (variant_id),
    INDEX idx_stock_quantity (stock_quantity),
    INDEX idx_available_quantity (available_quantity),
    UNIQUE KEY unique_inventory (product_id, variant_id, warehouse_location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================================
-- ORDER MANAGEMENT TABLES
-- ====================================================================

-- Orders table
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    order_number VARCHAR(50) NOT NULL UNIQUE,
    customer_id INT NOT NULL,
    order_status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'failed', 'refunded', 'partially_refunded') DEFAULT 'pending',
    fulfillment_status ENUM('unfulfilled', 'partial', 'fulfilled') DEFAULT 'unfulfilled',
    
    -- Order totals
    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0,
    discount_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    tax_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    shipping_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    
    -- Customer info snapshot
    customer_email VARCHAR(255),
    customer_phone VARCHAR(20),
    
    -- Addresses
    billing_address JSON,
    shipping_address JSON,
    
    -- Timestamps
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipped_date TIMESTAMP NULL,
    delivered_date TIMESTAMP NULL,
    cancelled_date TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Notes
    customer_notes TEXT,
    admin_notes TEXT,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    INDEX idx_customer_id (customer_id),
    INDEX idx_order_number (order_number),
    INDEX idx_order_status (order_status),
    INDEX idx_payment_status (payment_status),
    INDEX idx_order_date (order_date),
    INDEX idx_total_amount (total_amount),
    INDEX idx_customer_status (customer_id, order_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Order items table
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    variant_id INT,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    
    -- Product info snapshot (for historical reference)
    product_name VARCHAR(255),
    product_sku VARCHAR(100),
    variant_name VARCHAR(255),
    variant_sku VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id) ON DELETE RESTRICT,
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id),
    INDEX idx_variant_id (variant_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Shopping cart
CREATE TABLE shopping_cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    session_id VARCHAR(255),
    product_id INT NOT NULL,
    variant_id INT,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    
    -- Product info snapshot
    product_name VARCHAR(255),
    product_sku VARCHAR(100),
    variant_name VARCHAR(255),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    expires_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL 30 DAY),
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id) ON DELETE CASCADE,
    INDEX idx_customer_id (customer_id),
    INDEX idx_session_id (session_id),
    INDEX idx_product_id (product_id),
    INDEX idx_expires_at (expires_at),
    UNIQUE KEY unique_cart_item (customer_id, product_id, variant_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================================
-- PAYMENT TABLES
-- ====================================================================

-- Payment methods
CREATE TABLE payment_methods (
    payment_method_id INT AUTO_INCREMENT PRIMARY KEY,
    method_name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    processing_fee_percentage DECIMAL(5,4) DEFAULT 0,
    processing_fee_fixed DECIMAL(10,2) DEFAULT 0,
    min_amount DECIMAL(10,2) DEFAULT 0,
    max_amount DECIMAL(10,2),
    supported_currencies JSON,
    configuration JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_method_name (method_name),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Payment transactions
CREATE TABLE payment_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    order_id INT NOT NULL,
    payment_method_id INT NOT NULL,
    transaction_type ENUM('payment', 'refund', 'partial_refund', 'chargeback') DEFAULT 'payment',
    transaction_status ENUM('pending', 'processing', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    
    -- Amounts
    amount DECIMAL(10,2) NOT NULL,
    processing_fee DECIMAL(10,2) DEFAULT 0,
    net_amount DECIMAL(10,2) GENERATED ALWAYS AS (amount - processing_fee) STORED,
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- External reference
    gateway_transaction_id VARCHAR(255),
    gateway_response JSON,
    
    -- Timestamps
    initiated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    failed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Notes
    failure_reason TEXT,
    admin_notes TEXT,
    
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE RESTRICT,
    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(payment_method_id) ON DELETE RESTRICT,
    INDEX idx_order_id (order_id),
    INDEX idx_transaction_status (transaction_status),
    INDEX idx_transaction_type (transaction_type),
    INDEX idx_gateway_transaction_id (gateway_transaction_id),
    INDEX idx_initiated_at (initiated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================================
-- SHIPPING TABLES
-- ====================================================================

-- Shipping methods
CREATE TABLE shipping_methods (
    shipping_method_id INT AUTO_INCREMENT PRIMARY KEY,
    method_name VARCHAR(100) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    base_cost DECIMAL(10,2) NOT NULL DEFAULT 0,
    cost_per_kg DECIMAL(10,2) DEFAULT 0,
    cost_per_item DECIMAL(10,2) DEFAULT 0,
    free_shipping_threshold DECIMAL(10,2),
    estimated_delivery_days INT,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_method_name (method_name),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Shipments
CREATE TABLE shipments (
    shipment_id INT AUTO_INCREMENT PRIMARY KEY,
    shipment_uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    order_id INT NOT NULL,
    shipping_method_id INT NOT NULL,
    tracking_number VARCHAR(255),
    carrier VARCHAR(100),
    shipment_status ENUM('pending', 'processing', 'shipped', 'in_transit', 'delivered', 'returned') DEFAULT 'pending',
    
    -- Addresses
    shipping_address JSON,
    return_address JSON,
    
    -- Costs
    shipping_cost DECIMAL(10,2) NOT NULL DEFAULT 0,
    insurance_cost DECIMAL(10,2) DEFAULT 0,
    total_cost DECIMAL(10,2) GENERATED ALWAYS AS (shipping_cost + insurance_cost) STORED,
    
    -- Timestamps
    shipped_at TIMESTAMP NULL,
    estimated_delivery_at TIMESTAMP NULL,
    delivered_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Notes
    shipping_notes TEXT,
    delivery_notes TEXT,
    
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE RESTRICT,
    FOREIGN KEY (shipping_method_id) REFERENCES shipping_methods(shipping_method_id) ON DELETE RESTRICT,
    INDEX idx_order_id (order_id),
    INDEX idx_tracking_number (tracking_number),
    INDEX idx_shipment_status (shipment_status),
    INDEX idx_shipped_at (shipped_at),
    INDEX idx_delivered_at (delivered_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================================
-- CUSTOMER ENGAGEMENT TABLES
-- ====================================================================

-- Wishlists
CREATE TABLE wishlists (
    wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    wishlist_name VARCHAR(100) DEFAULT 'My Wishlist',
    is_public BOOLEAN DEFAULT FALSE,
    is_default BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    INDEX idx_customer_id (customer_id),
    INDEX idx_public (is_public)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Wishlist items
CREATE TABLE wishlist_items (
    wishlist_item_id INT AUTO_INCREMENT PRIMARY KEY,
    wishlist_id INT NOT NULL,
    product_id INT NOT NULL,
    variant_id INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (wishlist_id) REFERENCES wishlists(wishlist_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id) ON DELETE CASCADE,
    INDEX idx_wishlist_id (wishlist_id),
    INDEX idx_product_id (product_id),
    UNIQUE KEY unique_wishlist_item (wishlist_id, product_id, variant_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Customer reviews
CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    order_id INT,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    review_text TEXT,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN DEFAULT FALSE,
    helpful_votes INT DEFAULT 0,
    total_votes INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE SET NULL,
    INDEX idx_customer_id (customer_id),
    INDEX idx_product_id (product_id),
    INDEX idx_rating (rating),
    INDEX idx_approved (is_approved),
    INDEX idx_verified (is_verified_purchase),
    UNIQUE KEY unique_customer_product_review (customer_id, product_id, order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================================
-- TRIGGERS FOR BUSINESS LOGIC
-- ====================================================================

-- Trigger to update order totals when order items change
DELIMITER //
CREATE TRIGGER trg_update_order_totals
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE orders 
    SET 
        subtotal = (
            SELECT COALESCE(SUM(total_price), 0) 
            FROM order_items 
            WHERE order_id = NEW.order_id
        ),
        total_amount = (
            SELECT COALESCE(SUM(total_price), 0) 
            FROM order_items 
            WHERE order_id = NEW.order_id
        ) + (
            SELECT COALESCE(tax_amount, 0) + COALESCE(shipping_amount, 0) - COALESCE(discount_amount, 0)
            FROM orders 
            WHERE order_id = NEW.order_id
        )
    WHERE order_id = NEW.order_id;
END//

-- Trigger to update inventory when order is placed
CREATE TRIGGER trg_update_inventory_on_order
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    IF NEW.variant_id IS NOT NULL THEN
        UPDATE inventory 
        SET reserved_quantity = reserved_quantity + NEW.quantity
        WHERE variant_id = NEW.variant_id;
    ELSE
        UPDATE inventory 
        SET reserved_quantity = reserved_quantity + NEW.quantity
        WHERE product_id = NEW.product_id AND variant_id IS NULL;
    END IF;
END//

-- Trigger to update inventory when order is cancelled
CREATE TRIGGER trg_update_inventory_on_cancel
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF OLD.order_status != 'cancelled' AND NEW.order_status = 'cancelled' THEN
        UPDATE inventory i
        INNER JOIN order_items oi ON (
            (i.variant_id = oi.variant_id AND oi.variant_id IS NOT NULL) OR
            (i.product_id = oi.product_id AND oi.variant_id IS NULL AND i.variant_id IS NULL)
        )
        SET i.reserved_quantity = i.reserved_quantity - oi.quantity
        WHERE oi.order_id = NEW.order_id;
    END IF;
END//

-- Trigger to generate unique order numbers
CREATE TRIGGER trg_generate_order_number
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    IF NEW.order_number IS NULL OR NEW.order_number = '' THEN
        SET NEW.order_number = CONCAT('ORD-', YEAR(NOW()), MONTH(NOW()), '-', LPAD(NEW.order_id, 6, '0'));
    END IF;
END//

-- Trigger to update product average rating
CREATE TRIGGER trg_update_product_rating
AFTER INSERT ON reviews
FOR EACH ROW
BEGIN
    UPDATE products p
    SET 
        p.meta_keywords = CONCAT(
            COALESCE(p.meta_keywords, ''),
            ', rating:', NEW.rating
        )
    WHERE p.product_id = NEW.product_id;
END//

DELIMITER ;

-- ====================================================================
-- STORED PROCEDURES
-- ====================================================================

-- Procedure to process order checkout
DELIMITER //
CREATE PROCEDURE ProcessOrderCheckout(
    IN p_customer_id INT,
    IN p_shipping_method_id INT,
    IN p_payment_method_id INT,
    IN p_billing_address JSON,
    IN p_shipping_address JSON,
    OUT p_order_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(500)
)
BEGIN
    DECLARE v_cart_count INT DEFAULT 0;
    DECLARE v_cart_total DECIMAL(10,2) DEFAULT 0;
    DECLARE v_shipping_cost DECIMAL(10,2) DEFAULT 0;
    DECLARE v_tax_amount DECIMAL(10,2) DEFAULT 0;
    DECLARE v_order_total DECIMAL(10,2) DEFAULT 0;
    DECLARE exit handler for sqlexception
    BEGIN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = 'An error occurred during checkout';
        GET DIAGNOSTICS CONDITION 1 p_message = MESSAGE_TEXT;
    END;
    
    START TRANSACTION;
    
    -- Check if customer has items in cart
    SELECT COUNT(*), COALESCE(SUM(total_price), 0)
    INTO v_cart_count, v_cart_total
    FROM shopping_cart
    WHERE customer_id = p_customer_id;
    
    IF v_cart_count = 0 THEN
        SET p_success = FALSE;
        SET p_message = 'Shopping cart is empty';
        ROLLBACK;
    ELSE
        -- Calculate shipping cost
        SELECT base_cost INTO v_shipping_cost
        FROM shipping_methods
        WHERE shipping_method_id = p_shipping_method_id;
        
        -- Calculate tax (simplified - 8% tax rate)
        SET v_tax_amount = v_cart_total * 0.08;
        SET v_order_total = v_cart_total + v_shipping_cost + v_tax_amount;
        
        -- Create order
        INSERT INTO orders (
            customer_id, 
            subtotal, 
            tax_amount, 
            shipping_amount, 
            total_amount,
            billing_address,
            shipping_address,
            customer_email
        ) VALUES (
            p_customer_id,
            v_cart_total,
            v_tax_amount,
            v_shipping_cost,
            v_order_total,
            p_billing_address,
            p_shipping_address,
            (SELECT email FROM customers WHERE customer_id = p_customer_id)
        );
        
        SET p_order_id = LAST_INSERT_ID();
        
        -- Move cart items to order items
        INSERT INTO order_items (
            order_id, product_id, variant_id, quantity, unit_price, total_price,
            product_name, product_sku, variant_name, variant_sku
        )
        SELECT 
            p_order_id,
            sc.product_id,
            sc.variant_id,
            sc.quantity,
            sc.unit_price,
            sc.total_price,
            sc.product_name,
            sc.product_sku,
            sc.variant_name,
            COALESCE(pv.variant_sku, '')
        FROM shopping_cart sc
        LEFT JOIN product_variants pv ON sc.variant_id = pv.variant_id
        WHERE sc.customer_id = p_customer_id;
        
        -- Clear shopping cart
        DELETE FROM shopping_cart WHERE customer_id = p_customer_id;
        
        -- Create shipment record
        INSERT INTO shipments (order_id, shipping_method_id, shipping_cost, shipping_address)
        VALUES (p_order_id, p_shipping_method_id, v_shipping_cost, p_shipping_address);
        
        SET p_success = TRUE;
        SET p_message = 'Order created successfully';
        
        COMMIT;
    END IF;
END//

-- Procedure to add item to cart
CREATE PROCEDURE AddToCart(
    IN p_customer_id INT,
    IN p_product_id INT,
    IN p_variant_id INT,
    IN p_quantity INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(500)
)
BEGIN
    DECLARE v_stock_available INT DEFAULT 0;
    DECLARE v_unit_price DECIMAL(10,2) DEFAULT 0;
    DECLARE v_existing_quantity INT DEFAULT 0;
    
    -- Check stock availability
    IF p_variant_id IS NOT NULL THEN
        SELECT available_quantity, price
        INTO v_stock_available, v_unit_price
        FROM inventory i
        INNER JOIN product_variants pv ON i.variant_id = pv.variant_id
        WHERE i.variant_id = p_variant_id;
    ELSE
        SELECT available_quantity, price
        INTO v_stock_available, v_unit_price
        FROM inventory i
        INNER JOIN product_variants pv ON i.product_id = pv.product_id
        WHERE i.product_id = p_product_id AND i.variant_id IS NULL
        LIMIT 1;
    END IF;
    
    -- Check existing quantity in cart
    SELECT COALESCE(quantity, 0)
    INTO v_existing_quantity
    FROM shopping_cart
    WHERE customer_id = p_customer_id 
      AND product_id = p_product_id 
      AND (variant_id = p_variant_id OR (variant_id IS NULL AND p_variant_id IS NULL));
    
    IF v_stock_available >= (p_quantity + v_existing_quantity) THEN
        -- Add or update cart item
        INSERT INTO shopping_cart (
            customer_id, product_id, variant_id, quantity, unit_price,
            product_name, product_sku, variant_name
        ) VALUES (
            p_customer_id,
            p_product_id,
            p_variant_id,
            p_quantity,
            v_unit_price,
            (SELECT product_name FROM products WHERE product_id = p_product_id),
            (SELECT sku FROM products WHERE product_id = p_product_id),
            (SELECT variant_name FROM product_variants WHERE variant_id = p_variant_id)
        )
        ON DUPLICATE KEY UPDATE
            quantity = quantity + p_quantity,
            unit_price = v_unit_price,
            updated_at = CURRENT_TIMESTAMP;
        
        SET p_success = TRUE;
        SET p_message = 'Item added to cart successfully';
    ELSE
        SET p_success = FALSE;
        SET p_message = 'Insufficient stock available';
    END IF;
END//

DELIMITER ;

-- ====================================================================
-- VIEWS FOR COMMON QUERIES
-- ====================================================================

-- Customer order summary view
CREATE VIEW v_customer_order_summary AS
SELECT 
    c.customer_id,
    c.email,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) as total_orders,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    COALESCE(AVG(o.total_amount), 0) as avg_order_value,
    MAX(o.order_date) as last_order_date,
    MIN(o.order_date) as first_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.is_active = TRUE
GROUP BY c.customer_id, c.email, c.first_name, c.last_name;

-- Product performance view
CREATE VIEW v_product_performance AS
SELECT 
    p.product_id,
    p.product_name,
    p.sku,
    c.category_name,
    p.brand,
    COUNT(oi.order_item_id) as times_ordered,
    SUM(oi.quantity) as total_quantity_sold,
    SUM(oi.total_price) as total_revenue,
    AVG(oi.unit_price) as avg_selling_price,
    AVG(r.rating) as avg_rating,
    COUNT(r.review_id) as review_count
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN reviews r ON p.product_id = r.product_id
WHERE p.is_active = TRUE
GROUP BY p.product_id, p.product_name, p.sku, c.category_name, p.brand;

-- Low stock alert view
CREATE VIEW v_low_stock_alerts AS
SELECT 
    p.product_id,
    p.product_name,
    p.sku,
    pv.variant_id,
    pv.variant_name,
    pv.variant_sku,
    i.stock_quantity,
    i.reserved_quantity,
    i.available_quantity,
    i.low_stock_threshold,
    CASE 
        WHEN i.available_quantity <= 0 THEN 'OUT_OF_STOCK'
        WHEN i.available_quantity <= i.low_stock_threshold THEN 'LOW_STOCK'
        ELSE 'IN_STOCK'
    END as stock_status
FROM products p
LEFT JOIN product_variants pv ON p.product_id = pv.product_id
LEFT JOIN inventory i ON (i.product_id = p.product_id AND i.variant_id = pv.variant_id)
WHERE p.is_active = TRUE
  AND (i.available_quantity <= i.low_stock_threshold OR i.available_quantity <= 0);

-- ====================================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ====================================================================

-- Additional composite indexes for common query patterns
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date DESC);
CREATE INDEX idx_orders_status_date ON orders(order_status, order_date DESC);
CREATE INDEX idx_order_items_product_date ON order_items(product_id, created_at DESC);
CREATE INDEX idx_reviews_product_rating ON reviews(product_id, rating DESC);
CREATE INDEX idx_products_category_active ON products(category_id, is_active);
CREATE INDEX idx_products_featured_active ON products(is_featured, is_active);

-- ====================================================================
-- SAMPLE DATA INSERTS
-- ====================================================================

-- Insert payment methods
INSERT INTO payment_methods (method_name, display_name, description, is_active, processing_fee_percentage) VALUES
('credit_card', 'Credit Card', 'Visa, MasterCard, American Express', TRUE, 2.90),
('paypal', 'PayPal', 'Pay with your PayPal account', TRUE, 2.50),
('apple_pay', 'Apple Pay', 'Pay with Apple Pay', TRUE, 2.90),
('google_pay', 'Google Pay', 'Pay with Google Pay', TRUE, 2.90),
('bank_transfer', 'Bank Transfer', 'Direct bank transfer', TRUE, 0.50);

-- Insert shipping methods
INSERT INTO shipping_methods (method_name, display_name, description, base_cost, estimated_delivery_days, is_active) VALUES
('standard', 'Standard Shipping', 'Standard delivery 5-7 business days', 5.99, 6, TRUE),
('express', 'Express Shipping', 'Express delivery 2-3 business days', 12.99, 2, TRUE),
('overnight', 'Overnight Shipping', 'Next business day delivery', 24.99, 1, TRUE),
('free', 'Free Shipping', 'Free shipping on orders over $50', 0.00, 7, TRUE);

-- Insert sample categories
INSERT INTO categories (category_name, parent_category_id, slug, description, is_active) VALUES
('Electronics', NULL, 'electronics', 'Electronic devices and accessories', TRUE),
('Clothing', NULL, 'clothing', 'Apparel and fashion items', TRUE),
('Books', NULL, 'books', 'Books and literature', TRUE),
('Home & Garden', NULL, 'home-garden', 'Home improvement and gardening', TRUE),
('Sports & Outdoors', NULL, 'sports-outdoors', 'Sports equipment and outdoor gear', TRUE),
('Smartphones', 1, 'smartphones', 'Mobile phones and accessories', TRUE),
('Laptops', 1, 'laptops', 'Laptop computers and accessories', TRUE),
('Headphones', 1, 'headphones', 'Audio equipment and headphones', TRUE),
('Men\'s Clothing', 2, 'mens-clothing', 'Men\'s apparel and accessories', TRUE),
('Women\'s Clothing', 2, 'womens-clothing', 'Women\'s apparel and accessories', TRUE);

-- ====================================================================
-- COMPLETION MESSAGE
-- ====================================================================

SELECT 
    'MySQL E-commerce OLTP Database Schema Created Successfully!' as Message,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'ecommerce_oltp') as Total_Tables,
    (SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'ecommerce_oltp') as Total_Views,
    (SELECT COUNT(*) FROM information_schema.routines WHERE routine_schema = 'ecommerce_oltp') as Total_Procedures;