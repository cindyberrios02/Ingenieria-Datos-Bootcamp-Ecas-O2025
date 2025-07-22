#!/bin/bash

# =========================================
# SCRIPT DE CONFIGURACIÓN PRINCIPAL
# E-commerce Database Ecosystem Setup
# =========================================

set -e  # Salir si cualquier comando falla

echo "🚀 Iniciando configuración del ecosistema de bases de datos..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# =========================================
# VARIABLES DE CONFIGURACIÓN
# =========================================

PROJECT_DIR=$(pwd)
SQL_DIR="$PROJECT_DIR/sql"
NOSQL_DIR="$PROJECT_DIR/nosql"
DATA_DIR="$PROJECT_DIR/data"
SCRIPTS_DIR="$PROJECT_DIR/scripts"

# Base de datos
DB_NAME="ecommerce_db"
DB_USER="ecommerce_user"
DB_PASSWORD="secure_password_123"

# MongoDB
MONGO_DB="ecommerce_nosql"
MONGO_USER="mongo_user"
MONGO_PASSWORD="mongo_password_123"

# Cassandra
CASSANDRA_KEYSPACE="ecommerce_ks"

# =========================================
# FUNCIONES DE VERIFICACIÓN
# =========================================

check_postgresql() {
    log_info "Verificando PostgreSQL..."
    if command -v psql &> /dev/null; then
        log_success "PostgreSQL encontrado"
        return 0
    else
        log_error "PostgreSQL no está instalado"
        return 1
    fi
}

check_mongodb() {
    log_info "Verificando MongoDB..."
    if command -v mongosh &> /dev/null || command -v mongo &> /dev/null; then
        log_success "MongoDB encontrado"
        return 0
    else
        log_error "MongoDB no está instalado"
        return 1
    fi
}

check_mysql() {
    log_info "Verificando MySQL..."
    if command -v mysql &> /dev/null; then
        log_success "MySQL encontrado"
        return 0
    else
        log_warning "MySQL no encontrado (opcional)"
        return 1
    fi
}

check_cassandra() {
    log_info "Verificando Cassandra..."
    if command -v cqlsh &> /dev/null; then
        log_success "Cassandra encontrado"
        return 0
    else
        log_warning "Cassandra no encontrado (opcional)"
        return 1
    fi
}

# =========================================
# CONFIGURACIÓN DE POSTGRESQL
# =========================================

setup_postgresql() {
    log_info "Configurando PostgreSQL..."
    
    # Crear usuario y base de datos
    sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DB_NAME;"
    sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;"
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    
    # Ejecutar scripts de esquema
    if [ -f "$SQL_DIR/postgresql/ecommerce_schema.sql" ]; then
        log_info "Ejecutando esquema de PostgreSQL..."
        PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $DB_NAME -f "$SQL_DIR/postgresql/ecommerce_schema.sql"
        log_success "Esquema de PostgreSQL creado"
    fi
    
    # Ejecutar datos de prueba
    if [ -f "$SQL_DIR/postgresql/sample_data.sql" ]; then
        log_info "Insertando datos de prueba en PostgreSQL..."
        PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $DB_NAME -f "$SQL_DIR/postgresql/sample_data.sql"
        log_success "Datos de prueba insertados en PostgreSQL"
    fi
}

# =========================================
# CONFIGURACIÓN DE MONGODB
# =========================================

setup_mongodb() {
    log_info "Configurando MongoDB..."
    
    # Verificar si MongoDB está corriendo
    if ! pgrep -x "mongod" > /dev/null; then
        log_warning "Iniciando MongoDB..."
        sudo systemctl start mongod || service mongod start
        sleep 5
    fi
    
    # Ejecutar scripts de MongoDB
    if [ -f "$NOSQL_DIR/mongodb/setup.js" ]; then
        log_info "Ejecutando configuración de MongoDB..."
        if command -v mongosh &> /dev/null; then
            mongosh --file "$NOSQL_DIR/mongodb/setup.js"
        else
            mongo < "$NOSQL_DIR/mongodb/setup.js"
        fi
        log_success "MongoDB configurado"
    fi
    
    # Ejecutar datos de prueba
    if [ -f "$NOSQL_DIR/mongodb/sample_data.js" ]; then
        log_info "Insertando datos de prueba en MongoDB..."
        if command -v mongosh &> /dev/null; then
            mongosh --file "$NOSQL_DIR/mongodb/sample_data.js"
        else
            mongo < "$NOSQL_DIR/mongodb/sample_data.js"
        fi
        log_success "Datos de prueba insertados en MongoDB"
    fi
}

# =========================================
# CONFIGURACIÓN DE MYSQL (OPCIONAL)
# =========================================

