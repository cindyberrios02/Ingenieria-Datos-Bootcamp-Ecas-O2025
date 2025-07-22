// =========================================
// MONGODB SETUP Y OPERACIONES CRUD
// E-commerce Document Store
// =========================================

// Conectar a la base de datos
use('ecommerce_nosql');

// =========================================
// 1. CONFIGURACIÓN INICIAL
// =========================================

// Crear índices para optimización
db.products_catalog.createIndex({ "sku": 1 }, { unique: true });
db.products_catalog.createIndex({ "category": 1 });
db.products_catalog.createIndex({ "price": 1 });
db.products_catalog.createIndex({ "tags": 1 });
db.products_catalog.createIndex({ "name": "text", "description": "text" });

db.user_profiles.createIndex({ "user_id": 1 }, { unique: true });
db.user_profiles.createIndex({ "email": 1 }, { unique: true });
db.user_profiles.createIndex({ "preferences.categories": 1 });

db.user_sessions.createIndex({ "user_id": 1 });
db.user_sessions.createIndex({ "session_start": 1 });
db.user_sessions.createIndex({ "created_at": 1 }, { expireAfterSeconds: 2592000 }); // 30 días

db.reviews.createIndex({ "product_id": 1 });
db.reviews.createIndex({ "user_id": 1 });
db.reviews.createIndex({ "rating": 1 });
db.reviews.createIndex({ "created_at": 1 });

print("✅ Índices creados correctamente");

// =========================================
// 2. INSERCIÓN DE DATOS - CATÁLOGO DE PRODUCTOS
// =========================================

// Eliminar datos existentes para reiniciar
db.products_catalog.deleteMany({});

// Insertar catálogo de productos con información semiestructurada
db.products_catalog.insertMany([
    {
        sku: "PHONE-XYZ-001",
        name: "Smartphone XYZ Pro",
        description: "Teléfono inteligente de última generación con cámara de 108MP",
        category: "Electronics",
        subcategory: "Smartphones",
        price: 599.99,
        currency: "USD",
        brand: "TechBrand",
        tags: ["smartphone", "camera", "5G", "android"],
        specifications: {
            screen_size: "6.7 inches",
            battery: "4500mAh",
            storage: ["128GB", "256GB", "512GB"],
            colors: ["Black", "Silver", "Blue"],
            camera: {
                main: "108MP",
                front: "32MP",
                features: ["Night Mode", "Portrait", "Ultra Wide"]
            },
            connectivity: ["5G", "WiFi 6", "Bluetooth 5.2"],
            os: "Android 13"
        },
        dimensions: {
            width: 75.8,
            height: 164.2,
            depth: 8.9,
            weight: 195
        },
        images: [
            "https://example.com/images/phone-xyz-front.jpg",
            "https://example.com/images/phone-xyz-back.jpg",
            "https://example.com/images/phone-xyz-side.jpg"
        ],
        availability: {
            in_stock: true,
            quantity: 50,
            warehouse_location: "WH-001"
        },
        seo: {
            meta_title: "Smartphone XYZ Pro - Cámara 108MP | TechStore",
            meta_description: "Descubre el nuevo Smartphone XYZ Pro con cámara de 108MP, 5G y Android 13. Compra ahora con envío gratis.",
            keywords: ["smartphone", "108MP", "5G", "android", "techbrand"]
        },
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        sku: "LAPTOP-ABC-001",
        name: "Laptop Profesional ABC",
        description: "Laptop para uso profesional y gaming con procesador Intel i7",
        category: "Electronics",
        subcategory: "Laptops",
        price: 1299.99,
        currency: "USD",
        brand: "ProBrand",
        tags: ["laptop", "gaming", "professional", "intel", "SSD"],
        specifications: {
            processor: "Intel Core i7-12700H",
            memory: "16GB DDR4",
            storage: "512GB NVMe SSD",
            graphics: "NVIDIA RTX 3060",
            screen: {
                size: "15.6 inches",
                resolution: "1920x1080",
                refresh_rate: "144Hz",
                panel_type: "IPS"
            },
            ports: ["USB-C", "USB 3.0", "HDMI", "Ethernet", "Audio Jack"],
            battery: "80Wh",
            os: "Windows 11 Pro"
        },
        dimensions: {
            width: 359,
            height: 255,
            depth: 23.9,
            weight: 2500
        },
        images: [
            "https://example.com/images/laptop-abc-open.jpg",
            "https://example.com/images/laptop-abc-closed.jpg",
            "https://example.com/images/laptop-abc-ports.jpg"
        ],
        availability: {
            in_stock: true,
            quantity: 25,
            warehouse_location: "WH-001"
        },
        warranty: {
            duration: "2 years",
            type: "Limited warranty",
            coverage: ["Hardware defects", "Manufacturing issues"]
        },
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        sku: "SHIRT-BASIC-001",
        name: "Camiseta Básica Cotton",
        description: "Camiseta básica 100% algodón, perfecta para uso diario",
        category: "Clothing",
        subcategory: "T-Shirts",
        price: 19.99,
        currency: "USD",
        brand: "BasicWear",
        tags: ["t-shirt", "cotton", "basic", "casual"],
        specifications: {
            material: "100% Cotton",
            sizes: ["XS", "S", "M", "L", "XL", "XXL"],
            colors: ["White", "Black", "Navy", "Gray", "Red"],
            fit: "Regular",
            care_instructions: ["Machine wash cold", "Tumble dry low", "Do not bleach"],
            origin: "Made in USA"
        },
        size_chart: {
            XS: { chest: 84, length: 66 },
            S: { chest: 89, length: 69 },
            M: { chest: 94, length: 72 },
            L: { chest: 99, length: 75 },
            XL: { chest: 104, length: 78 },
            XXL: { chest: 109, length: 81 }
        },
        images: [
            "https://example.com/images/shirt-basic-white.jpg",
            "https://example.com/images/shirt-basic-black.jpg",
            "https://example.com/images/shirt-basic-navy.jpg"
        ],
        availability: {
            in_stock: true,
            quantity: 100,
            warehouse_location: "WH-002"
        },
        created_at: new Date(),
        updated_at: new Date()
    }
]);

print("✅ Productos insertados en el catálogo");

// =========================================
// 3. INSERCIÓN DE PERFILES DE USUARIO
// =========================================

db.user_profiles.deleteMany({});

