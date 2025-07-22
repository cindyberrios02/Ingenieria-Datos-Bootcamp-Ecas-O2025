# 🏗️ Arquitectura de Bases de Datos
## Diseño Integral del Ecosistema de Datos

### 🎯 Visión General

Este documento describe la arquitectura completa del ecosistema de bases de datos para nuestro e-commerce, detallando cómo cada tecnología se integra para crear una solución robusta, escalable y eficiente.


## 1. Principios Arquitectónicos

### 🏛️ Principios Fundamentales

#### **Principio de Responsabilidad Única**
Cada base de datos se especializa en un conjunto específico de tareas, optimizando rendimiento y mantenibilidad.

#### **Principio de Escalabilidad**
La arquitectura permite escalamiento independiente de cada componente según la demanda.

#### **Principio de Disponibilidad**
Diseño redundante que garantiza continuidad del servicio ante fallos.

#### **Principio de Consistencia Eventual**
Acepta trade-offs entre consistencia y disponibilidad donde sea apropiado.

---

## 2. Arquitectura de Capas

### 🏗️ Diagrama de Arquitectura Completa

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  Web App    │  Mobile App  │  Admin Panel  │  API Gateway      │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  Auth Service │ Order Service │ Product Service │ User Service  │
│  Payment API  │ Notification  │ Analytics API   │ Search API    │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA ACCESS LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│      ORM/ODM         │    Connection Pool    │    Cache Layer   │
│   (SQLAlchemy,       │   (PgBouncer,        │   (Redis,        │
│    Mongoose)         │    MySQL Pool)       │    Memcached)    │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                             │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│ PostgreSQL  │   MySQL     │  MongoDB    │  Cassandra  │DynamoDB │
│             │             │             │             │         │
│ 🔹Analytics │ 🔹OLTP      │ 🔹Catalog   │ 🔹Logs      │🔹Session│
│ 🔹Reporting │ 🔹Orders    │ 🔹Products  │ 🔹Events    │🔹Cart   │
│ 🔹BI        │ 🔹Users     │ 🔹Reviews   │ 🔹Metrics   │🔹Notif  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  Load Balancers │  Monitoring  │  Backup Systems │  Security    │
│  (HAProxy,      │  (Prometheus,│  (pg_dump,      │  (SSL, IAM,  │
│   Nginx)        │   Grafana)   │   mongodump)    │   VPC)       │
└─────────────────────────────────────────────────────────────────┘
```


## 3. Diseño Detallado por Tecnología

### 🐘 PostgreSQL - Analytics & Data Warehousing

#### **Configuración de Alta Disponibilidad**
```yaml
PostgreSQL Cluster:
  Primary Server:
    - Host: pg-primary.internal
    - Port: 5432
    - Resources: 16GB RAM, 8 CPU cores
    - Storage: 1TB SSD
  
  Read Replicas:
    - pg-replica-1.internal (Analytics queries)
    - pg-replica-2.internal (Reporting queries)
    - pg-replica-3.internal (Backup & ETL)
  
  Connection Pooling:
    - PgBouncer: Max 100 connections
    - Session pooling for analytics
    - Transaction pooling for quick queries
```

#### **Esquema de Datos**
```sql
-- Data Warehouse Schema
CREATE SCHEMA analytics;