setup_mysql() {
    if ! check_mysql; then
        log_warning "Saltando configuración de MySQL"
        return
    fi
    
    log_info "Configurando MySQL..."
    
    # Crear base de datos y usuario
    mysql -u root -p -e "DROP DATABASE IF EXISTS ${DB_NAME}_mysql;"
    mysql -u root -p -e "CREATE DATABASE ${DB_NAME}_mysql;"
    mysql -u root -p -e "DROP USER IF EXISTS '${DB_USER}_mysql'@'localhost';"
    mysql -u root -p -e "CREATE USER '${DB_USER}_mysql'@'localhost' IDENTIFIED BY '$DB_PASSWORD';"
    mysql -u root -p -e "GRANT ALL PRIVILEGES ON ${DB_NAME}_mysql.* TO '${DB_USER}_mysql'@'localhost';"
    mysql -u root -p -e "FLUSH PRIVILEGES;"
    
    # Ejecutar scripts de MySQL
    if [ -f "$SQL_DIR/mysql/ecommerce_schema.sql" ]; then
        log_info "Ejecutando esquema de MySQL..."
        mysql -u "${DB_USER}_mysql" -p$DB_PASSWORD "${DB_NAME}_mysql" < "$SQL_DIR/mysql/ecommerce_schema.sql"
        log_success "Esquema de MySQL creado"
    fi
}

# =========================================
# CONFIGURACIÓN DE CASSANDRA (OPCIONAL)
# =========================================

setup_cassandra() {
    if ! check_cassandra; then
        log_warning "Saltando configuración de Cassandra"
        return
    fi
    
    log_info "Configurando Cassandra..."
    
    # Ejecutar scripts de Cassandra
    if [ -f "$NOSQL_DIR/cassandra/keyspace.cql" ]; then
        log_info "Ejecutando configuración de Cassandra..."
        cqlsh -f "$NOSQL_DIR/cassandra/keyspace.cql"
        log_success "Cassandra configurado"
    fi
    
    if [ -f "$NOSQL_DIR/cassandra/tables.cql" ]; then
        log_info "Creando tablas en Cassandra..."
        cqlsh -f "$NOSQL_DIR/cassandra/tables.cql"
        log_success "Tablas de Cassandra creadas"
    fi
}

# =========================================
# GENERACIÓN DE DATOS DE PRUEBA
# =========================================

generate_sample_data() {
    log_info "Generando datos de prueba..."
    
    if [ -f "$SCRIPTS_DIR/data_generator.py" ]; then
        python3 "$SCRIPTS_DIR/data_generator.py"
        log_success "Datos de prueba generados"
    else
        log_warning "Script de generación de datos no encontrado"
    fi
}

# =========================================
# VERIFICACIÓN FINAL
# =========================================

verify_setup() {
    log_info "Verificando configuración final..."
    
    # Verificar PostgreSQL
    if PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) FROM users;" &> /dev/null; then
        log_success "✅ PostgreSQL funcionando correctamente"
    else
        log_error "❌ Error en PostgreSQL"
    fi
    
    # Verificar MongoDB
    if command -v mongosh &> /dev/null; then
        if mongosh --quiet --eval "db.runCommand('ping')" $MONGO_DB &> /dev/null; then
            log_success "✅ MongoDB funcionando correctamente"
        else
            log_error "❌ Error en MongoDB"
        fi
    fi
    
    log_info "Configuración completada!"
}

# =========================================
# FUNCIÓN PRINCIPAL
# =========================================

main() {
    log_info "🎯 Iniciando configuración del ecosistema de bases de datos"
    log_info "📁 Directorio del proyecto: $PROJECT_DIR"
    
    # Verificar herramientas instaladas
    log_info "🔍 Verificando herramientas disponibles..."
    check_postgresql
    check_mongodb
    check_mysql
    check_cassandra
    
    echo
    log_info "🛠️ Iniciando configuración de bases de datos..."
    
    # Configurar PostgreSQL (obligatorio)
    setup_postgresql
    
    # Configurar MongoDB (obligatorio)
    setup_mongodb
    
    # Configurar MySQL (opcional)
    setup_mysql
    
    # Configurar Cassandra (opcional)
    setup_cassandra
    
    # Generar datos de prueba
    generate_sample_data
    
    # Verificación final
    verify_setup
    
    echo
    log_success "🎉 ¡Configuración completada exitosamente!"
    echo
    log_info "📋 Credenciales de acceso:"
    echo "   PostgreSQL:"
    echo "     Host: localhost"
    echo "     Database: $DB_NAME"
    echo "     User: $DB_USER"
    echo "     Password: $DB_PASSWORD"
    echo
    echo "   MongoDB:"
    echo "     Database: $MONGO_DB"
    echo "     Connection: mongodb://localhost:27017/$MONGO_DB"
    echo
    log_info "🚀 El ecosistema de bases de datos está listo para usar!"
}

# Verificar si se está ejecutando como script principal
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi