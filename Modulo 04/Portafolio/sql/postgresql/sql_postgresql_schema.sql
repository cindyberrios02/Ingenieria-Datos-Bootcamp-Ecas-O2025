-- ====================================================================
-- PostgreSQL Schema for E-commerce Analytics & Data Warehouse
-- Optimized for OLAP workloads, complex queries, and reporting
-- ====================================================================

-- Create database and user
-- CREATE DATABASE ecommerce_analytics;
-- CREATE USER analytics_user WITH PASSWORD 'secure_password';
-- GRANT ALL PRIVILEGES ON DATABASE ecommerce_analytics TO analytics_user;

-- Connect to analytics database
\c ecommerce_analytics;

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- ====================================================================
-- ANALYTICS SCHEMA
-- ====================================================================

CREATE SCHEMA IF NOT EXISTS analytics;
SET search_path TO analytics, public;

-- ====================================================================
-- DIMENSION TABLES
-- ====================================================================

-- Customer Dimension
CREATE TABLE dim_customers (
    customer_id INTEGER PRIMARY KEY,
    customer_key UUID DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    full_name VARCHAR(200) GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED,
    date_of_birth DATE,
    age INTEGER GENERATED ALWAYS AS (EXTRACT(YEAR FROM age(current_date, date_of_birth))) STORED,
    gender CHAR(1) CHECK (gender IN ('M', 'F', 'O')),
    country VARCHAR(100),
    city VARCHAR(100),
    postal_code VARCHAR(20),
    customer_segment VARCHAR(50),
    registration_date DATE,
    registration_cohort VARCHAR(7) GENERATED ALWAYS AS (to_char(registration_date, 'YYYY-MM')) STORED,
    lifetime_value DECIMAL(10,2) DEFAULT 0,
    total_orders INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product Dimension
CREATE TABLE dim_products (
    product_id INTEGER PRIMARY KEY,
    product_key UUID DEFAULT uuid_generate_v4(),
    sku VARCHAR(100) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INTEGER,
    category_name VARCHAR(100),
    brand VARCHAR(100),
    current_price DECIMAL(10,2),
    cost DECIMAL(10,2),
    margin DECIMAL(10,2) GENERATED ALWAYS AS (current_price - cost) STORED,
    margin_percentage DECIMAL(5,2) GENERATED ALWAYS AS (
        CASE 
            WHEN current_price > 0 THEN ((current_price - cost) / current_price * 100)
            ELSE 0 
        END
    ) STORED,
    weight DECIMAL(8,2),
    color VARCHAR(50),
    size VARCHAR(20),
    rating_average DECIMAL(3,2),
    rating_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Time Dimension
CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date_value DATE UNIQUE NOT NULL,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name VARCHAR(10),
    week INTEGER,
    day INTEGER,
    day_name VARCHAR(10),
    day_of_week INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN DEFAULT FALSE,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    season VARCHAR(10)
);

-- Category Dimension
CREATE TABLE dim_categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    parent_category_id INTEGER,
    parent_category_name VARCHAR(100),
    category_path VARCHAR(500),
    category_level INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Location Dimension
CREATE TABLE dim_locations (
    location_id SERIAL PRIMARY KEY,
    country VARCHAR(100),
    country_code VARCHAR(3),
    state_province VARCHAR(100),
    city VARCHAR(100),
    postal_code VARCHAR(20),
    region VARCHAR(100),
    continent VARCHAR(50),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    population INTEGER,
    timezone VARCHAR(50)
);

-- ====================================================================
-- FACT TABLES
-- ====================================================================

-- Sales Fact Table
CREATE TABLE fact_sales (
    sales_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    date_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    