db.user_profiles.insertMany([
    {
        user_id: 1001,
        email: "juan.perez@email.com",
        profile: {
            first_name: "Juan",
            last_name: "Pérez",
            avatar: "https://example.com/avatars/juan.jpg",
            phone: "+1234567890",
            birth_date: new Date("1990-05-15"),
            gender: "Male"
        },
        preferences: {
            categories: ["Electronics", "Sports"],
            brands: ["TechBrand", "SportsBrand"],
            price_range: { min: 50, max: 1000 },
            notifications: {
                email: true,
                sms: false,
                push: true
            },
            language: "es",
            currency: "USD"
        },
        addresses: [
            {
                type: "shipping",
                is_default: true,
                street: "123 Main St",
                city: "Springfield",
                state: "IL",
                postal_code: "62701",
                country: "USA",
                coordinates: {
                    lat: 39.7817,
                    lng: -89.6501
                }
            },
            {
                type: "billing",
                is_default: false,
                street: "456 Oak Ave",
                city: "Springfield",
                state: "IL",
                postal_code: "62701",
                country: "USA"
            }
        ],
        social_profiles: {
            facebook: "juan.perez.fb",
            instagram: "@juan_perez_insta"
        },
        loyalty: {
            points: 1250,
            tier: "Gold",
            joined_date: new Date("2023-01-15")
        },
        purchase_history: {
            total_orders: 15,
            total_spent: 3250.75,
            avg_order_value: 216.72,
            favorite_categories: ["Electronics", "Clothing"],
            last_purchase: new Date("2024-12-15")
        },
        created_at: new Date("2023-01-15"),
        updated_at: new Date()
    },
    {
        user_id: 1002,
        email: "maria.garcia@email.com",
        profile: {
            first_name: "María",
            last_name: "García",
            avatar: "https://example.com/avatars/maria.jpg",
            phone: "+1234567891",
            birth_date: new Date("1988-08-22"),
            gender: "Female"
        },
        preferences: {
            categories: ["Clothing", "Home", "Beauty"],
            brands: ["BasicWear", "HomeDecor"],
            price_range: { min: 20, max: 500 },
            notifications: {
                email: true,
                sms: true,
                push: false
            },
            language: "es",
            currency: "USD"
        },
        addresses: [
            {
                type: "shipping",
                is_default: true,
                street: "789 Pine St",
                city: "Chicago",
                state: "IL",
                postal_code: "60601",
                country: "USA",
                coordinates: {
                    lat: 41.8781,
                    lng: -87.6298
                }
            }
        ],
        loyalty: {
            points: 850,
            tier: "Silver",
            joined_date: new Date("2023-03-10")
        },
        purchase_history: {
            total_orders: 8,
            total_spent: 1680.50,
            avg_order_value: 210.06,
            favorite_categories: ["Clothing", "Home"],
            last_purchase: new Date("2024-11-28")
        },
        created_at: new Date("2023-03-10"),
        updated_at: new Date()
    }
]);

print("✅ Perfiles de usuario insertados");

// =========================================
// 4. INSERCIÓN DE SESIONES DE USUARIO
// =========================================

db.user_sessions.deleteMany({});

db.user_sessions.insertMany([
    {
        session_id: "sess_" + new Date().getTime() + "_1001",
        user_id: 1001,
        session_start: new Date(Date.now() - 1800000), // 30 minutos atrás
        session_end: null,
        device_info: {
            user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            device_type: "desktop",
            browser: "Chrome",
            os: "Windows 10",
            ip_address: "192.168.1.100"
        },
        activities: [
            {
                timestamp: new Date(Date.now() - 1800000),
                action: "login",
                details: { method: "email_password" }
            },
            {
                timestamp: new Date(Date.now() - 1650000),
                action: "view_product",
                details: { product_id: "PHONE-XYZ-001", duration: 120 }
            },
            {
                timestamp: new Date(Date.now() - 1500000),
                action: "add_to_cart",
                details: { product_id: "PHONE-XYZ-001", quantity: 1 }
            },
            {
                timestamp: new Date(Date.now() - 900000),
                action: "view_product",
                details: { product_id: "LAPTOP-ABC-001", duration: 200 }
            }
        ],
        cart: {
            items: [
                {
                    product_id: "PHONE-XYZ-001",
                    quantity: 1,
                    price: 599.99,
                    added_at: new Date(Date.now() - 1500000)
                }
            ],
            total: 599.99,
            currency: "USD"
        },
        created_at: new Date(Date.now() - 1800000),
        updated_at: new Date()
    }
]);

print("✅ Sesiones de usuario insertadas");

// =========================================
// 5. INSERCIÓN DE REVIEWS Y COMENTARIOS
// =========================================

db.reviews.deleteMany({});

db.reviews.insertMany([
    {
        review_id: "rev_" + new Date().getTime() + "_001",
        product_id: "PHONE-XYZ-001",
        user_id: 1002,
        rating: 5,
        title: "Excelente teléfono",
        comment: "Muy buen teléfono, la cámara es increíble y la batería dura todo el día. Lo recomiendo totalmente.",
        pros: ["Excelente cámara", "Batería duradera", "Diseño elegante"],
        cons: ["Un poco caro"],
        verified_purchase: true,
        helpful_votes: 15,
        total_votes: 18,
        media: [
            {
                type: "image",
                url: "https://example.com/reviews/phone-xyz-user-photo1.jpg",
                caption: "Foto tomada con la cámara del teléfono"
            }
        ],
        created_at: new Date(Date.now() - 2592000000), // 30 días atrás
        updated_at: new Date(Date.now() - 2592000000)
    },
    {
        review_id: "rev_" + new Date().getTime() + "_002",
        product_id: "LAPTOP-ABC-001",
        user_id: 1001,
        rating: 4,
        title: "Muy buena laptop para trabajo",
        comment: "Perfecta para programar y usar aplicaciones pesadas. El único detalle es que se calienta un poco con uso intensivo.",
        pros: ["Muy rápida", "Buena pantalla", "Excelente para gaming"],
        cons: ["Se calienta con uso intensivo", "Un poco pesada"],
        verified_purchase: true,
        helpful_votes: 8,
        total_votes: 12,
        created_at: new Date(Date.now() - 1296000000), // 15 días atrás
        updated_at: new Date(Date.now() - 1296000000)
    }
]);

print("✅ Reviews insertadas");

// =========================================
// 6. OPERACIONES CRUD - CREATE
// =========================================

print("\n=== OPERACIONES CREATE ===");

// Insertar nuevo producto
const newProduct = {
    sku: "HEADPHONE-DEF-001",
    name: "Audífonos Inalámbricos DEF",
    description: "Audífonos bluetooth con cancelación de ruido activa",
    category: "Electronics",
    subcategory: "Audio",
    price: 199.99,
    currency: "USD",
    brand: "AudioTech",
    tags: ["headphones", "bluetooth", "noise-cancelling", "wireless"],
    specifications: {
        connectivity: "Bluetooth 5.0",
        battery_life: "30 hours",
        charging_time: "2 hours",
        noise_cancellation: true,
        drivers: "40mm",
        frequency_response: "20Hz - 20kHz",
        weight: 250
    },
    availability: {
        in_stock: true,
        quantity: 75,
        warehouse_location: "WH-001"
    },
    created_at: new Date(),
    updated_at: new Date()
};

const insertResult = db.products_catalog.insertOne(newProduct);
print(`✅ Nuevo producto creado con ID: ${insertResult.insertedId}`);

// =========================================
// 7. OPERACIONES CRUD - READ
// =========================================

print("\n=== OPERACIONES READ ===");

// Buscar productos por categoría
print("📱 Productos en categoría Electronics:");
db.products_catalog.find({ category: "Electronics" }, { name: 1, price: 1, brand: 1 }).forEach(printjson);

// Buscar productos en rango de precio
print("\n💰 Productos entre $100 y $500:");
db.products_catalog.find(
    { price: { $gte: 100, $lte: 500 } },
    { name: 1, price: 1, availability: 1 }
).forEach(printjson);

// Búsqueda de texto completo
print("\n🔍 Búsqueda de texto: 'smartphone camera':");
db.products_catalog.find(
    { $text: { $search: "smartphone camera" } },
    { score: { $meta: "textScore" }, name: 1, price: 1 }
).sort({ score: { $meta: "textScore" } }).forEach(printjson);

// Buscar usuario por email
print("\n👤 Usuario por email:");
const user = db.user_profiles.findOne({ email: "juan.perez@email.com" });
printjson(user);

// Reviews de un producto específico
print("\n⭐ Reviews del producto PHONE-XYZ-001:");
db.reviews.find({ product_id: "PHONE-XYZ-001" }, { rating: 1, title: 1, comment: 1, created_at: 1 }).forEach(printjson);

// =========================================
// 8. OPERACIONES CRUD - UPDATE
// =========================================

print("\n=== OPERACIONES UPDATE ===");