-- Fact Tables
CREATE TABLE analytics.fact_sales (
    sale_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    order_date DATE NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension Tables
CREATE TABLE analytics.dim_customers (
    customer_id INT PRIMARY KEY,
    customer_segment VARCHAR(50),
    registration_date DATE,
    lifetime_value DECIMAL(10,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Casos de Uso Específicos**
- **Análisis de Cohortes**: Retención de clientes por período
- **Reporting Financiero**: Ingresos, márgenes, tendencias
- **Segmentación de Clientes**: RFM analysis, CLV
- **Análisis de Productos**: Performance por categoría

### 🐬 MySQL - Transaccional (OLTP)

#### **Configuración de Replicación**
```yaml
MySQL Cluster:
  Master Server:
    - Host: mysql-master.internal
    - Port: 3306
    - Engine: InnoDB
    - Resources: 8GB RAM, 4 CPU cores
  
  Slave Servers:
    - mysql-slave-1.internal (Read queries)
    - mysql-slave-2.internal (Backup)
  
  Configuration:
    - innodb_buffer_pool_size: 6GB
    - max_connections: 500
    - query_cache_size: 256MB
```

#### **Esquema Transaccional**
```sql
-- Core Business Tables
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled'),
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

#### **Casos de Uso Específicos**
- **Gestión de Pedidos**: Ciclo completo de órdenes
- **Autenticación**: Login, registro, permisos
- **Inventario**: Stock, movimientos, reservas
- **Pagos**: Transacciones, reembolsos

### 🍃 MongoDB - Catálogo y Contenido

#### **Configuración de Cluster**
```yaml
MongoDB Replica Set:
  Primary: mongodb-primary.internal:27017
  Secondaries:
    - mongodb-secondary-1.internal:27017
    - mongodb-secondary-2.internal:27017
  
  Sharding:
    - Shard Key: category_id
    - Chunks: Auto-balancing
    - Config Servers: 3 nodes
```

#### **Esquema de Documentos**
```javascript
// Product Document Schema
{
  "_id": ObjectId("..."),
  "sku": "IPHONE-15-PRO-128-BLUE",
  "name": "iPhone 15 Pro",
  "category": {
    "id": "smartphones",
    "name": "Smartphones",
    "path": "electronics/mobile/smartphones"
  },
  "specifications": {
    "storage": ["128GB", "256GB", "512GB", "1TB"],
    "colors": ["Natural Titanium", "Blue Titanium", "White Titanium"],
    "display": {
      "size": "6.1 inches",
      "resolution": "2556 x 1179",
      "technology": "Super Retina XDR"
    }
  },
  "pricing": {
    "base_price": 999.99,
    "variants": [
      { "storage": "128GB", "price": 999.99 },
      { "storage": "256GB", "price": 1099.99 }
    ]
  },
  "reviews": [
    {
      "user_id": "user123",
      "rating": 5,
      "comment": "Excellent camera quality!",
      "date": ISODate("2024-01-15")
    }
  ],
  "search_tags": ["iphone", "apple", "smartphone", "5g"],
  "created_at": ISODate("2024-01-01"),
  "updated_at": ISODate("2024-01-15")
}
```

#### **Casos de Uso Específicos**
- **Catálogo de Productos**: Información detallada y flexible
- **Búsqueda y Filtrado**: Full-text search, faceted search
- **Reseñas y Ratings**: Contenido generado por usuarios
- **Recomendaciones**: Productos relacionados y sugerencias

### 🏛️ Cassandra - Big Data y Logs

#### **Configuración de Cluster**
```yaml
Cassandra Cluster:
  Datacenter: dc1
  Nodes:
    - cassandra-1.internal:9042
    - cassandra-2.internal:9042
    - cassandra-3.internal:9042
  
  Replication:
    - Strategy: NetworkTopologyStrategy
    - Replication Factor: 3
    - Consistency Level: QUORUM
```

#### **Esquema de Datos**
```sql
-- Keyspace Creation
CREATE KEYSPACE ecommerce_logs 
WITH REPLICATION = {
  'class': 'NetworkTopologyStrategy',
  'dc1': 3
};

-- Event Logs Table
CREATE TABLE ecommerce_logs.user_events (
    user_id UUID,
    event_timestamp TIMESTAMP,
    event_type TEXT,
    event_data TEXT,
    session_id UUID,
    ip_address INET,
    user_agent TEXT,
    PRIMARY KEY (user_id, event_timestamp)
) WITH CLUSTERING ORDER BY (event_timestamp DESC);
```

#### **Casos de Uso Específicos**
- **Logs de Aplicación**: Eventos de usuario, errores, performance
- **Datos Históricos**: Transacciones de años anteriores
- **Métricas de Tiempo Real**: Contadores, estadísticas
- **Auditoría**: Trazabilidad de operaciones críticas

### ⚡ DynamoDB - Baja Latencia y Serverless

#### **Configuración de Tablas**
```yaml
DynamoDB Tables:
  UserSessions:
    PartitionKey: user_id (String)
    SortKey: session_timestamp (Number)
    TTL: 24 hours
    RCU: 100, WCU: 50
    GlobalSecondaryIndex: session_id
  
  ShoppingCart:
    PartitionKey: user_id (String)
    SortKey: product_id (String)
    TTL: 30 days
    RCU: 200, WCU: 100
  
  Notifications:
    PartitionKey: user_id (String)
    SortKey: notification_id (String)
    TTL: 90 days
    RCU: 50, WCU: 100
```

#### **Casos de Uso Específicos**
- **Sesiones de Usuario**: Estado de login, preferencias
- **Carrito de Compras**: Estado temporal antes de checkout
- **Notificaciones Push**: Mensajes personalizados
- **Caché de Aplicación**: Datos frecuentemente accedidos


## 4. Patrones de Integración

### 🔄 Sincronización de Datos

#### **Event-Driven Architecture**
```yaml
Event Flow:
  1. Order Created (MySQL) → Event Bus → Update Analytics (PostgreSQL)
  2. Product Updated (MongoDB) → Event Bus → Cache Invalidation
  3. User Action (DynamoDB) → Event Bus → Log Event (Cassandra)
```

#### **Change Data Capture (CDC)**
```python
# Ejemplo de CDC con Debezium
debezium_config = {
    "name": "mysql-connector",
    "config": {
        "connector.class": "io.debezium.connector.mysql.MySqlConnector",
        "database.hostname": "mysql-master.internal",
        "database.port": "3306",
        "database.user": "debezium",
        "database.password": "password",
        "database.server.id": "184054",
        "database.server.name": "ecommerce",
        "table.whitelist": "ecommerce.orders,ecommerce.customers"
    }
}
```

### 🔒 Consistencia y Transacciones

#### **Saga Pattern para Transacciones Distribuidas**
```python
class OrderSaga:
    def process_order(self, order_data):
        try:
            # Step 1: Reserve inventory (MySQL)
            inventory_reserved = self.reserve_inventory(order_data)
            
            # Step 2: Process payment (External API)
            payment_processed = self.process_payment(order_data)
            
            # Step 3: Update product availability (MongoDB)
            product_updated = self.update_product_availability(order_data)
            
            # Step 4: Log transaction (Cassandra)
            self.log_transaction(order_data)
            
            # Step 5: Update analytics (PostgreSQL)
            self.update_analytics(order_data)
            
        except Exception as e:
            # Compensation actions
            self.compensate_order(order_data, e)
```


## 5. Estrategias de Escalabilidad

### 📈 Escalabilidad Horizontal vs Vertical

#### **PostgreSQL - Vertical + Read Replicas**
```yaml
Scaling Strategy:
  Vertical Scaling:
    - Primary: 32GB RAM, 16 CPU cores
    - Max single machine capacity
  
  Horizontal Scaling:
    - Multiple read replicas
    - Partitioning by date/customer
    - Federated queries
```

#### **MongoDB - Horizontal Sharding**
```javascript
// Sharding Configuration
sh.enableSharding("ecommerce")
sh.shardCollection("ecommerce.products", {"category_id": 1})

// Shard Key Strategy
{
  "electronics": "shard-1",
  "clothing": "shard-2",
  "books": "shard-3"
}
```

#### **Cassandra - Distribución Automática**
```sql
-- Partition Strategy
CREATE TABLE user_events (
    user_id UUID,
    event_timestamp TIMESTAMP,
    event_data TEXT,
    PRIMARY KEY (user_id, event_timestamp)
) WITH CLUSTERING ORDER BY (event_timestamp DESC);

-- Data is automatically distributed across nodes
```

### 🔧 Optimización de Performance

#### **Índices Estratégicos**
```sql
-- PostgreSQL Analytics Indexes
CREATE INDEX idx_sales_date ON analytics.fact_sales(order_date);
CREATE INDEX idx_customer_segment ON analytics.dim_customers(customer_segment);

-- MySQL Transactional Indexes
CREATE INDEX idx_orders_customer ON orders(customer_id, created_at);
CREATE INDEX idx_products_category ON products(category_id, status);
```

#### **Caching Strategy**
```python
# Multi-layer Caching
class CacheStrategy:
    def __init__(self):
        self.l1_cache = Redis(host='redis-l1')    # Application cache
        self.l2_cache = Redis(host='redis-l2')    # Database cache
        self.cdn_cache = CloudFront()             # Static content
    
    def get_product(self, product_id):
        # L1 Cache check
        product = self.l1_cache.get(f"product:{product_id}")
        if product:
            return product
        
        # L2 Cache check
        product = self.l2_cache.get(f"product:{product_id}")
        if product:
            self.l1_cache.set(f"product:{product_id}", product, ttl=300)
            return product
        
        # Database query
        product = self.mongodb.find_one({"_id": product_id})
        self.l2_cache.set(f"product:{product_id}", product, ttl=3600)
        self.l1_cache.set(f"product:{product_id}", product, ttl=300)
        return product
```


## 6. Monitoreo y Observabilidad

### 📊 Métricas Clave

#### **Database Performance Metrics**
```yaml
PostgreSQL Metrics:
  - Query execution time
  - Buffer hit ratio
  - Connection pool utilization
  - Replication lag

MySQL Metrics:
  - Queries per second
  - Slow query log
  - InnoDB buffer pool usage
  - Master-slave lag

MongoDB Metrics:
  - Document read/write rates
  - Index usage statistics
  - Replica set health
  - Sharding balance

Cassandra Metrics:
  - Write/read latency
  - Compaction statistics
  - Node availability
  - Consistency level success rate

DynamoDB Metrics:
  - Consumed read/write capacity
  - Throttling events
  - Item size distribution
  - Hot partition detection
```

#### **Alerting Strategy**
```python
# Monitoring Configuration
alerts = {
    "high_latency": {
        "condition": "avg_query_time > 100ms",
        "severity": "warning",
        "notification": "slack + email"
    },
    "connection_pool_exhausted": {
        "condition": "active_connections > 90% of max",
        "severity": "critical",
        "notification": "pagerduty"
    },
    "replication_lag": {
        "condition": "lag > 5 minutes",
        "severity": "warning",
        "notification": "slack"
    }
}
```


## 7. Seguridad y Compliance

### 🔐 Estrategias de Seguridad

#### **Autenticación y Autorización**
```yaml
Security Layers:
  Network Security:
    - VPC with private subnets
    - Security groups and NACLs
    - SSL/TLS encryption in transit
  
  Database Security:
    - Database-level authentication
    - Role-based access control
    - Encryption at rest
    - Regular security patches
  
  Application Security:
    - API authentication (JWT)
    - Rate limiting
    - Input validation
    - SQL injection prevention
```

#### **Backup y Disaster Recovery**
```python
# Backup Strategy
backup_schedule = {
    "postgresql": {
        "full_backup": "weekly",
        "incremental": "daily",
        "wal_archiving": "continuous",
        "retention": "30 days"
    },
    "mysql": {
        "full_backup": "daily",
        "binary_logs": "continuous",
        "retention": "7 days"
    },
    "mongodb": {
        "replica_set_backup": "daily",
        "oplog_backup": "continuous",
        "retention": "14 days"
    }
}
```


## 8. Costos y ROI

### 💰 Análisis de Costos

#### **Costo Estimado Mensual**
```yaml
Infrastructure Costs:
  PostgreSQL Cluster:
    - Primary: $200/month
    - Replicas: $150/month x 3 = $450/month
    - Total: $650/month
  
  MySQL Cluster:
    - Master: $150/month
    - Slaves: $100/month x 2 = $200/month
    - Total: $350/month
  
  MongoDB Cluster:
    - Sharded cluster: $800/month
    - Config servers: $150/month
    - Total: $950/month
  
  Cassandra Cluster:
    - 3-node cluster: $600/month
  
  DynamoDB:
    - Variable based on usage
    - Estimated: $300/month
  
  Total Monthly Cost: $2,850/month
```

#### **ROI Calculation**
```python
# ROI Analysis
benefits = {
    "performance_improvement": {
        "query_speed": "40% faster",
        "user_experience": "improved",
        "conversion_rate": "+15%"
    },
    "scalability": {
        "user_capacity": "10x more users",
        "downtime_reduction": "99.9% uptime",
        "maintenance_cost": "-30%"
    },
    "development_efficiency": {
        "time_to_market": "-50%",
        "developer_productivity": "+25%",
        "bug_reduction": "-40%"
    }
}
```


## 9. Conclusiones y Próximos Pasos

### ✅ Arquitectura Validada

Esta arquitectura híbrida proporciona:

1. **Especialización**: Cada DB optimizada para su caso de uso
2. **Escalabilidad**: Horizontal y vertical según necesidades
3. **Disponibilidad**: Redundancia y failover automático
4. **Performance**: Latencia optimizada por tipo de operación
5. **Flexibilidad**: Adaptación a nuevos requerimientos

### 🎯 Implementación Progresiva

La implementación seguirá este orden:

1. **Fase 1**: PostgreSQL y MySQL (bases relacionales)
2. **Fase 2**: MongoDB (catálogo y contenido)
3. **Fase 3**: Cassandra (logs y big data)
4. **Fase 4**: DynamoDB (tiempo real)
5. **Fase 5**: Integración y optimización

### 📈 Métricas de Éxito

- **Performance**: <50ms para consultas críticas
- **Disponibilidad**: 99.9% SLA
- **Escalabilidad**: Soporte para 1M+ usuarios
- **Costos**: Optimización del 25% vs alternativas


*Esta arquitectura representa una implementación madura y escalable que balancea performance, costo y complejidad operacional.*