// Actualizar precio de producto
const updatePriceResult = db.products_catalog.updateOne(
    { sku: "PHONE-XYZ-001" },
    { 
        $set: { 
            price: 549.99,
            updated_at: new Date()
        }
    }
);
print(`✅ Precio actualizado. Documentos modificados: ${updatePriceResult.modifiedCount}`);

// Actualizar stock de productos
const updateStockResult = db.products_catalog.updateMany(
    { "availability.quantity": { $lt: 30 } },
    { 
        $inc: { "availability.quantity": 20 },
        $set: { updated_at: new Date() }
    }
);
print(`✅ Stock actualizado en ${updateStockResult.modifiedCount} productos`);

// Agregar dirección a usuario
const addAddressResult = db.user_profiles.updateOne(
    { user_id: 1001 },
    { 
        $push: {
            addresses: {
                type: "work",
                is_default: false,
                street: "999 Business Ave",
                city: "Springfield",
                state: "IL",
                postal_code: "62701",
                country: "USA"
            }
        },
        $set: { updated_at: new Date() }
    }
);
print(`✅ Dirección agregada. Documentos modificados: ${addAddressResult.modifiedCount}`);

// Actualizar preferencias de usuario
db.user_profiles.updateOne(
    { user_id: 1002 },
    {
        $addToSet: { "preferences.categories": "Electronics" },
        $set: { 
            "preferences.price_range.max": 1000,
            updated_at: new Date()
        }
    }
);
print("✅ Preferencias de usuario actualizadas");

// =========================================
// 9. OPERACIONES CRUD - DELETE
// =========================================

print("\n=== OPERACIONES DELETE ===");

// Eliminar review específica (soft delete)
const softDeleteReview = db.reviews.updateOne(
    { review_id: "rev_" + new Date().getTime() + "_001" },
    { 
        $set: { 
            deleted: true,
            deleted_at: new Date(),
            updated_at: new Date()
        }
    }
);
print(`✅ Review marcada como eliminada: ${softDeleteReview.modifiedCount}`);

// Eliminar sesiones antiguas (hard delete)
const deleteOldSessions = db.user_sessions.deleteMany({
    created_at: { $lt: new Date(Date.now() - 2592000000) } // Más de 30 días
});
print(`✅ Sesiones antiguas eliminadas: ${deleteOldSessions.deletedCount}`);

// =========================================
// 10. CONSULTAS AGREGADAS AVANZADAS
// =========================================

print("\n=== CONSULTAS AGREGADAS ===");

// Productos más populares por reviews
print("🏆 Top productos por rating promedio:");
db.reviews.aggregate([
    { $match: { deleted: { $ne: true } } },
    { 
        $group: {
            _id: "$product_id",
            avg_rating: { $avg: "$rating" },
            total_reviews: { $sum: 1 },
            total_helpful_votes: { $sum: "$helpful_votes" }
        }
    },
    { $match: { total_reviews: { $gte: 1 } } },
    { $sort: { avg_rating: -1, total_reviews: -1 } },
    { $limit: 5 }
]).forEach(printjson);

// Análisis de usuarios por tier de lealtad
print("\n👑 Distribución de usuarios por tier:");
db.user_profiles.aggregate([
    {
        $group: {
            _id: "$loyalty.tier",
            count: { $sum: 1 },
            avg_points: { $avg: "$loyalty.points" },
            total_spent: { $sum: "$purchase_history.total_spent" }
        }
    },
    { $sort: { total_spent: -1 } }
]).forEach(printjson);

// Productos con bajo stock
print("\n⚠️ Productos con stock bajo:");
db.products_catalog.aggregate([
    { $match: { "availability.quantity": { $lt: 50 } } },
    {
        $project: {
            name: 1,
            sku: 1,
            current_stock: "$availability.quantity",
            warehouse: "$availability.warehouse_location",
            price: 1
        }
    },
    { $sort: { current_stock: 1 } }
]).forEach(printjson);

print("\n✅ Todas las operaciones CRUD completadas exitosamente");
print("🎉 Setup de MongoDB finalizado");